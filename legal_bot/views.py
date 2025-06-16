from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
from .services import LegalBotService, DeepSeekScoringService
from .models import ChatHistory, ScoringHistory
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.


class LegalBotView(TemplateView):
    template_name = "legal_bot/index.html"


class AskQuestionView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot_service = LegalBotService()

    def post(self, request, *args, **kwargs):
        try:
            question = request.POST.get("question")
            response = self.bot_service.get_answer(question)

            # Save chat history
            ChatHistory.objects.create(question=question, answer=response)

            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class DeepSeekScoringView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scoring_service = DeepSeekScoringService()

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            query = data.get('query')
            response_1 = data.get('response_1')
            response_2 = data.get('response_2')
            response_3 = data.get('response_3')
            
            result = self.scoring_service.score_responses(
                query=query,
                response_1=response_1,
                response_2=response_2,
                response_3=response_3
            )

            # Save the scoring result to the database
            ScoringHistory.objects.create(
                query=query,
                response_1=response_1,
                response_2=response_2,
                response_3=response_3,
                scoring_result=result
            )

            return JsonResponse({"deepseek_scoring": result})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
