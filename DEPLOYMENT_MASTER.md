# 🚀 LTR Service - Complete Free Deployment Guide

## 🎯 Three Free Deployment Options Ready!

Your LTR (Learning to Rank) service is configured for deployment on three different platforms, each optimized for different use cases.

## 📊 Comparison Table

| Platform | Cost | RAM | CPU | Sleep | Setup Time | Best For |
|----------|------|-----|-----|-------|------------|----------|
| **Render** | 100% Free | 512MB | 0.1 vCPU | 15min | 5 min | Production-ready free hosting |
| **Fly.io** | Free Tier | 256MB | Shared | Never | 10 min | Always-on service |
| **Railway** | $5 credit | 512MB | 0.1 vCPU | 5min* | 3 min | Best performance |

*Configurable sleep time

## 🎯 **Option 1: Render (RECOMMENDED for Free)**

**Why Choose Render:**
- Completely free forever
- No credit card required
- Automatic HTTPS & custom domains
- GitHub auto-deploy

**Deploy Now:**
1. Go to: https://render.com
2. Sign up with GitHub
3. New Web Service → Connect `exposuresolutions/ltr-service`
4. Use settings from `/docs/RENDER_GUIDE.md`

**Expected URL:** `https://ltr-service-[random].onrender.com`

---

## 🚀 **Option 2: Fly.io (Best Performance)**

**Why Choose Fly.io:**
- Never sleeps (always available)
- Global edge network
- Better performance than Render

**Deploy Now:**
```powershell
# Already installed: flyctl
cd C:\Users\danga\ltr-service-github
fly auth login
fly launch --no-deploy --name ltr-service-fly
fly deploy
```

**Expected URL:** `https://ltr-service-fly.fly.dev`

---

## 🛤️ **Option 3: Railway (Premium Experience)**

**Why Choose Railway:**
- Best developer experience
- Fastest deployments
- Advanced monitoring

**Deploy Now:**
```powershell
# Already installed: railway CLI
cd C:\Users\danga\ltr-service-github
railway login
railway up
```

**Expected URL:** `https://ltr-service-production.up.railway.app`

---

## 🧪 Testing Your Deployed Service

Once deployed, test with these commands (replace URL):

```bash
# Health check
curl https://your-deployed-url.com/health

# Tool relevance prediction
curl -X POST https://your-deployed-url.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find files in my project", 
    "tools": ["file_search", "semantic_search", "grep_search"]
  }'
```

**Expected Response:**
```json
{
  "query": "Find files in my project",
  "tool_relevance_scores": {
    "file_search": 0.92,
    "semantic_search": 0.78,
    "grep_search": 0.85
  },
  "recommended_tool": "file_search",
  "confidence": 0.92
}
```

## 🔧 Files Configured

✅ **Render**: `render.yaml` + `docs/RENDER_GUIDE.md`
✅ **Fly.io**: `fly.toml` + `docs/FLY_GUIDE.md`  
✅ **Railway**: `railway.json` + `docs/RAILWAY_OPTIMIZED.md`
✅ **GitHub Actions**: `.github/workflows/deploy-render.yml`
✅ **Docker**: `Dockerfile` + `docker-compose.yml`

## 🎉 Quick Start Recommendation

**For immediate free deployment:**
1. **Start with Render** (easiest, completely free)
2. **Backup with Fly.io** (better performance)
3. **Upgrade to Railway** (when you want premium features)

## 🔗 Useful Links

- **GitHub Repo**: https://github.com/exposuresolutions/ltr-service
- **Docker Image**: https://hub.docker.com/r/exposureai/ltr-service
- **Local Development**: `docker-compose up`

Choose your deployment platform and let's get your LTR service live! 🚀
