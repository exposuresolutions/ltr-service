# 🎯 Render Free Deployment Guide

## Quick Deploy Steps
1. **Go to**: https://render.com
2. **Sign up/Login** with GitHub
3. **New Web Service** → Connect GitHub → Select `exposuresolutions/ltr-service`
4. **Configure**:
   - Name: `ltr-service`
   - Environment: `Docker`
   - Plan: **FREE**
   - Branch: `main`
   - Build Command: (leave empty)
   - Start Command: `uvicorn tool_relevance_api:app --host 0.0.0.0 --port $PORT`
   - Health Check: `/health`
   - Auto Deploy: `Yes`

## Expected Results
- **URL**: `https://ltr-service-[random].onrender.com`
- **Build Time**: 5-7 minutes
- **Free Limits**: 750 hours/month, sleeps after 15min inactivity
- **Resources**: 0.1 CPU, 512MB RAM

## Test After Deployment
```bash
# Health check
curl https://your-app.onrender.com/health

# Prediction test
curl -X POST https://your-app.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"query": "Find files", "tools": ["file_search", "semantic_search"]}'
```

## Troubleshooting
- If build fails: Check Dockerfile syntax
- If health check fails: Ensure `/health` endpoint works
- If timeout: App might be sleeping (free tier limitation)

## Pros
✅ Completely free (no credit card needed)
✅ Custom domains supported
✅ Automatic HTTPS
✅ GitHub auto-deploy
✅ Docker support
✅ Reliable uptime

## Cons
❌ Sleeps after 15 minutes of inactivity
❌ Slower cold starts
❌ Limited to 512MB RAM
