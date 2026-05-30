# Setup and Installation Guide for Crop Disease Detection

## Quick Start (5 minutes)

### 1. Prerequisites
- Python 3.11+
- pip or poetry
- Git

### 2. Installation

```bash
# Clone repository
git clone https://github.com/Zain4111552/crop-disease-detection.git
cd crop-disease-detection

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app.database import init_db; init_db()"
```

### 3. Running the Application

```bash
# Development mode (with auto-reload)
python app/main.py

# Production mode (with Gunicorn)
gunicorn "app.main:app" -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 4. Access the Application

Open your browser and navigate to:
- **Scanner Interface**: http://localhost:8000
- **Admin Dashboard**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/docs

---

## Project Structure

```
crop-disease-detection/
├── app/
│   ├── __init__.py              # App initialization
│   ├── main.py                  # FastAPI application
│   ├── config.py                # Configuration management
│   ├── models.py                # Pydantic schemas
│   ├── database.py              # SQLite management
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── inference.py         # ML model pipeline
│   │   └── disease_mappings.py  # Disease protocols
│   └── routes/
│       ├── __init__.py
│       ├── scanner.py           # Scan endpoints
│       └── admin.py             # Dashboard endpoints
├── static/
│   ├── css/
│   │   └── style.css            # Premium styles
│   └── js/
│       ├── scanner.js           # Scanner logic
│       └── admin.js             # Dashboard logic
├── templates/
│   ├── index.html               # Scanner UI
│   └── admin.html               # Dashboard UI
├── database/
│   └── schema.sql               # SQLite schema
├── requirements.txt             # Dependencies
├── .env.example                 # Environment template
└── README.md                    # Documentation
```

---

## API Endpoints

### Scanner Endpoints

#### POST `/api/scan`
Upload and analyze crop image
- **Request**: multipart/form-data (image file)
- **Response**: Disease prediction with confidence and latency

```bash
curl -X POST "http://localhost:8000/api/scan" \
  -F "file=@crop_image.jpg"
```

#### GET `/api/scan/history`
Retrieve scan history
- **Query**: `limit` (default: 50)

```bash
curl "http://localhost:8000/api/scan/history?limit=20"
```

#### GET `/api/scan/disease/{disease_name}`
Get disease details and treatment protocols

```bash
curl "http://localhost:8000/api/scan/disease/powdery_mildew"
```

#### GET `/api/scan/diseases`
List all supported diseases

```bash
curl "http://localhost:8000/api/scan/diseases"
```

### Admin Endpoints

#### GET `/api/admin/stats`
System statistics and KPIs

```bash
curl "http://localhost:8000/api/admin/stats"
```

#### GET `/api/admin/diagnostics`
Diagnostic logs
- **Query**: `limit` (default: 100)

```bash
curl "http://localhost:8000/api/admin/diagnostics?limit=50"
```

#### GET `/api/admin/distribution`
Disease distribution breakdown

```bash
curl "http://localhost:8000/api/admin/distribution"
```

#### GET `/api/admin/health`
System health check

```bash
curl "http://localhost:8000/api/admin/health"
```

---

## Environment Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

### Configuration Variables

```env
# FastAPI
DEBUG=True
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Database
DATABASE_URL=sqlite:///./crop_disease_detection.db
DB_PATH=./crop_disease_detection.db

# Security
SECRET_KEY=change-this-in-production
ADMIN_PASSWORD=admin123

# ML Model
MODEL_CONFIDENCE_THRESHOLD=0.75

# Upload
MAX_UPLOAD_SIZE_MB=10
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif
```

---

## Database Schema

The application uses SQLite with three main tables:

### `scans` Table
Logs all crop scanning operations:
- `id` - Primary key
- `timestamp` - When scan occurred
- `disease_name` - Detected disease
- `confidence_score` - Classification confidence (0-100)
- `processing_latency_ms` - Inference time
- `image_filename` - Uploaded image name
- `user_ip` - Client IP address

### `disease_statistics` Table
Aggregated disease occurrence data:
- `disease_name` - Disease identifier
- `occurrence_count` - Total detections
- `average_confidence` - Mean confidence
- `last_detected` - Most recent detection

### `system_metrics` Table
Performance monitoring data:
- `total_scans` - Cumulative scans
- `average_latency_ms` - Average inference time
- `system_accuracy_rate` - Classification accuracy

---

## Disease Classification

The system supports 9 disease types:

1. **Powdery Mildew** - Fungal infection with white coating
2. **Early Blight** - Concentric lesions on lower leaves
3. **Late Blight** - Rapid plant collapse (critical)
4. **Septoria Leaf Spot** - Circular spots with dark margins
5. **Fusarium Wilt** - Vascular discoloration (soil-borne)
6. **Downy Mildew** - Yellow spots with downy growth
7. **Alternaria Leaf Spot** - Dark concentric spots
8. **Bacterial Wilt** - Insect-transmitted rapid collapse
9. **Healthy** - No detectable disease

Each disease includes:
- Severity level (none/mild/moderate/high/severe)
- Description and affected areas
- Treatment protocols (immediate, biological, preventative)

---

## Development

### Code Style

```bash
# Format code with Black
black app/

# Linting with Pylint
pylint app/

# Type checking with mypy
mypy app/
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/

# With coverage
pytest --cov=app tests/
```

---

## Production Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t crop-detection .
docker run -p 8000:8000 crop-detection
```

### Using Systemd (Linux)

Create `/etc/systemd/system/crop-detection.service`:

```ini
[Unit]
Description=Crop Disease Detection Application
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/crop-detection
ExecStart=/var/www/crop-detection/venv/bin/gunicorn \
    "app.main:app" \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable crop-detection
sudo systemctl start crop-detection
```

---

## Troubleshooting

### Database Issues
```bash
# Reset database
rm crop_disease_detection.db
python -c "from app.database import init_db; init_db()"
```

### Port Already in Use
```bash
# Find process on port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### CORS Issues
Ensure CORS middleware is enabled in `app/main.py` for frontend requests.

---

## Support & Documentation

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **GitHub Issues**: [Report bugs](https://github.com/Zain4111552/crop-disease-detection/issues)

---

## License

MIT License - See LICENSE file for details

---

**Built with ❤️ for precision agriculture**
