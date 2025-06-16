from django.test import TestCase
from django.urls import reverse
import json
from ..services import DeepSeekScoringService

class DeepSeekAPITest(TestCase):
    def setUp(self):
        self.test_data = {
            "query": "What are the legal requirements for starting a business in Ghana?",
            "response_1": "To start a business in Ghana, you need to register with the Registrar General's Department. The process includes business name registration, tax registration, and obtaining necessary permits.",
            "response_2": "Business registration in Ghana requires submitting forms to the RGD, getting a TIN, and paying registration fees. The Companies Act 2019 (Act 992) governs this process.",
            "response_3": "According to Ghanaian law, business registration involves: 1) Name search and reservation, 2) Company registration with RGD, 3) Tax registration with GRA, 4) SSNIT registration if you'll have employees."
        }
        
    def test_deepseek_scoring_api(self):
        """Test the DeepSeek scoring API endpoint"""
        url = reverse('deepseek_score')
        response = self.client.post(
            url,
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('deepseek_scoring', data)
        
        # Check if the response contains expected scoring criteria
        scoring = data['deepseek_scoring']
        expected_criteria = [
            'Factual Correctness',
            'Relevance',
            'Completeness',
            'Clarity',
            'Jurisdiction Awareness',
            'Caution/Disclaimer'
        ]
        
        for criterion in expected_criteria:
            self.assertIn(criterion, scoring)
            
    def test_deepseek_service_directly(self):
        """Test the DeepSeekScoringService directly"""
        try:
            service = DeepSeekScoringService()
            result = service.score_responses(
                self.test_data['query'],
                self.test_data['response_1'],
                self.test_data['response_2'],
                self.test_data['response_3']
            )
            
            # Verify that the result is a non-empty string
            self.assertIsInstance(result, str)
            self.assertTrue(len(result) > 0)
            
            # Check if all responses are scored
            self.assertIn("Response 1:", result)
            self.assertIn("Response 2:", result)
            self.assertIn("Response 3:", result)
            
        except Exception as e:
            self.fail(f"DeepSeekScoringService raised an exception: {str(e)}")