from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import logging
import numpy as np
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LTR Tool Relevance API",
    description="Learning to Rank service for predicting tool relevance based on user queries",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Pydantic models
class Tool(BaseModel):
    name: str
    description: str

class PredictionRequest(BaseModel):
    query: str
    available_tools: List[Tool]

class ToolPrediction(BaseModel):
    tool_name: str
    relevance_score: float

class PredictionResponse(BaseModel):
    query: str
    predictions: List[ToolPrediction]
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# Simple ML model for tool relevance prediction
class SimpleRelevanceModel:
    def __init__(self):
        # Keywords that increase relevance scores
        self.keyword_weights = {
            'search': 0.8,
            'find': 0.7,
            'get': 0.6,
            'accommodation': 0.9,
            'hotel': 0.8,
            'rental': 0.8,
            'weather': 0.9,
            'forecast': 0.8,
            'flight': 0.9,
            'book': 0.7,
            'reserve': 0.7,
            'location': 0.6,
            'place': 0.6,
            'city': 0.6
        }
    
    def predict_relevance(self, query: str, tool_description: str) -> float:
        """Predict relevance score between query and tool"""
        query_lower = query.lower()
        desc_lower = tool_description.lower()
        
        # Base score
        score = 0.3
        
        # Keyword matching
        for keyword, weight in self.keyword_weights.items():
            if keyword in query_lower and keyword in desc_lower:
                score += weight * 0.3
            elif keyword in query_lower or keyword in desc_lower:
                score += weight * 0.1
        
        # Word overlap scoring
        query_words = set(query_lower.split())
        desc_words = set(desc_lower.split())
        
        if query_words and desc_words:
            overlap = len(query_words.intersection(desc_words))
            total_words = len(query_words.union(desc_words))
            overlap_score = overlap / total_words if total_words > 0 else 0
            score += overlap_score * 0.4
        
        # Normalize score to [0, 1]
        return min(max(score, 0.0), 1.0)

# Initialize model
model = SimpleRelevanceModel()

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "LTR Tool Relevance API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_tool_relevance(request: PredictionRequest):
    """Predict tool relevance for a given query"""
    try:
        predictions = []
        
        for tool in request.available_tools:
            relevance_score = model.predict_relevance(
                request.query, 
                tool.description
            )
            
            predictions.append(ToolPrediction(
                tool_name=tool.name,
                relevance_score=relevance_score
            ))
        
        # Sort by relevance score (descending)
        predictions.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return PredictionResponse(
            query=request.query,
            predictions=predictions,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/tools/example")
async def get_example_tools():
    """Get example tools for testing"""
    return {
        "example_tools": [
            {
                "name": "search_accommodations",
                "description": "Search for vacation rentals and accommodations"
            },
            {
                "name": "weather_forecast",
                "description": "Get weather information and forecasts"
            },
            {
                "name": "flight_booking",
                "description": "Search and book flights"
            },
            {
                "name": "restaurant_finder",
                "description": "Find restaurants and make reservations"
            }
        ]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
