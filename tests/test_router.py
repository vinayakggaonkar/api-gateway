# test_router.py - Tests for AI intent classification and routing
from gateway.router import MCPRouter

class TestRouter:

    def setup_method(self):
        self.router = MCPRouter()
    def test_finance_intent(self):
        intent, confidence = self.router.classify_intent("What is the stock price of Apple?")
        assert intent == "finance"
        assert confidence > 0
    def test_weather_intent(self):
        intent, confidence = self.router.classify_intent("What is the weather in Mysuru?")
        assert intent == "weather"
        assert confidence > 0
    def test_health_intent(self):
        intent, confidence = self.router.classify_intent("I have a headache and fever")
        assert intent == "health"
        assert confidence > 0
    def test_general_intent(self):
        intent, confidence = self.router.classify_intent("asdfghjkl")
        assert intent == "general"
        assert confidence == 0.5
    def test_route_returns_correct_service(self):
        decision = self.router.route("Bitcoin price today")
        assert decision.intent == "finance"
        assert decision.service_name == "finance-service"
        assert decision.target_url == "http://localhost:9001"
        assert decision.service_id == 1