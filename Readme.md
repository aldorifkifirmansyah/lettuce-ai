# Lettuce AI Detection API

API untuk deteksi pertumbuhan dan penyakit tanaman selada menggunakan model YOLOv8.

## Fitur

- **Deteksi Tahap Pertumbuhan**: Mengidentifikasi tahap pertumbuhan tanaman selada
- **Deteksi Penyakit**: Mendeteksi penyakit pada tanaman selada
- **REST API**: Interface HTTP yang mudah digunakan
- **Upload Gambar**: Mendukung format PNG, JPG, dan JPEG
- **Respons JSON**: Format respons yang terstruktur dengan informasi detail

## Persyaratan Sistem

- Python 3.8+
- pip (Python package manager)

## Instalasi

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd lettuce-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Pastikan model tersedia**
   - Model harus tersimpan di folder `models/`
   - `growth_model.pt` - untuk deteksi pertumbuhan
   - `disease_model.pt` - untuk deteksi penyakit

4. **Buat direktori upload**
   ```bash
   mkdir -p static/uploads
   ```

## Menjalankan Aplikasi

```bash
python app.py
```

Server akan berjalan di `http://localhost:5000`

## Endpoint API

### 1. Status Check
**GET** `/status`

Memeriksa status API dan model yang dimuat.

**Response:**
```json
{
  "status": "online",
  "models_loaded": true,
  "supported_formats": ["png", "jpg", "jpeg"]
}
```

### 2. Deteksi Pertumbuhan
**POST** `/detect-growth`

Mendeteksi tahap pertumbuhan tanaman selada.

**Request:**
- Content-Type: `multipart/form-data`
- Parameter: `image` (file gambar)

**Response:**
```json
{
  "success": true,
  "filename": "1234567890_lettuce.jpg",
  "file_url": "/static/uploads/1234567890_lettuce.jpg",
  "predictions": [
    {
      "id": 0,
      "class_id": 1,
      "class_name": "mature",
      "confidence": 0.8543,
      "bbox": [100.5, 150.2, 300.7, 400.9]
    }
  ]
}
```

### 3. Deteksi Penyakit
**POST** `/detect-disease`

Mendeteksi penyakit pada tanaman selada.

**Request:**
- Content-Type: `multipart/form-data`
- Parameter: `image` (file gambar)

**Response:**
```json
{
  "success": true,
  "filename": "1234567890_lettuce.jpg",
  "file_url": "/static/uploads/1234567890_lettuce.jpg",
  "predictions": [
    {
      "id": 0,
      "class_id": 2,
      "class_name": "leaf_spot",
      "confidence": 0.7821,
      "bbox": [50.3, 75.1, 200.8, 250.4]
    }
  ]
}
```

## Format Respons

### Respons Sukses
- `success`: Boolean, status keberhasilan
- `filename`: String, nama file yang disimpan
- `file_url`: String, URL untuk mengakses file
- `predictions`: Array, hasil prediksi

### Respons Error
```json
{
  "success": false,
  "error": "Error message"
}
```

## Contoh Penggunaan

### Menggunakan cURL

```bash
# Cek status
curl -X GET http://localhost:5000/status

# Deteksi pertumbuhan
curl -X POST \
  -F "image=@path/to/your/lettuce.jpg" \
  http://localhost:5000/detect-growth

# Deteksi penyakit
curl -X POST \
  -F "image=@path/to/your/lettuce.jpg" \
  http://localhost:5000/detect-disease
```

### Menggunakan Python requests

```python
import requests

# Cek status
response = requests.get('http://localhost:5000/status')
print(response.json())

# Deteksi pertumbuhan
with open('lettuce.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5000/detect-growth', files=files)
    print(response.json())
```

### Menggunakan JavaScript (Browser)

```javascript
// Deteksi pertumbuhan
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('/detect-growth', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## Struktur Proyek

```
lettuce-ai/
├── app.py                 # Aplikasi Flask utama
├── requirements.txt       # Dependencies Python
├── README.md             # Dokumentasi ini
├── models/               # Folder model AI
│   ├── growth_model.pt   # Model deteksi pertumbuhan
│   └── disease_model.pt  # Model deteksi penyakit
├── static/
│   └── uploads/          # Folder upload gambar
└── __pycache__/          # Cache Python
```

## Error Handling

API menangani berbagai jenis error:

- **400 Bad Request**: File tidak valid atau tidak ada
- **500 Internal Server Error**: Error saat memproses model atau server

## Konfigurasi

Anda dapat mengubah konfigurasi di file [`app.py`](app.py):

- `UPLOAD_FOLDER`: Direktori penyimpanan file upload
- `ALLOWED_EXTENSIONS`: Format file yang diperbolehkan
- `MODEL_FOLDER`: Direktori model AI

## Troubleshooting

### Model tidak dimuat
- Pastikan file model ada di folder `models/`
- Periksa format file (.pt untuk PyTorch)
- Cek log error saat startup

### Error upload file
- Pastikan format file didukung (PNG, JPG, JPEG)
- Periksa ukuran file tidak terlalu besar
- Pastikan direktori `static/uploads/` ada dan writable

### Server tidak dapat diakses
- Periksa port 5000 tidak digunakan aplikasi lain
- Pastikan firewall tidak memblokir koneksi
- Untuk akses eksternal, ubah host ke `0.0.0.0`

## Tentang
Proyek ini dibuat untuk mata kuliah PPL ADPL Semester 4, Kelompok 9:
Fionella Vernanda P. A. O   (232410103021)
Aldo Rifki Firmansyah       (232410103025)
Naufal Rifqi Prasetyo       (232410103055)
Adelia Damar Cantika        (232410103092)
Bramudya Melvan Ibrahim     (232410103097)
