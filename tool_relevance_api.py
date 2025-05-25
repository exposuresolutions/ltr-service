from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import logging
import numpy as np
from datetime import datetime
import os
import requests # Added for Abacus.ai integration

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

# Abacus.ai LTR Model
class AbacusLTRModel:
    def __init__(self):
        self.api_key = os.getenv("ABACUS_AI_API_KEY")
        self.model_id = os.getenv("ABACUS_MODEL_ID", "your-default-ltr-model-id") # Provide a default or ensure it's set
        self.base_url = os.getenv("ABACUS_API_BASE_URL", "https://api.abacus.ai/v1") # Allow overriding base URL

        if not self.api_key:
            logger.warning("ABACUS_AI_API_KEY not set. AbacusLTRModel may not function.")
        if self.model_id == "your-default-ltr-model-id":
            logger.warning("ABACUS_MODEL_ID not set or using default. Ensure this is configured for Abacus.ai.")

    def _simple_fallback(self, query: str, tool_description: str) -> float:
        """Fallback to a simple model if Abacus.ai fails or is not configured."""
        logger.warning("Abacus.ai prediction failed or not configured. Falling back to simple model.")
        # This uses an instance of the simple model for fallback
        # For simplicity, directly instantiating here. Consider a shared instance if performance is critical.
        simple_model_fallback = SimpleRelevanceModel()
        return simple_model_fallback.predict_relevance(query, tool_description)

    def predict_relevance(self, query: str, tool_description: str) -> float: # Matched signature
        """Predict relevance score using Abacus.ai API."""
        if not self.api_key or not self.model_id or self.model_id == "your-default-ltr-model-id":
            logger.warning("Abacus.ai API key or model ID not configured. Using fallback.")
            return self._simple_fallback(query, tool_description)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # The payload structure depends on your Abacus.ai model's expected input.
        # Assuming it takes 'query' and 'tool_description' as features.
        # Adjust this payload to match your Abacus.ai model's schema.
        payload = {
            "model_id": self.model_id,
            "deployment_token": os.getenv("ABACUS_DEPLOYMENT_TOKEN"), # If your model uses a deployment token
            "features": { # Common way to pass features
                "query_text": query,
                "tool_desc_text": tool_description
                # Add other features your Abacus.ai model expects
            }
        }
        # Remove deployment_token if not used by your Abacus model
        if not payload["deployment_token"]:
            del payload["deployment_token"]

        try:
            logger.info(f"Querying Abacus.ai model {self.model_id} at {self.base_url}/predictions")
            response = requests.post(
                f"{self.base_url}/predictions", # Common endpoint, verify with Abacus.ai docs
                json=payload,
                headers=headers,
                timeout=10  # Adding a timeout
            )
            response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)
            
            prediction_data = response.json()
            logger.info(f"Abacus.ai response: {prediction_data}")

            # Extract the relevance score. This path depends on your Abacus.ai model's output structure.
            # Example: prediction_data['predictions'][0]['label_scores']['relevant']
            # Or: prediction_data['predictions'][0]['score']
            # Please adjust this based on the actual response from your Abacus.ai model.
            # Assuming the score is directly available or under a 'relevance_score' key.
            relevance_score = prediction_data.get("relevance_score") # A placeholder
            if relevance_score is None: # Try a common structure
                 if "predictions" in prediction_data and isinstance(prediction_data["predictions"], list) and len(prediction_data["predictions"]) > 0:
                    if isinstance(prediction_data["predictions"][0], dict) and "score" in prediction_data["predictions"][0]:
                         relevance_score = prediction_data["predictions"][0]["score"]
                    elif isinstance(prediction_data["predictions"][0], dict) and "relevance_score" in prediction_data["predictions"][0]:
                         relevance_score = prediction_data["predictions"][0]["relevance_score"]


            if relevance_score is not None:
                return float(relevance_score)
            else:
                logger.error(f"Could not extract relevance score from Abacus.ai response: {prediction_data}")
                return self._simple_fallback(query, tool_description)

        except requests.exceptions.RequestException as e:
            logger.error(f"Abacus.ai request failed: {e}")
            return self._simple_fallback(query, tool_description)
        except Exception as e:
            logger.error(f"Error processing Abacus.ai response: {e}")
            return self._simple_fallback(query, tool_description)

# Initialize model based on environment variable
MODEL_TYPE = os.getenv("MODEL_TYPE", "simple").lower()

if MODEL_TYPE == "abacus_ai_pro":
    logger.info("Using Abacus.ai Pro LTR Model")
    model = AbacusLTRModel()
elif MODEL_TYPE == "simple":
    logger.info("Using Simple Relevance Model")
    model = SimpleRelevanceModel()
else:
    logger.warning(f"Unknown MODEL_TYPE '{MODEL_TYPE}'. Defaulting to Simple Relevance Model.")
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
