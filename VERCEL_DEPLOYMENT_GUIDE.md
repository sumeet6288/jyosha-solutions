# Complete Vercel Deployment Guide - BotSmith Chatbot Builder

## Prerequisites
- ✅ GitHub repository with your code
- ✅ Vercel account (sign up at vercel.com)
- ✅ MongoDB Atlas account (for production database)
- ✅ API keys for AI providers (optional - can use Emergent LLM key)

---

## Part 1: Setup MongoDB Atlas (Database)

### Step 1: Create MongoDB Atlas Cluster
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up or log in
3. Click **"Build a Database"**
4. Choose **"M0 Free"** tier
5. Select your preferred cloud provider and region
6. Name your cluster (e.g., "botsmith-prod")
7. Click **"Create"**

### Step 2: Configure Database Access
1. In Atlas dashboard, go to **"Database Access"**
2. Click **"Add New Database User"**
3. Create username and strong password (save these!)
4. Set permissions to **"Read and write to any database"**
5. Click **"Add User"**

### Step 3: Configure Network Access
1. Go to **"Network Access"**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0)
   - For production, you can restrict to Vercel IPs later
4. Click **"Confirm"**

### Step 4: Get Connection String
1. Go to **"Database"** → Click **"Connect"**
2. Choose **"Connect your application"**
3. Copy the connection string (looks like):
   ```
   mongodb+srv://username:<password>@cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
4. Replace `<password>` with your actual password
5. Add database name before the `?`: 
   ```
   mongodb+srv://username:password@cluster.xxxxx.mongodb.net/botsmith?retryWrites=true&w=majority
   ```

---

## Part 2: Deploy Backend (FastAPI) on Vercel

### Step 1: Create vercel.json for Backend
In your backend directory, create a `vercel.json` file:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "server.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "server.py"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.11"
  }
}
```

### Step 2: Create requirements.txt in Backend Root
Ensure your `requirements.txt` is in the backend directory (already done ✅)

### Step 3: Deploy Backend to Vercel

**Option A: Using Vercel Dashboard**
1. Go to https://vercel.com/dashboard
2. Click **"Add New"** → **"Project"**
3. Import your GitHub repository
4. Vercel will detect it as a monorepo
5. Configure project:
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/`

6. Add Environment Variables (click "Environment Variables"):
   ```
   MONGO_URL = mongodb+srv://username:password@cluster.xxxxx.mongodb.net/botsmith?retryWrites=true&w=majority
   JWT_SECRET = your-super-secret-jwt-key-min-32-chars
   EMERGENT_LLM_KEY = your-emergent-llm-key (optional)
   ALLOWED_ORIGINS = https://your-frontend-url.vercel.app
   ```

7. Click **"Deploy"**
8. Wait for deployment to complete (5-10 minutes)
9. Copy your backend URL (e.g., `https://your-backend.vercel.app`)

**Option B: Using Vercel CLI**
```bash
cd backend
npm i -g vercel
vercel login
vercel --prod
```

### Step 4: Test Backend Deployment
Visit: `https://your-backend.vercel.app/api/chatbots`
Should return JSON (empty array or data)

---

## Part 3: Deploy Frontend (React) on Vercel

### Step 1: Update Frontend Environment Variables
Edit `/app/frontend/.env`:
```env
REACT_APP_BACKEND_URL=https://your-backend.vercel.app
```

### Step 2: Create vercel.json for Frontend
In your frontend directory, create `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### Step 3: Update package.json Scripts
Ensure your frontend `package.json` has:
```json
{
  "scripts": {
    "start": "craco start",
    "build": "craco build",
    "vercel-build": "craco build"
  }
}
```

### Step 4: Deploy Frontend to Vercel

**Option A: Using Vercel Dashboard**
1. Go to https://vercel.com/dashboard
2. Click **"Add New"** → **"Project"**
3. Import your GitHub repository (same repo, different project)
4. Configure project:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `yarn build` or `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `yarn install`

5. Add Environment Variables:
   ```
   REACT_APP_BACKEND_URL = https://your-backend.vercel.app
   ```

6. Click **"Deploy"**
7. Wait for deployment (3-5 minutes)
8. Your app will be live at: `https://your-frontend.vercel.app`

**Option B: Using Vercel CLI**
```bash
cd frontend
vercel --prod
```

---

## Part 4: Connect Backend to Frontend

### Step 1: Update Backend CORS Settings
Go back to your backend deployment on Vercel:
1. Click **"Settings"** → **"Environment Variables"**
2. Update `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS = https://your-frontend.vercel.app,https://your-custom-domain.com
   ```
3. Redeploy backend (go to Deployments → click "..." → "Redeploy")

### Step 2: Verify Frontend Environment
1. Go to frontend deployment settings
2. Verify `REACT_APP_BACKEND_URL` is correct
3. If you change it, redeploy frontend

---

## Part 5: Custom Domain (Optional)

### For Backend:
1. In Vercel dashboard, open your backend project
2. Go to **"Settings"** → **"Domains"**
3. Add your domain: `api.yourdomain.com`
4. Follow Vercel's DNS instructions
5. Update frontend `REACT_APP_BACKEND_URL` to use custom domain

