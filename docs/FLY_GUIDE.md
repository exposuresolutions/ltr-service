# 🚀 Fly.io Free Deployment Guide

## Prerequisites
```powershell
# Install Fly CLI
iwr https://fly.io/install.ps1 -useb | iex

# Login to Fly.io
fly auth login
```

## Deployment Steps

### Step 1: Initialize Fly App
```powershell
cd C:\Users\danga\ltr-service-github
fly launch --no-deploy --name ltr-service-fly
```

### Step 2: Configure fly.toml
The `fly.toml` file will be created automatically, but we'll optimize it for free tier.

### Step 3: Deploy
```powershell
fly deploy
```

## Free Tier Limits
- **3 shared-cpu-1x VMs** (256MB RAM each)
- **3GB persistent volume** storage
- **160GB bandwidth** per month
- **No credit card required** for free tier

## Expected Results
- **URL**: `https://ltr-service-fly.fly.dev`
- **Build Time**: 3-5 minutes
- **Global Edge**: Multiple regions available
- **Always On**: No sleeping (unlike Render)

## Fly.toml Configuration
```toml
app = "ltr-service-fly"
primary_region = "ord"

[build]

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256

[checks]
  [checks.health]
    grace_period = "10s"
    interval = "30s"
    method = "GET"
    path = "/health"
    port = 8000
    timeout = "5s"
```

## Pros
✅ No sleeping (better than Render for always-on)
✅ Global edge network
✅ Better performance than Render free
✅ Persistent volumes included
✅ Good documentation

## Cons
❌ More complex setup
❌ CLI-based deployment
❌ Smaller RAM (256MB vs Render's 512MB)
