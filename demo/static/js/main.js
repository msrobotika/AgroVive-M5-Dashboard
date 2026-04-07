document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const selectBtn = document.getElementById('select-btn');
    const resultsPanel = document.getElementById('results-panel');
    const previewImg = document.getElementById('preview-img');
    const predictionText = document.getElementById('final-prediction');
    const confidenceText = document.getElementById('confidence-val');
    const confidenceFill = document.getElementById('confidence-fill');
    const m5RouteText = document.getElementById('m5-route');
    const inferenceTimeText = document.getElementById('inference-time');
    const top3List = document.getElementById('top3-list');
    const toast = document.getElementById('toast');

    // -- Event Listeners --

    selectBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleUpload(e.target.files[0]);
        }
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = "#00FF41";
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = "var(--border-gl)";
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = "var(--border-gl)";
        if (e.dataTransfer.files.length > 0) {
            handleUpload(e.dataTransfer.files[0]);
        }
    });

    // -- Core Logic --

    async function handleUpload(file) {
        // Show loading state
        resultsPanel.classList.remove('hidden');
        resultsPanel.scrollIntoView({ behavior: 'smooth' });
        predictionText.innerText = "Analizando...";
        confidenceText.innerText = "---%";
        confidenceFill.style.width = "0%";

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (data.error) throw new Error(data.error);

            // Update UI
            renderResults(data);

        } catch (err) {
            showError(err.message);
        }
    }

    function renderResults(data) {
        // 1. Image Preview
        previewImg.src = data.image_url;

        // 2. Final Prediction (Clean up names)
        const cleanName = data.prediction.replace(/___/g, ' - ').replace(/_/g, ' ');
        predictionText.innerText = cleanName;
        
        // Color coding for health
        if (cleanName.toLowerCase().includes('healthy')) {
            predictionText.style.color = "#00FF41";
        } else {
            predictionText.style.color = "#FF8A00"; // Alarm Orange
        }

        // 3. Confidence Meter
        const confPercent = (data.confidence * 100).toFixed(2);
        confidenceText.innerText = `${confPercent}%`;
        confidenceFill.style.width = `${confPercent}%`;

        // 4. Meta
        m5RouteText.innerText = data.m5_route;
        inferenceTimeText.innerText = `${(data.inference_time * 1000).toFixed(0)}ms`;

        // 5. Top 3 List
        top3List.innerHTML = '';
        data.top3.forEach(item => {
            const li = document.createElement('li');
            const cleanItemName = item.class.replace(/___/g, ' - ').replace(/_/g, ' ');
            li.innerHTML = `
                <span class="li-class">${cleanItemName}</span>
                <span class="li-val">${(item.conf * 100).toFixed(2)}%</span>
            `;
            top3List.appendChild(li);
        });
    }

    function showError(msg) {
        toast.innerText = `Error: ${msg}`;
        toast.classList.remove('hidden');
        setTimeout(() => toast.classList.add('hidden'), 5000);
    }
});
