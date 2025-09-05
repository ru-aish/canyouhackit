# HackBite - Self-Contained Backend

## 🚀 Quick Start (From `/1` Directory)

### **Start the Backend Server**
```bash
cd /path/to/your/1/directory
python3 run_server.py
```

### **Access the Application**
- **API Server**: http://localhost:5000
- **Frontend**: Open `frontend/registration/login.html` in your browser

---

## 📁 Project Structure

```
1/
├── backend/                    # Backend API code
│   ├── __init__.py
│   ├── api_server.py          # Flask REST API
│   ├── database.py            # Database management
│   └── registration_system.py # CLI interface
├── frontend/                   # Frontend code
│   └── registration/
│       ├── login.html         # Registration form
│       ├── login.js           # Frontend logic
│       └── login.css          # Styling
├── sql/                       # Database schema
│   └── create_tables.sql      # Table definitions
├── database/                  # SQLite database (auto-created)
│   └── database.db           # User data storage
├── tests/                     # Test files
├── run_server.py             # Main server launcher ⭐
├── test_backend.py           # Backend test script
├── setup.sh                  # Setup script
├── requirements.txt          # Python dependencies
└── backend_description.md    # Technical documentation
```

---

## 🛠 Installation & Setup

### **1. Install Dependencies**
```bash
# Using pip
pip install -r requirements.txt

# Or using pip3
pip3 install -r requirements.txt

# Or run the setup script
chmod +x setup.sh
./setup.sh
```

### **2. Test the Backend**
```bash
python3 test_backend.py
```

### **3. Start the Server**
```bash
python3 run_server.py
```

---

## 🌐 API Endpoints

### **User Management**
- `POST /api/register` - Register new user
- `POST /api/login` - User authentication  
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get specific user
- `PUT /api/users/<id>/profile-logo` - Update avatar

### **Data & Analytics**
- `GET /api/profile-logos` - Available avatars
- `GET /api/statistics` - User statistics
- `GET /api/skill-categories` - Skill categories
- `GET /health` - Health check

---

## 🎯 Usage Examples

### **Start Server with Custom Options**
```bash
# Custom port
python3 run_server.py --port 8080

# Custom host and debug mode
python3 run_server.py --host 127.0.0.1 --debug

# Help
python3 run_server.py --help
```

### **Test API Manually**
```bash
# Health check
curl http://localhost:5000/health

# Register user
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"pass123","profile_logo":"rocket"}'

# Get users
curl http://localhost:5000/api/users
```

### **Frontend Integration**
The frontend registration form automatically connects to the backend:
1. Start backend: `python3 run_server.py`
2. Open `frontend/registration/login.html` in browser
3. Fill out registration form
4. Data is saved to SQLite database

---

## ☁️ Cloud Deployment

### **Upload to Cloud**
1. **Zip the entire `/1` directory**
2. **Upload to your cloud platform** (AWS, Google Cloud, Azure, etc.)
3. **Install Python dependencies** on the server
4. **Run the server**

### **Platform-Specific Instructions**

#### **Heroku**
```bash
# Create Procfile
echo "web: python3 run_server.py --port \$PORT --host 0.0.0.0" > Procfile

# Deploy
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
git push heroku main
```

#### **Railway**
```bash
# No additional setup needed
# Railway auto-detects Python and runs the app
```

#### **Render**
```bash
# Build command: pip install -r requirements.txt
# Start command: python3 run_server.py --port $PORT --host 0.0.0.0
```

#### **DigitalOcean App Platform**
```yaml
# app.yaml
name: hackbite
services:
- name: web
  source_dir: /
  github:
    repo: your-username/your-repo
    branch: main
  run_command: python3 run_server.py --port $PORT --host 0.0.0.0
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
```

---

## 🔧 Configuration

### **Environment Variables**
```bash
# Optional environment variables
export FLASK_ENV=production        # Production mode
export DATABASE_PATH=database/prod.db  # Custom database path
export PORT=5000                   # Server port
export HOST=0.0.0.0               # Server host
```

### **Production Considerations**
1. **Use a production WSGI server** (gunicorn, uWSGI)
2. **Set up reverse proxy** (nginx, Apache)
3. **Enable HTTPS** with SSL certificates
4. **Configure proper CORS origins**
5. **Set up database backups**
6. **Monitor logs and performance**

### **Production Server Setup**
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.api_server:app
```

---

## 🐛 Troubleshooting

### **Common Issues**

#### **Port Already in Use**
```bash
# Check what's using the port
lsof -i :5000

# Kill existing processes
pkill -f "python3 run_server.py"
```

#### **Module Import Errors**
```bash
# Install missing dependencies
pip install -r requirements.txt

# Check Python path
python3 -c "import sys; print(sys.path)"
```

#### **Database Issues**
```bash
# Reset database
rm database/database.db

# Test database
python3 test_backend.py
```

#### **Frontend Can't Connect**
1. Ensure server is running: `curl http://localhost:5000/health`
2. Check CORS settings in browser console
3. Verify API_BASE_URL in `frontend/registration/login.js`

---

## 📊 Features

### **Current Features**
✅ User registration with avatars and skills  
✅ Secure password hashing  
✅ Email uniqueness validation  
✅ SQLite database with comprehensive schema  
✅ REST API with CORS support  
✅ Activity logging and analytics  
✅ Frontend integration ready  

### **Future-Ready Features**
🔜 Team formation and management  
🔜 Multi-hackathon support  
🔜 Skill-based team matching  
🔜 Notification system  
🔜 Advanced user profiles  
🔜 Real-time chat integration  

---

## 🎉 You're Ready!

The entire HackBite backend is now self-contained in the `/1` directory and ready for cloud deployment. Just run:

```bash
cd /path/to/your/1/directory
python3 run_server.py
```

And your hackathon registration system is live! 🚀