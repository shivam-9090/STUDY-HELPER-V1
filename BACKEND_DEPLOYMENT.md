# 🚀 Backend Deployment Guide - Study Helper AI

This guide will help you deploy your Flask backend to production using Render (free tier).

## 📋 Deployment Options

### Option 1: Render.com (RECOMMENDED - Free Forever)
- ✅ Free tier forever
- ✅ Auto-deploys from Git
- ✅ SSL/HTTPS included
- ✅ Simple setup
- ⏱️ Spins down after inactivity (restarts in ~30s)

### Option 2: Railway.app
- ✅ $5 free credit monthly
- ✅ Fast deployment
- ⚠️ Paid after credit runs out

### Option 3: Heroku
- ⚠️ No longer free
- Starting at $5/month

---

## 🎯 Deploy to Render (FREE)

### Step 1: Prepare Your Repository

1. **Commit all backend changes:**
```bash
cd E:\APPS\STUDY-HELPER-V1
git add backend/
git commit -m "Prepare backend for production deployment"
git push origin main
```

### Step 2: Create Render Account

1. Go to: https://render.com/
2. Sign up with GitHub account (easiest)
3. Authorize Render to access your repository

### Step 3: Create Web Service

1. **Dashboard** → **New** → **Web Service**
2. **Connect Repository:**
   - Select your `STUDY-HELPER-V1` repository
   - Click **Connect**

3. **Configure Service:**
   ```
   Name: study-helper-backend
   Region: Oregon (US West) - fastest
   Branch: main
   Root Directory: backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   Instance Type: Free
   ```

4. **Environment Variables:**
   Click **Advanced** → **Add Environment Variable**
   
   Add these:
   ```
   FLASK_ENV = production
   GEMINI_API_KEY = your_actual_gemini_api_key_here
   PORT = 10000
   ```

5. **Click "Create Web Service"**

### Step 4: Wait for Deployment

- Build time: ~2-3 minutes
- You'll see logs in real-time
- ✅ Look for: "Your service is live 🎉"

### Step 5: Get Your Backend URL

Your backend will be at:
```
https://study-helper-backend.onrender.com
```

Or custom: `https://your-service-name.onrender.com`

### Step 6: Test Your Backend

```bash
# Test health endpoint
curl https://study-helper-backend.onrender.com/health

# Should return: {"status":"healthy"}
```

---

## 🔧 Update Flutter App with Production URL

### Option A: Hardcode Production URL (Simple)

Edit: `E:\APPS\STUDY-HELPER-V1\frontend\lib\services\api_service.dart`

```dart
class ApiService {
  // Change this line:
  static const String baseUrl = 'https://study-helper-backend.onrender.com/api';
  
  // Old: 'http://127.0.0.1:5000/api'
```

### Option B: Environment-Based URLs (Better)

1. Create config file:

**File:** `frontend/lib/config/api_config.dart`
```dart
class ApiConfig {
  static const bool isDevelopment = bool.fromEnvironment('dart.vm.product') == false;
  
  static String get baseUrl {
    if (isDevelopment) {
      return 'http://10.0.2.2:5000/api'; // Android emulator
    } else {
      return 'https://study-helper-backend.onrender.com/api'; // Production
    }
  }
}
```

2. Update `api_service.dart`:
```dart
import 'package:study_helper/config/api_config.dart';

class ApiService {
  static final String baseUrl = ApiConfig.baseUrl;
  // rest of your code...
}
```

### Rebuild Your App

```bash
cd E:\APPS\STUDY-HELPER-V1\frontend
flutter build appbundle --release
```

New AAB will be at: `build/app/outputs/bundle/release/app-release.aab`

---

## 🔍 Troubleshooting

### Issue: "Application Error" or 500

**Check Render Logs:**
1. Render Dashboard → Your Service → **Logs** tab
2. Look for Python errors
3. Common issues:
   - Missing `GEMINI_API_KEY`
   - SQLAlchemy database errors
   - Import errors

