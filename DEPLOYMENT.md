# Cloud Deployment Guide

## 🚀 Quick Cloud Deployment

### **Step 1: Prepare Your `/1` Directory**
```bash
# Ensure everything is working locally
cd /path/to/your/1/directory
python3 test_backend.py
python3 run_server.py --port 8000
```

### **Step 2: Create Deployment Files**

#### **For Heroku:**
```bash
# Create Procfile
echo "web: python3 run_server.py --port \$PORT --host 0.0.0.0" > Procfile

# Create runtime.txt (optional)
echo "python-3.11.0" > runtime.txt
```

#### **For Railway/Render:**
```bash
# Create start command in package.json (optional)
echo '{"scripts": {"start": "python3 run_server.py --port $PORT --host 0.0.0.0"}}' > package.json
```

### **Step 3: Deploy**

#### **Option A: Git-based Deployment**
```bash
git init
git add .
git commit -m "HackBite backend deployment"

# Push to your preferred platform
# Heroku: heroku create && git push heroku main
# Railway: Connect GitHub repo
# Render: Connect GitHub repo
```

#### **Option B: Direct Upload**
1. Zip the entire `/1` directory
2. Upload to your cloud platform
3. Set start command: `python3 run_server.py --port $PORT --host 0.0.0.0`

### **Step 4: Configure Environment**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python3 run_server.py --port $PORT --host 0.0.0.0`
- **Python Version**: 3.8+

### **Step 5: Test Deployment**
```bash
# Test your deployed API
curl https://your-app.platform.com/health
curl https://your-app.platform.com/api/profile-logos
```

## 🎉 Done!
Your HackBite backend is now live on the cloud!