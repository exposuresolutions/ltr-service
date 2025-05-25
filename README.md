# LTR Service - Learning to Rank Tool Relevance Prediction

A FastAPI-based service that predicts tool relevance for user queries using machine learning.

## 🚀 Live Deployments

- **Railway**: [Auto-deployed from main branch]
- **Render**: [Auto-deployed via GitHub Actions]

## 🛠️ Features

- **FastAPI** REST API with automatic documentation
- **Machine Learning** tool relevance prediction
- **Docker** containerized deployment
- **Health checks** and monitoring endpoints
- **Swagger UI** for API exploration

## 📚 API Endpoints

- `GET /health` - Health check
- `POST /predict` - Tool relevance prediction
- `GET /docs` - Swagger UI documentation
- `GET /openapi.json` - OpenAPI specification

## 🧪 Test the API

```bash
# Health check
curl https://your-deployment-url/health

# Prediction example
curl -X POST "https://your-deployment-url/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find Airbnb homes in New York",
    "available_tools": [
      {
        "name": "search_accommodations",
        "description": "Search for vacation rentals and accommodations"
      }
    ]
  }'
```

## 🏗️ Development

```bash
# Run locally
docker build -t ltr-service .
docker run -p 8000:8000 ltr-service

# Or with docker-compose
docker-compose up
```

## 📦 Deployment

This service auto-deploys to:
- **Railway** on every push to main branch
- **Render** via GitHub Actions workflow

Both deployments use the same Docker image: `exposureai/ltr-service:latest`
