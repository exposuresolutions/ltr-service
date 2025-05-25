# Render Free Deployment Instructions

## Option 1: Web Interface (Recommended)
1. Go to https://render.com
2. Sign up/login with GitHub
3. Click "New" → "Web Service"
4. Connect GitHub account
5. Select repository: `exposuresolutions/ltr-service`
6. Configure:
   - **Name**: ltr-service
   - **Environment**: Docker
   - **Plan**: Free
   - **Build Command**: (leave empty)
   - **Start Command**: `uvicorn tool_relevance_api:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/health`
   - **Auto Deploy**: Yes

## Option 2: Render Blueprint (render.yaml)
The render.yaml file in this repo will automatically configure the service.

## Free Tier Limits
- 750 hours/month of runtime
- Sleeps after 15 minutes of inactivity
- 0.1 CPU, 512 MB RAM
- Public repositories only
- Custom domains supported

## Expected Deployment Time
- Build: 3-5 minutes
- Deploy: 1-2 minutes
- Total: ~5-7 minutes

## Post-Deployment Testing
Once deployed, test with:
```bash
curl https://your-app-name.onrender.com/health
curl -X POST https://your-app-name.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"query": "Find files in project", "tools": ["file_search", "semantic_search"]}'
```
