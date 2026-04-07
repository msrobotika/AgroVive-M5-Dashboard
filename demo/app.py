from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from engine import AgroViveEngine, SimpleSoftVoting, TorchLogisticRegression, TorchMLP
import uuid
import sys

# Patch for Pickle/Joblib to find classes in __main__
import __main__
__main__.SimpleSoftVoting = SimpleSoftVoting
__main__.TorchLogisticRegression = TorchLogisticRegression
__main__.TorchMLP = TorchMLP

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Engine
engine = AgroViveEngine(models_path="models")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Selected file is empty"}), 400

    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        result = engine.predict(filepath)
        result['image_url'] = f"/static/uploads/{filename}"
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
