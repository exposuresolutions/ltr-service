# 🛤️ Railway Optimized Free Deployment

## Strategy: Maximize Your $5 Monthly Credit

### Cost Optimization Settings
- **Sleep after**: 5 minutes of inactivity
- **Memory limit**: 512MB (minimum)
- **CPU limit**: 0.1 vCPU
- **Auto-scale**: Off
- **Replicas**: 1 (maximum)

## Deployment Steps

### Option 1: Web Interface (Recommended)
1. **Go to**: https://railway.app
2. **New Project** → **Deploy from GitHub**
3. **Select**: `exposuresolutions/ltr-service`
4. **Configure Environment Variables**:
   - `PORT`: 8000
   - `RAILWAY_STATIC_URL`: (Railway will set automatically)

### Option 2: Railway CLI
```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy from current directory
cd C:\Users\danga\ltr-service-github
railway up
```

## Optimized railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "uvicorn tool_relevance_api:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3,
    "sleepApplication": true,
    "sleepApplicationTimeout": 300
  },
  "environments": {
    "production": {
      "variables": {
        "RAILWAY_ENVIRONMENT": "production"
      }
    }
  }
}
```

## Cost Monitoring
- **Check usage**: Railway dashboard → Usage tab
- **Estimated cost**: ~$2-3/month with optimization
- **Budget alert**: Set up notifications at $4

## Expected Results
- **URL**: `https://ltr-service-production.up.railway.app`
- **Build Time**: 3-4 minutes (faster than Render)
- **Performance**: Better than free tiers (dedicated resources)

## Free Credit Maximization Tips
1. **Enable sleeping**: App sleeps after 5 minutes
2. **Monitor usage**: Check daily in dashboard
3. **Optimize Docker**: Use multi-stage builds
4. **Resource limits**: Set CPU/memory caps
5. **Development mode**: Use for testing only

## Pros
✅ Better performance than free tiers
✅ Faster deployments
✅ No sleeping limitations (if within budget)
✅ Excellent developer experience
✅ Built-in monitoring

## Cons
❌ Limited by $5 monthly credit
❌ Can exceed free tier if not monitored
❌ Requires credit card for verification

## Budget Breakdown (Estimated)
- **CPU**: ~$1.50/month (0.1 vCPU)
- **Memory**: ~$1.00/month (512MB)
- **Networking**: ~$0.50/month (minimal traffic)
- **Total**: ~$3/month (within $5 limit)