### For Frontend:
1. In Vercel dashboard, open your frontend project
2. Go to **"Settings"** → **"Domains"**
3. Add your domain: `yourdomain.com` or `app.yourdomain.com`
4. Follow Vercel's DNS instructions
5. Update backend `ALLOWED_ORIGINS` to include custom domain

---

## Part 6: Post-Deployment Configuration

### 1. Test All Features
- ✅ Login/Registration (if auth is enabled)
- ✅ Create a chatbot
- ✅ Upload files (test with small file first)
- ✅ Add website source
- ✅ Test chat with AI
- ✅ Check analytics
- ✅ Test public chat link

### 2. Monitor Logs
- **Backend logs**: Vercel Dashboard → Your Backend Project → "Logs"
- **Frontend logs**: Browser console (F12)

### 3. Set Up Continuous Deployment
Vercel automatically deploys when you push to GitHub:
- **Production branch**: `main` or `master`
- **Preview deployments**: Any other branch

---

## Troubleshooting Common Issues

### Issue 1: Backend Shows 404
**Solution**: Check vercel.json routes configuration. Ensure all API routes start with `/api/`

### Issue 2: CORS Errors
**Solution**: 
1. Update backend `ALLOWED_ORIGINS` environment variable
2. Include your frontend URL
3. Redeploy backend

### Issue 3: Database Connection Failed
**Solution**:
1. Verify MongoDB Atlas IP whitelist includes 0.0.0.0/0
2. Check connection string in `MONGO_URL` environment variable
3. Ensure password doesn't contain special characters (or URL encode them)

### Issue 4: Build Fails - emergentintegrations
**Solution**: Ensure install command includes:
```bash
pip install -r requirements.txt --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

### Issue 5: Frontend Can't Connect to Backend
**Solution**:
1. Check `REACT_APP_BACKEND_URL` in frontend environment variables
2. Ensure it ends without trailing slash
3. Test backend URL directly in browser
4. Verify CORS is properly configured

### Issue 6: Function Timeout
**Solution**: Vercel has 10-second timeout on hobby plan, 60 seconds on pro
- For long operations (file uploads), consider:
  1. Upgrading to Vercel Pro
  2. Using async background processing
  3. Implementing chunked uploads

### Issue 7: File Upload Fails
**Solution**:
1. Vercel has 5MB limit for hobby plan (50MB for Pro)
2. Consider using direct S3 uploads for large files
3. Implement chunked upload for files >5MB

---

## Environment Variables Summary

### Backend Environment Variables:
```env
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/botsmith?retryWrites=true&w=majority
JWT_SECRET=your-super-secret-jwt-key-minimum-32-characters-long
EMERGENT_LLM_KEY=your-emergent-llm-key
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### Frontend Environment Variables:
```env
REACT_APP_BACKEND_URL=https://your-backend.vercel.app
```

---

## Alternative Deployment Options

### If Vercel Backend Has Issues:

**Option 1: Railway.app (Recommended for Python)**
- Better for long-running processes
- Simpler Python deployment
- Built-in PostgreSQL/MongoDB

**Option 2: Render.com**
- Good Python support
- Free tier available
- Auto-deploys from GitHub

**Option 3: AWS Lambda + API Gateway**
- More scalable
- Pay-per-use pricing
- Requires more setup

### Frontend stays on Vercel (best for static sites)

---

## Cost Estimates

### Free Tier (Hobby):
- **Vercel**: Free for both frontend + backend
  - 100 GB bandwidth/month
  - 100 GB-hours serverless function execution
  
- **MongoDB Atlas**: Free M0 cluster
  - 512 MB storage
  - Shared RAM
  - Good for testing/small apps

### Paid Options:
- **Vercel Pro**: $20/month
  - 1 TB bandwidth
  - No team members
  - Faster builds
  
- **MongoDB Atlas M10**: ~$57/month
  - 10 GB storage
  - Dedicated RAM
  - Better performance

---

## Next Steps After Deployment

1. ✅ Test all features thoroughly
2. ✅ Set up custom domain
3. ✅ Configure monitoring/alerts
4. ✅ Set up backup strategy for MongoDB
5. ✅ Add SSL certificate (automatic with Vercel)
6. ✅ Set up analytics (Vercel Analytics)
7. ✅ Configure preview deployments for staging

---

## Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **MongoDB Atlas Docs**: https://docs.atlas.mongodb.com/
- **FastAPI on Vercel**: https://vercel.com/guides/deploying-fastapi-with-vercel
- **React on Vercel**: https://vercel.com/guides/deploying-react-with-vercel

---

## Quick Reference Commands

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy backend
cd backend
vercel --prod

# Deploy frontend
cd frontend
vercel --prod

# Check logs
vercel logs <deployment-url>

# Pull environment variables locally
vercel env pull
```

---

**🎉 Congratulations! Your BotSmith Chatbot Builder should now be live on Vercel!**

Visit your frontend URL and start building chatbots! 🚀