**Fix:**
- Add missing environment variables
- Check `requirements.txt` has all dependencies
- Redeploy: **Manual Deploy** → **Deploy latest commit**

### Issue: "Service Unavailable" after inactivity

**Render free tier spins down after 15 minutes:**
- First request takes ~30 seconds to wake up
- Add loading state in Flutter app
- Or upgrade to paid ($7/month for always-on)

### Issue: CORS errors in Flutter app

**Update `app.py`:**
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

Then redeploy.

### Issue: Database not persisting

**Render free tier doesn't persist SQLite files:**

Options:
1. **Use Render PostgreSQL** (free tier available)
2. **Use external database** (Supabase, PlanetScale)
3. **Keep SQLite** (data resets on each deploy - OK for chat history)

For PostgreSQL:
```python
# In app.py, change:
import os
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///study_helper.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
```

Then add PostgreSQL in Render dashboard.

---

## 📊 Monitor Your Backend

### Render Dashboard Shows:
- ✅ Deploy status
- 📊 CPU/Memory usage
- 📝 Real-time logs
- 🌐 Request metrics

### Set Up Alerts:
1. Render Dashboard → Your Service → **Settings**
2. **Notification Settings** → Add email
3. Get notified of:
   - Deploy failures
   - Service crashes
   - High resource usage

---

## 🔐 Security Best Practices

### 1. Environment Variables (NEVER commit!)
```bash
# backend/.env is in .gitignore
GEMINI_API_KEY=your_real_key_here
```

### 2. Add Rate Limiting (Optional)
```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("20 per minute")
def chat():
    # your code...
```

### 3. API Key Validation
```python
# Optional: Add API key for Flutter app
API_KEY = os.getenv('APP_API_KEY')

@app.before_request
def validate_api_key():
    if request.path.startswith('/api/'):
        key = request.headers.get('X-API-Key')
        if key != API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
```

---

## 💰 Costs

### Render Free Tier:
- ✅ **$0/month**
- 750 hours/month compute time
- Spins down after 15 min inactivity
- 512 MB RAM
- Shared CPU

### Render Paid ($7/month):
- Always-on (no spin down)
- 512 MB RAM
- Better performance

---

## 🚀 Quick Deploy Checklist

- [ ] Commit backend code to Git
- [ ] Push to GitHub
- [ ] Create Render account
- [ ] Create new Web Service
- [ ] Configure build/start commands
- [ ] Add environment variables (GEMINI_API_KEY)
- [ ] Deploy and wait for build
- [ ] Test health endpoint
- [ ] Update Flutter app with production URL
- [ ] Rebuild Flutter AAB
- [ ] Test app with production backend

---

## 📝 Example: Full Deployment Flow

```bash
# 1. Commit backend
cd E:\APPS\STUDY-HELPER-V1
git add backend/
git commit -m "Add production deployment files"
git push origin main

# 2. Deploy on Render (via web dashboard)
# ... follow steps above ...

# 3. Update Flutter with production URL
# Edit: frontend/lib/services/api_service.dart
# Change: baseUrl = 'https://study-helper-backend.onrender.com/api'

# 4. Rebuild Flutter app
cd frontend
flutter clean
flutter build appbundle --release

# 5. Upload new AAB to Play Store
# File: build/app/outputs/bundle/release/app-release.aab
```

---

## 🆘 Need Help?

- Render Docs: https://render.com/docs
- Flask Deployment: https://flask.palletsprojects.com/en/3.0.x/deploying/
- Issues: Check Render logs first!

---

## 🎯 Alternative: Quick Deploy with Railway

### Railway.app (5 minutes setup)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Deploy
cd E:\APPS\STUDY-HELPER-V1\backend
railway init
railway up

# 4. Get URL
railway domain
```

Your backend will be at: `https://your-project.up.railway.app`

---

**Ready to deploy? Follow the Render steps above! 🚀**
