# router.py - AI brain that classifies intent and routes to correct service
from gateway.models import RouteDecision

# keyword dictionary:
INTENT_KEYWORDS = {
    "finance": [
        "stock", "price", "market", "crypto", "bitcoin",
        "investment", "trade", "dividend", "currency",
        "equity", "bond", "fund", "share", "profit",
        "revenue", "earnings", "financial"
    ],
    "weather": [
        "weather", "temperature", "forecast", "rain", "sunny",
        "humidity", "wind", "storm", "snow", "climate",
        "hot", "cold", "warm", "monsoon", "fog"
    ],
    "health": [
        "health", "symptom", "disease", "medicine", "doctor",
        "hospital", "treatment", "diagnosis", "pain", "fever",
        "headache", "blood pressure", "diabetes", "drug",
        "prescription", "vitamin", "diet", "nutrition"
    ],
    "search": [
        "search", "find", "look up", "retrieve",
        "get me", "show me", "fetch", "list",
        "who is", "where is", "how to"
    ],
    "general": []
}

# service registry:
SERVICE_REGISTRY = {
    "finance": {
        "name": "finance-service",
        "base_url": "http://localhost:9001",
        "service_id": 1
    },
    "weather": {
        "name": "weather-service",
        "base_url": "http://localhost:9002",
        "service_id": 2
    },
    "health": {
        "name": "health-service",
        "base_url": "http://localhost:9003",
        "service_id": 3
    },
    "search": {
        "name": "search-service",
        "base_url": "http://localhost:9004",
        "service_id": 4
    },
    "general": {
        "name": "general-service",
        "base_url": "http://localhost:9005",
        "service_id": 5
    },
}

# router class:
class MCPRouter:
    def classify_intent(self, query:str):
        query_lower = query.lower()
        scores = {}
        PRIORITY = {
            "finance": 2.5,
            "weather": 2.5,
            "health": 2.5,
            "search": 1.0,
        }
        for intent, keywords in INTENT_KEYWORDS.items():
            if intent == "general":
                continue
            hits = sum(1 for kw in keywords if kw in query_lower)
            if hits > 0:
                weight = PRIORITY.get(intent, 1.0)
                scores[intent] = (hits / max(len(keywords), 1)) * weight
        if not scores:
            return "general", 0.5
        best_intent = max(scores,key=lambda k:scores[k])
        confidence = min(1.0, scores[best_intent] * 10)
        return best_intent, round(confidence, 2)
    
    def route(self, query:str) -> RouteDecision:
        intent, confidence = self.classify_intent(query)
        service = SERVICE_REGISTRY.get(intent, SERVICE_REGISTRY["general"])
        return RouteDecision(
            intent = intent,
            confidence=confidence,
            target_url=service["base_url"],
            service_name=service["name"],
            service_id=service["service_id"]
        )
    
    def get_mock_response(self, intent: str, query: str) -> str:
        responses = {
            "finance": f"📈 Financial data for: '{query}'\n• Market is OPEN\n• S&P 500: 5,234.18 (+0.42%)\n• Processed by Finance Service.",
            "weather": f"🌤️ Weather for: '{query}'\n• Current: 28°C, Partly Cloudy\n• Humidity: 65%\n• Processed by Weather Service.",
            "health": f"🏥 Health info for: '{query}'\n• Processed by Health Service.\n• Always consult a doctor.",
            "search": f"🔍 Search results for: '{query}'\n• Result 1: Most relevant article\n• Result 2: Secondary reference\n• Processed by Search Service.",
            "general": f"💬 General response for: '{query}'\n• Processed by General Service.",
        }
        return responses.get(intent, responses["general"])
    
mcp_router = MCPRouter()