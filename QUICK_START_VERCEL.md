# 🚀 Quick Start: Deploy BotSmith to Vercel in 20 Minutes

## 📋 What You'll Need
- ✅ GitHub account with your code pushed
- ✅ Vercel account (free) - Sign up at https://vercel.com
- ✅ MongoDB Atlas account (free) - Sign up at https://www.mongodb.com/cloud/atlas
- ✅ 20 minutes of your time

---

## 🗄️ STEP 1: Setup MongoDB (5 min)

### 1.1 Create Database
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up or login
3. Click **"Build a Database"**
4. Select **"M0 FREE"**
5. Choose any cloud provider (AWS recommended)
6. Name it: `botsmith-prod`
7. Click **"Create"**

### 1.2 Create Database User
1. You'll see a popup "Security Quickstart"
2. Choose **"Username and Password"**
3. Username: `botsmith`
4. Click **"Autogenerate Secure Password"** and **COPY IT!**
5. Click **"Create User"**

### 1.3 Allow Access
1. In the same popup, select **"Cloud Environment"**
2. It will show IP: `0.0.0.0/0` (allow from anywhere)
3. Click **"Add Entry"**
4. Click **"Finish and Close"**

### 1.4 Get Connection String
1. Click **"Database"** in left menu
2. Click **"Connect"** button
3. Choose **"Drivers"**
4. Copy the connection string (looks like):
   ```
   mongodb+srv://botsmith:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with the password you copied
6. Change `/?retryWrites` to `/botsmith?retryWrites`

**Final connection string should look like:**
```
mongodb+srv://botsmith:your_password@cluster0.xxxxx.mongodb.net/botsmith?retryWrites=true&w=majority
```

**SAVE THIS!** You'll need it in the next step! 📝

---

## 🔧 STEP 2: Deploy Backend to Vercel (10 min)

### 2.1 Import Project
1. Go to https://vercel.com/dashboard
2. Click **"Add New"** → **"Project"**
3. Click **"Import Git Repository"**
4. Find your GitHub repo and click **"Import"**

### 2.2 Configure Backend
Vercel will show configuration screen:

**Root Directory:**
- Click **"Edit"** next to Root Directory
- Type: `backend`
- Click **"Continue"**

**Build Settings:**
- Framework Preset: **Other**
- Build Command: Leave empty
- Output Directory: Leave empty
- Install Command: 
  ```
  pip install -r requirements.txt --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
  ```

### 2.3 Add Environment Variables
Click **"Environment Variables"** section:

**Add these 3 variables:**

1. **Variable 1:**
   - Name: `MONGO_URL`
   - Value: `mongodb+srv://botsmith:your_password@cluster0.xxxxx.mongodb.net/botsmith?retryWrites=true&w=majority`
   - (Use YOUR connection string from Step 1.4!)

2. **Variable 2:**
   - Name: `JWT_SECRET`
   - Value: Any random 32+ character string
   - Example: `my-super-secret-jwt-key-change-this-in-production-2025`

3. **Variable 3:**
   - Name: `EMERGENT_LLM_KEY`
   - Value: Your Emergent universal key (get from your profile)
   - (Or leave empty if you have individual API keys)

### 2.4 Deploy!
1. Click **"Deploy"**
2. Wait 5-10 minutes for build to complete
3. You'll see: **"Congratulations! Your project has been deployed"** 🎉
4. **COPY YOUR BACKEND URL!** (looks like `https://your-project-backend.vercel.app`)

### 2.5 Test Backend
Open in browser: `https://your-project-backend.vercel.app/api/chatbots`

Should see: `[]` or JSON data (not an error!)

✅ Backend deployed successfully!

---

## 🎨 STEP 3: Deploy Frontend to Vercel (5 min)

### 3.1 Create New Project
1. Go back to https://vercel.com/dashboard
2. Click **"Add New"** → **"Project"**
3. Import the **SAME GitHub repository** again
4. Click **"Import"**

### 3.2 Configure Frontend
**Root Directory:**
- Click **"Edit"**
- Type: `frontend`
- Click **"Continue"**

**Build Settings:**
- Framework Preset: **Create React App** (auto-detected)
- Build Command: `yarn build`
- Output Directory: `build`
- Install Command: `yarn install`

### 3.3 Add Environment Variable
Click **"Environment Variables"**:

