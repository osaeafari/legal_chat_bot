from django.contrib import admin
from .models import ChatHistory, ScoringHistory

admin.site.register(ChatHistory)
admin.site.register(ScoringHistory)
