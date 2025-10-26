# Pre-Deployment Checklist ✅

## Before You Deploy

### 1. GitHub Repository Setup
- [ ] Code pushed to GitHub
- [ ] Repository is public or Vercel has access
- [ ] All latest changes committed
- [ ] `.env` files are in `.gitignore` (security!)

### 2. MongoDB Atlas Setup
- [ ] MongoDB Atlas account created
- [ ] Free M0 cluster created
- [ ] Database user created with password
- [ ] Network access set to 0.0.0.0/0 (allow from anywhere)
- [ ] Connection string copied and ready

### 3. Required Files Created ✅
- [x] `/app/backend/vercel.json` - Backend configuration
- [x] `/app/frontend/vercel.json` - Frontend configuration
- [x] `/app/backend/.vercelignore` - Files to ignore
- [x] `/app/frontend/.vercelignore` - Files to ignore
- [x] `/app/backend/requirements.txt` - Python dependencies
- [x] `/app/frontend/package.json` - Node dependencies
- [x] `/app/VERCEL_DEPLOYMENT_GUIDE.md` - Complete guide
- [x] `/app/DEPLOYMENT_INFO.md` - Package versions info

---

## Deployment Steps (Quick Version)

### Step 1: Setup MongoDB (5 minutes)
1. Create MongoDB Atlas account → https://www.mongodb.com/cloud/atlas
2. Create free M0 cluster
3. Create database user
4. Whitelist IP: 0.0.0.0/0
5. Copy connection string: `mongodb+srv://user:password@cluster.xxxxx.mongodb.net/botsmith?retryWrites=true&w=majority`

### Step 2: Deploy Backend to Vercel (10 minutes)
1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Set Root Directory: `backend`
5. Set Install Command: `pip install -r requirements.txt --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/`
6. Add Environment Variables:
   - `MONGO_URL` = your MongoDB connection string
   - `JWT_SECRET` = random 32+ character string
   - `EMERGENT_LLM_KEY` = your emergent key (optional)
7. Click Deploy
8. Copy backend URL: `https://your-backend.vercel.app`

### Step 3: Deploy Frontend to Vercel (5 minutes)
1. Click "Add New" → "Project" (new project)
2. Import same GitHub repository
3. Set Root Directory: `frontend`
4. Set Build Command: `yarn build`
5. Set Output Directory: `build`
6. Add Environment Variables:
   - `REACT_APP_BACKEND_URL` = your backend URL from Step 2
7. Click Deploy
8. Your app is live! 🎉

### Step 4: Update CORS (2 minutes)
1. Go to backend project in Vercel
2. Settings → Environment Variables
3. Add: `ALLOWED_ORIGINS` = your frontend URL
4. Redeploy backend

---

## Environment Variables Reference

### Backend (.env)
```env
MONGO_URL=mongodb+srv://username:password@cluster.xxxxx.mongodb.net/botsmith?retryWrites=true&w=majority
JWT_SECRET=your-super-secret-jwt-key-at-least-32-characters-long-random-string
EMERGENT_LLM_KEY=your-emergent-llm-universal-key
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=https://your-backend.vercel.app
```

---

## Post-Deployment Testing

### Test Checklist
- [ ] Frontend loads without errors
- [ ] Backend API responds: `https://your-backend.vercel.app/api/chatbots`
- [ ] Can create a new chatbot
- [ ] Can add text source
- [ ] Can test chat (AI responds)
- [ ] Analytics page loads
- [ ] Public chat link works

### If Something Doesn't Work
1. Check Vercel logs (Deployments → View Function Logs)
2. Check browser console (F12)
3. Verify environment variables are set correctly
4. Ensure MongoDB connection string is correct
5. Check CORS configuration

---

## Important Notes

### Vercel Limitations (Free Tier)
- ⏱️ 10-second timeout for serverless functions
- 📦 5MB request/response size limit
- 🔄 100 GB bandwidth per month
- 💾 Serverless function size: 50MB max

### Recommended Upgrades
- For production: Upgrade to Vercel Pro ($20/month)
- For better database: MongoDB Atlas M10 ($57/month)
- For file uploads >5MB: Use S3 or chunked uploads

### Security Best Practices
- ✅ Never commit `.env` files
- ✅ Use strong JWT_SECRET (32+ characters)
- ✅ Restrict MongoDB IP access in production
- ✅ Enable rate limiting for APIs
- ✅ Use HTTPS only (Vercel provides this automatically)

---

## Useful Commands

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy from command line
vercel --prod

# View logs
vercel logs <deployment-url>

# Set environment variable
vercel env add MONGO_URL production
```

---

## Quick Links

- 📖 Full Guide: `/app/VERCEL_DEPLOYMENT_GUIDE.md`
- 📦 Package Info: `/app/DEPLOYMENT_INFO.md`
- 🔧 Vercel Dashboard: https://vercel.com/dashboard
- 🗄️ MongoDB Atlas: https://cloud.mongodb.com/
- 📚 Vercel Docs: https://vercel.com/docs

---

## Need Help?

Common issues and solutions are in the main deployment guide.

**Your app is fully prepared for deployment!** 🚀

All configuration files are ready. Just follow the steps above!
