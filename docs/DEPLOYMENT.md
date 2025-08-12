# 🚀 Deployment Guide

This guide covers various deployment options for CineMatch.

## 📋 Prerequisites

- Python 3.8+
- Git
- Your movie dataset (`movies.csv`)

## 🌐 Streamlit Cloud (Recommended)

### Step 1: Prepare Repository
```bash
# Ensure your repo is public on GitHub
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `app.py`
6. Click "Deploy!"

### Step 3: Configure Secrets (if needed)
If you have API keys or secrets:
1. Go to app settings
2. Add secrets in TOML format:
```toml
[secrets]
api_key = "your-api-key"
```

## 🐳 Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run
```bash
# Build the image
docker build -t cinematch .

# Run the container
docker run -p 8501:8501 cinematch
```

### Docker Compose
```yaml
version: '3.8'
services:
  cinematch:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## ☁️ Cloud Platforms

### Heroku

1. **Create Procfile**
```bash
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Create runtime.txt**
```
python-3.9.16
```

3. **Deploy**
```bash
# Install Heroku CLI
heroku create your-app-name
git push heroku main
```

### Google Cloud Platform

1. **Create app.yaml**
```yaml
runtime: python39

env_variables:
  STREAMLIT_SERVER_PORT: 8080
  STREAMLIT_SERVER_ADDRESS: 0.0.0.0

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

2. **Deploy**
```bash
gcloud app deploy
```

### AWS EC2

1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 LTS
   - Configure security group (port 8501)

2. **Setup Application**
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip git

# Clone repository
git clone https://github.com/yourusername/cinematch.git
cd cinematch

# Install requirements
pip3 install -r requirements.txt

# Run application
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

3. **Setup as Service**
```bash
# Create service file
sudo nano /etc/systemd/system/cinematch.service
```

```ini
[Unit]
Description=CineMatch Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/cinematch
ExecStart=/home/ubuntu/.local/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable cinematch
sudo systemctl start cinematch
```

## 🔧 Configuration

### Environment Variables
```bash
# Set in your deployment environment
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Streamlit Config
Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
address = "0.0.0.0"
runOnSave = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#ff6b6b"
backgroundColor = "#0c0c0c"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#ffffff"
```

## 📊 Performance Optimization

### Caching
```python
# Use Streamlit caching effectively
@st.cache_data
def load_data():
    return pd.read_csv('data/movies.csv')

@st.cache_resource
def load_model():
    return MovieRecommendationSystem()
```

### Memory Management
```python
# For large datasets
import gc

def cleanup_memory():
    gc.collect()
    
# Call after heavy operations
cleanup_memory()
```

### Resource Limits
```yaml
# For containerized deployments
resources:
  limits:
    memory: "2Gi"
    cpu: "1000m"
  requests:
    memory: "1Gi"
    cpu: "500m"
```

## 🔒 Security

### HTTPS Setup
```nginx
# Nginx configuration
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Environment Secrets
```python
# Use environment variables for sensitive data
import os

API_KEY = os.getenv('API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
```

## 📈 Monitoring

### Health Checks
```python
# Add to your app
def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

# Endpoint for monitoring
if st.sidebar.button("Health Check"):
    st.json(health_check())
```

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9
```

2. **Memory Issues**
```python
# Reduce dataset size
df = df.sample(n=10000)  # Use 10K movies instead of full dataset
```

3. **Slow Loading**
```python
# Optimize data loading
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    return pd.read_csv('data/movies.csv')
```

### Performance Monitoring
```bash
# Monitor resource usage
htop
docker stats  # For Docker deployments
```

## 📱 Mobile Optimization

### Responsive Design
```css
/* Add to your CSS */
@media (max-width: 768px) {
    .main-title {
        font-size: 2rem;
    }
    
    .movie-card {
        padding: 1rem;
    }
}
```

### Touch-Friendly Interface
```python
# Use appropriate Streamlit components
st.button("Search", use_container_width=True)  # Full-width buttons
st.selectbox("Options", options, key="mobile_select")  # Better for mobile
```

## 🔄 CI/CD Pipeline

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python -m pytest tests/
    - name: Deploy
      run: echo "Deployment triggered"
```

---

**Need help with deployment?** Check our [Contributing Guide](../CONTRIBUTING.md) or open an issue on GitHub.