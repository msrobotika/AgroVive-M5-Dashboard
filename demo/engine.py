import os
import joblib
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms
from pathlib import Path
import time

class TorchLogisticRegression(nn.Module):
    def __init__(self, input_dim, num_classes, device="cpu"):
        super().__init__()
        self.device = device
        self.model = nn.Linear(input_dim, num_classes).to(self.device)
    def predict_proba(self, X):
        self.model.eval()
        X_t = torch.tensor(X, dtype=torch.float32)
        with torch.no_grad():
            probs = F.softmax(self.model(X_t.to(self.device)), dim=1).cpu().numpy()
        return probs

class TorchMLP(nn.Module):
    def __init__(self, input_dim, hidden_layers, num_classes, dropout=0.2, device="cpu"):
        super().__init__()
        self.device = device
        layers = []
        in_d = input_dim
        for h in hidden_layers:
            layers.extend([nn.Linear(in_d, h), nn.BatchNorm1d(h), nn.ReLU(), nn.Dropout(dropout)])
            in_d = h
        layers.append(nn.Linear(in_d, num_classes))
        self.model = nn.Sequential(*layers).to(self.device)
    def predict_proba(self, X):
        self.model.eval()
        X_t = torch.tensor(X, dtype=torch.float32)
        with torch.no_grad():
            probs = F.softmax(self.model(X_t.to(self.device)), dim=1).cpu().numpy()
        return probs

class SimpleSoftVoting:
    def __init__(self, estimators, weights):
        self.estimators_ = estimators
        self.weights = np.asarray(weights, dtype=np.float32)
    def predict_proba(self, x):
        wsum = float(self.weights.sum())
        prob = None
        for est, w in zip(self.estimators_, self.weights):
            p = est.predict_proba(x)
            prob = p * w if prob is None else prob + p * w
        return prob / wsum

class AgroViveEngine:
    def __init__(self, models_path="models"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.models_path = Path(models_path)
        self.componentes_pca = 1200
        self._load_models()
        self.transform = transforms.Compose([
            transforms.Resize((64, 64)),
            transforms.ToTensor()
        ])
        # Mapping standard plantvillage (Alphabetical)
        self.classes = [
            "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
            "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
            "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_",
            "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy", "Grape___Black_rot",
            "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
            "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot", "Peach___healthy",
            "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy", "Potato___Early_blight",
            "Potato___Late_blight", "Potato___healthy", "Raspberry___healthy", "Soybean___healthy",
            "Squash___Powdery_mildew", "Strawberry___Leaf_scorch", "Strawberry___healthy",
            "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold",
            "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite",
            "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus",
            "Tomato___healthy"
        ]

    def _load_models(self):
        print(f"Loading M5 Engine components from {self.models_path}...")
        topologia = joblib.load(self.models_path / "abgen_topologia_pca.pkl")
        self.ipca = topologia['pca_modelo']
        self.pesos_f = topologia['pesos_fisher']
        self.cent_norm = topologia['centroides_norm']
        
        self.n1_voting = joblib.load(self.models_path / "agro_quimera_n1_elite.pkl")
        self.n2_dict = joblib.load(self.models_path / "agro_quimera_n2_poly_elite.pkl")
        print("Models online.")

    def _f32(self, x): 
        return x.to(dtype=torch.float32) if torch.is_tensor(x) else np.asarray(x, dtype=np.float32)

    def _normalize_l2_rows(self, x): 
        return (x / (np.linalg.norm(x, axis=1, keepdims=True) + 1e-8)).astype(np.float32)

    def _multi_scale_fft(self, x_pca):
        def fft_b(x_np, blk):
            n_blocks = self.componentes_pca // blk
            with torch.no_grad():
                batch = torch.as_tensor(x_np, dtype=torch.float32, device=self.device)
                parts = [torch.abs(torch.fft.rfft(batch[:, b*blk:(b+1)*blk], dim=1)) for b in range(n_blocks)]
                return torch.cat(parts, dim=1).cpu().numpy().astype(np.float32)
        
        mi, md = fft_b(x_pca, 40), fft_b(x_pca, 200)
        mi /= (mi.max(axis=1, keepdims=True) + 1e-8)
        md /= (md.max(axis=1, keepdims=True) + 1e-8)
        
        with torch.no_grad():
            seg = torch.as_tensor(x_pca, dtype=torch.float32, device=self.device)
            ma = torch.abs(torch.fft.rfft(seg, dim=1)).cpu().numpy().astype(np.float32)
        ma /= (ma.max(axis=1, keepdims=True) + 1e-8)
        return np.hstack([x_pca, mi, md, ma])[:, self.componentes_pca:]

    def _construir_features(self, x_pca_w):
        xn = self._normalize_l2_rows(x_pca_w)
        sims = xn @ self.cent_norm.T
        qik = self._f32((sims**2) / ((sims**2).sum(axis=1, keepdims=True) + 1e-8))
        hcr = self._f32(np.hstack([sims, sims**2, sims**3]))
        dists = 1.0 - sims
        topo = self._f32(np.hstack([dists.mean(axis=1, keepdims=True), 
                                   dists.std(axis=1, keepdims=True), 
                                   dists.min(axis=1, keepdims=True), 
                                   dists.std(axis=1, keepdims=True)/(dists.mean(axis=1, keepdims=True)+1e-8)]))
        xd, cd = np.diff(xn, axis=1), np.diff(self.cent_norm, axis=1)
        gsb = self._f32((xd @ cd.T) / (np.abs(xd @ cd.T).max(axis=1, keepdims=True) + 1e-8))
        return np.hstack([x_pca_w, self._multi_scale_fft(x_pca_w), qik, hcr, topo, gsb]).astype(np.float32)

    def _extract_logit_features(self, x):
        probs = []
        rng = np.random.default_rng(42)
        for est in self.n1_voting.estimators_:
            p = est.predict_proba(x) 
            p += est.predict_proba(x + rng.normal(0, 0.015, x.shape).astype(np.float32))
            p = p / 2.0
            logit_p = np.log(p + 1e-8)
            probs.append(logit_p.astype(np.float32))
        return np.hstack(probs).astype(np.float32)

    def predict(self, image_path):
        start_time = time.time()
        img = Image.open(image_path).convert('RGB')
        x_tensor = self.transform(img)
        x_raw = x_tensor.numpy().flatten().reshape(1, -1)

        # 1. M5 Topological Feature Extraction
        x_pca = self.ipca.transform(x_raw)
        x_w = self._f32(x_pca * self.pesos_f)
        x_feat = self._construir_features(x_w)

        # 2. Level N1 (Voting Logits)
        prob_n1 = self.n1_voting.predict_proba(x_feat)[0]
        top3_indices = np.argsort(prob_n1)[::-1][:3]
        
        # 3. Level N2 (Poly-Ridge Meta-Learner)
        meta_feat = self._extract_logit_features(x_feat)
        poly_x = self.n2_dict['poly'].transform(meta_feat)
        scaled_x = self.n2_dict['scaler'].transform(poly_x)
        pred_idx = self.n2_dict['ridge'].predict(scaled_x)[0]
        
        confidence = float(prob_n1[pred_idx])
        
        result = {
            "prediction": self.classes[pred_idx],
            "confidence": confidence,
            "inference_time": round(time.time() - start_time, 4),
            "m5_route": "M4 (Fast Resoluion)" if confidence >= 0.75 else "M5 (Complex Topology Activation)",
            "top3": [
                {"class": self.classes[idx], "conf": round(float(prob_n1[idx]), 4)}
                for idx in top3_indices
            ]
        }
        return result
