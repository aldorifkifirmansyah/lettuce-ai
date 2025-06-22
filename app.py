from flask import Flask, request, jsonify
from ultralytics import YOLO
import os
from werkzeug.utils import secure_filename
import time
import numpy as np
from PIL import Image
import traceback

app = Flask(__name__)

# Konfigurasi
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan direktori model ada
MODEL_FOLDER = 'models'
os.makedirs(MODEL_FOLDER, exist_ok=True)

# Cek file yang diperbolehkan
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load models dengan error handling
try:
    growth_model = YOLO(os.path.join(MODEL_FOLDER, 'growth_model.pt'))
    disease_model = YOLO(os.path.join(MODEL_FOLDER, 'disease_model.pt'))
    models_loaded = True
except Exception as e:
    print(f"Error loading models: {e}")
    models_loaded = False

@app.route('/status', methods=['GET'])
def status():
    """Endpoint untuk memeriksa status API dan model"""
    return jsonify({
        'status': 'online',
        'models_loaded': models_loaded,
        'supported_formats': list(ALLOWED_EXTENSIONS)
    })

@app.route('/detect-growth', methods=['POST'])
def detect_growth():
    """Endpoint untuk deteksi pertumbuhan"""
    if not models_loaded:
        return jsonify({'error': 'Models not loaded correctly'}), 500
    return detect(growth_model)

@app.route('/detect-disease', methods=['POST'])
def detect_disease():
    """Endpoint untuk deteksi penyakit"""
    if not models_loaded:
        return jsonify({'error': 'Models not loaded correctly'}), 500
    return detect(disease_model)

def detect(model):
    """Fungsi utama untuk deteksi dengan model YOLOv8"""
    # Cek apakah ada file yang diunggah
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    
    # Cek apakah file kosong
    if file.filename == '':
        return jsonify({'error': 'Empty file submitted'}), 400
    
    # Cek apakah file diperbolehkan
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Supported types: {ALLOWED_EXTENSIONS}'}), 400
    
    try:
        # Buat nama file unik
        timestamp = int(time.time())
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Simpan file
        file.save(path)
        
        # Jalankan prediksi
        results = model(path)
        
        # Siapkan respons lengkap
        response = {
            'success': True,
            'filename': filename,
            'file_url': f"/static/uploads/{filename}",
            'predictions': []
        }
        
        # Jika ada hasil deteksi
        if len(results) > 0 and len(results[0].boxes) > 0:
            labels = results[0].names
            boxes = results[0].boxes
            
            for i, box in enumerate(boxes):
                class_id = int(box.cls.item())
                confidence = float(box.conf.item())
                coords = box.xyxy.tolist()[0]  # [x1, y1, x2, y2]
                
                prediction = {
                    'id': i,
                    'class_id': class_id,
                    'class_name': labels[class_id],
                    'confidence': round(confidence, 4),
                    'bbox': [round(x, 2) for x in coords]
                }
                response['predictions'].append(prediction)
        
        return jsonify(response)
    
    except Exception as e:
        # Log error untuk debugging
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
    # cleanup file yang diunggah jika tidak diperlukan
    finally:
        if os.path.exists(path):
            os.remove(path)

if __name__ == '__main__':
    # Buat direktori upload jika belum ada
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Jalankan aplikasi
    app.run(debug=True, host='0.0.0.0', port=5000)