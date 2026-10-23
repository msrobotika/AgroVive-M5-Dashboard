# AB-GEN | AgroVive M5 Dashboard

> **Ficha del proyecto · MS ROBOTIKA**  
> **Estado:** Demostrador agrícola / investigación de visión artificial  
> **Licencia del código:** [AGPL-3.0](LICENSE) presente en main. Los pesos, datasets y fotografías pueden tener licencias y derechos independientes aún pendientes de inventario.  
> [Estado técnico](docs/PROJECT_STATUS.md) · [Política de evidencias](EVIDENCE_STATUS.md) · [CI de integridad](.github/workflows/ci.yml) · [Problemas y evidencias](https://github.com/msrobotika/AgroVive-M5-Dashboard/issues)  
> **EVIDENCIA PENDIENTE:** el rendimiento y las cifras de consumo divulgados previamente no están acreditados como benchmarks independientes reproducibles. La galería contiene imágenes agrícolas de ejemplo, no capturas verificadas de ejecución.
### Experimental non-CNN agricultural image-classification dashboard

[![Status: Experimental](https://img.shields.io/badge/Status-Experimental-grey.svg)](https://github.com/msrobotika/AgroVive-M5-Dashboard)
[![Code license: AGPL-3.0](https://img.shields.io/badge/Code%20license-AGPL--3.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![YouTube Demo](https://img.shields.io/badge/YouTube-Video%20Demo-red.svg)](https://youtu.be/C9E_C58Cu3U?is=9MVm3AbTfJL4_KCd)

**AB-GEN AgroVive** is a research dashboard exploring a non-CNN classification pipeline for agricultural images. Historical project material reports near-perfect PlantVillage performance, but that number has **not been independently reproduced through a documented leakage-free RAW→prediction evaluation**. No energy advantage over CNNs has been verified under a matched benchmarking protocol.

---

**Scope:** demonstration and research, not a certified plant-disease diagnostic service or a basis for automated pesticide application. See [Safety & security](SECURITY.md), [License](LICENSE) and [Evidence status](EVIDENCE_STATUS.md). Models, datasets and images can have separate rights.

---

## 📺 Live Demonstration
[![AgroVive M5 Interface](https://img.youtube.com/vi/C9E_C58Cu3U/maxresdefault.jpg)](https://youtu.be/C9E_C58Cu3U?is=9MVm3AbTfJL4_KCd)

*Click the image above to watch the Dashboard analyzing crops in real-time.*

---

## Research questions and hypotheses

The prototype explores geometric and spectral features. The following are research hypotheses, **not established commercial or scientific performance advantages**:

*   🌿 **Green AI**: Can lower resource use in principle; no matching joules-per-image benchmark is currently validated.
*   🔍 **XAI (Explainable AI)**: The pipeline exposes intermediate signals, but this does not establish faithful explanations of model decisions.
*   ⚡ **Latency target**: runtime benchmarks on actual Edge hardware are needed; no zero-latency claim.
*   🎯 **Accuracy target**: requires contamination checks, identical splits and comparisons to clearly specified baselines.

---

## 🔬 Scientific Whitepaper
For a deep dive into the **M5 Feature Space** (PCA-Fisher Projection, Multi-Scale FFT, and Gradient Similarity Bridges), read the official document:

See the [AB-GEN reproducibility audit](https://github.com/msrobotika/AB-GEN-Green-AI) and [local evidence-status requirements](EVIDENCE_STATUS.md).

---

## Historical accuracy claims — NOT VALIDATED in this repository

The original project README included PlantVillage ~100%, MNIST 97.79%, Fashion-MNIST 90.17% and CIFAR-10 ~85.20% along with claimed SOTA margins. **These are historical assertions, not verified benchmark results.** In particular, they should not be interpreted as matching the independently audited AB-GEN evaluation records, which have different documented routes and accuracies. Reproducible source commits, dataset hashes, preprocessing, splits, predictions and baselines are required before any number can be advertised as validated.

---

## 🚀 Quick Setup (Local Dashboard)

To run the M5 Dashboard locally on your machine:

1. **Clone the Repo:**
   ```bash
   git clone https://github.com/msrobotika/AgroVive-M5-Dashboard.git
   cd AgroVive-M5-Dashboard/demo
   ```
2. **Execute the Launcher:**
   Double-click `run_demo.bat` (Windows) or run:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
3. **Open Browser:** `http://127.0.0.1:5000`

---

## 🤝 Contact & Commercial Licensing
This project is part of the **msrobotika** AI ecosystem. For commercial inquiries, clinical integration, or partnership opportunities, please reach out via the GitHub profile.

---
© 2026 msrobotika. Advanced Agentic Coding Project.
