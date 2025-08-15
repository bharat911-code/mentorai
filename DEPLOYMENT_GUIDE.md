# Complete Deployment Guide

## Step 1: Get HuggingFace Token (FREE)

1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Give it a name like "looore-api"
4. Select "Read" role
5. Copy the token (starts with `hf_`)

## Step 2: Deploy Backend on Render

### 2.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Verify your email

### 2.2 Deploy Backend
1. Click "New" → "Web Service"
2. Connect your GitHub repo
3. Configure:
   - **Name**: `looore-backend` (or any name)
   - **Environment**: `Docker`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty (root)
   - **Build Command**: Leave empty (uses Dockerfile)
   - **Start Command**: Leave empty (uses Dockerfile CMD)

### 2.3 Add Environment Variable
1. Go to "Environment" tab
2. Add variable:
   - **Key**: `HF_TOKEN`
   - **Value**: Your HuggingFace token (starts with `hf_`)

### 2.4 Deploy
1. Click "Create Web Service"
2. Wait for build (5-10 minutes)
3. Copy the URL (e.g., `https://looore-backend.onrender.com`)

## Step 3: Update Frontend API URL

1. Open `frontend/src/App.tsx`
2. Find line with `fetch('https://your-backend-name.onrender.com/ask'`
3. Replace `your-backend-name` with your actual Render service name
4. Save the file

## Step 4: Deploy Frontend

### Option A: Vercel (Recommended)
1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "New Project"
4. Import your repo
5. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Deploy

### Option B: Netlify
1. Go to https://netlify.com
2. Sign up with GitHub
3. Click "New site from Git"
4. Select your repo
5. Configure:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
6. Deploy

### Option C: GitHub Pages
1. Push your code to GitHub
2. Go to repo Settings → Pages
3. Set source to "GitHub Actions"
4. Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [ main ]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '18'
    - name: Install dependencies
      run: |
        cd frontend
        npm install
    - name: Build
      run: |
        cd frontend
        npm run build
    - name: Deploy
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./frontend/dist
```

## Step 5: Test Your Deployment

1. **Test Backend**: Visit your Render URL + `/health`
   - Should show: `{"status": "healthy", "model_initialized": true, "personalities_loaded": 5}`

2. **Test Frontend**: Visit your frontend URL
   - Should load the chat interface
   - Try asking a question

## Troubleshooting

### Backend Issues
- **Build fails**: Check Render logs for Python version issues
- **Model not loading**: Verify HF_TOKEN is set correctly
- **CORS errors**: Backend has CORS enabled, check frontend URL

### Frontend Issues
- **API errors**: Verify the backend URL in App.tsx
- **Build fails**: Check Node.js version (use 18+)
- **Images not loading**: Ensure images are in `public/personalitiesimgs/`

### Common Fixes
1. **Python 3.13 error**: Dockerfile already uses Python 3.11
2. **Memory issues**: HuggingFace API handles this automatically
3. **Timeout errors**: Responses take 2-5 seconds, this is normal

## Cost Breakdown (FREE)

- **HuggingFace API**: 30,000 requests/month free
- **Render**: 750 hours/month free
- **Vercel/Netlify**: Unlimited static sites free
- **Total**: $0/month

## Monitoring

- **Render Dashboard**: Monitor backend health and logs
- **Vercel/Netlify Dashboard**: Monitor frontend deployments
- **HuggingFace**: Monitor API usage in account settings

## Next Steps

1. **Custom Domain**: Add your own domain to frontend
2. **Analytics**: Add Google Analytics or similar
3. **Supabase**: Add vector database for better performance (optional)
4. **More Personalities**: Add new AI personalities

Your app is now live and completely free! 🎉 