**Add 1 variable:**
- Name: `REACT_APP_BACKEND_URL`
- Value: Your backend URL from Step 2.4
- Example: `https://your-project-backend.vercel.app`
- ⚠️ **NO trailing slash!** ⚠️

### 3.4 Deploy!
1. Click **"Deploy"**
2. Wait 3-5 minutes
3. You'll see: **"Congratulations!"** 🎉
4. Click **"Visit"** to see your live app!

✅ Frontend deployed successfully!

---

## 🔗 STEP 4: Connect Backend & Frontend (2 min)

### 4.1 Update Backend CORS
1. Go back to Vercel dashboard
2. Open your **backend project**
3. Click **"Settings"**
4. Click **"Environment Variables"**
5. Click **"Add New"**:
   - Name: `ALLOWED_ORIGINS`
   - Value: Your frontend URL (e.g., `https://your-project.vercel.app`)
6. Click **"Save"**

### 4.2 Redeploy Backend
1. Click **"Deployments"** tab
2. Find the latest deployment
3. Click **"..."** (three dots)
4. Click **"Redeploy"**
5. Click **"Redeploy"** to confirm

Wait 2-3 minutes for redeployment.

✅ Backend and frontend connected!

---

## 🧪 STEP 5: Test Your App!

### Open your frontend URL and test:

1. **✅ Create a Chatbot**
   - Click "Create New"
   - Enter name
   - Select AI provider (OpenAI GPT-4o-mini)
   - Click "Create"

2. **✅ Add a Source**
   - Click "Add Source"
   - Try "Add Text Content"
   - Paste some text
   - Click "Add"

3. **✅ Test Chat**
   - Click "Preview" button
   - Send a message
   - AI should respond! 🤖

4. **✅ Check Analytics**
   - Go to Analytics tab
   - Should see stats

---

## 🎉 DONE! Your App is Live!

Your chatbot builder is now deployed and working on Vercel!

### Your URLs:
- 🎨 **Frontend**: `https://your-project.vercel.app`
- 🔧 **Backend**: `https://your-project-backend.vercel.app`
- 🗄️ **Database**: MongoDB Atlas

---

## 🆘 Troubleshooting

### Problem: Backend shows "Application Error"
**Solution:** 
1. Check Vercel logs: Backend project → Deployments → View Function Logs
2. Verify `MONGO_URL` is correct
3. Check MongoDB Atlas network access allows 0.0.0.0/0

### Problem: Frontend shows "Network Error"
**Solution:**
1. Verify `REACT_APP_BACKEND_URL` is correct (no trailing slash)
2. Check backend is working: `https://your-backend.vercel.app/api/chatbots`
3. Verify `ALLOWED_ORIGINS` in backend includes frontend URL

### Problem: Chat doesn't respond
**Solution:**
1. Check `EMERGENT_LLM_KEY` is set in backend
2. Or add individual API keys (OPENAI_API_KEY, etc.)
3. Check backend logs for errors

### Problem: Build Failed
**Solution:**
1. Backend: Check install command includes `--extra-index-url`
2. Frontend: Ensure Root Directory is set to `frontend`
3. Check error logs in Vercel deployment

---

## 📚 Additional Resources

- **Full Deployment Guide**: `/app/VERCEL_DEPLOYMENT_GUIDE.md`
- **Checklist**: `/app/DEPLOYMENT_CHECKLIST.md`
- **Environment Variables**: `/app/backend/.env.template` & `/app/frontend/.env.template`

---

## 🔐 Security Reminders

- ✅ Never commit `.env` files to GitHub
- ✅ Use strong passwords for MongoDB
- ✅ Keep JWT_SECRET secret and random
- ✅ In production, restrict MongoDB IP access

---

## 🚀 Next Steps

1. **Custom Domain**: Vercel Settings → Domains → Add your domain
2. **Monitoring**: Enable Vercel Analytics
3. **Backups**: Set up MongoDB automated backups
4. **SSL**: Automatic with Vercel! ✅
5. **CI/CD**: Automatic deployments on git push! ✅

---

## 💡 Pro Tips

- Use **Preview Deployments** for testing: Push to any branch except main
- **Environment Variables** can be different per environment (Production/Preview/Development)
- **Vercel CLI** for faster deployments: `npm i -g vercel`
- **Monitor costs**: Free tier is generous but watch usage

---

**Congratulations! You're now a Vercel deployment expert!** 🎊

Need help? Check the troubleshooting section or full guide.

Happy building! 🚀
