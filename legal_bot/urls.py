from django.urls import path
from .views import LegalBotView, AskQuestionView, DeepSeekScoringView

urlpatterns = [
    path("", LegalBotView.as_view(), name="legal_bot"),
    path("ask/", AskQuestionView.as_view(), name="ask_question"),
    path("deepseek-score/", DeepSeekScoringView.as_view(), name="deepseek_score"),
]
