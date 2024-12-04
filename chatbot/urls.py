from django.urls import path
from .views import chatbot_page, chatbot_response

urlpatterns = [
    path("", chatbot_page, name="chatbot_home"),  # Renders chat page
    path("chat/", chatbot_response, name="chatbot_response"),  # API endpoint for chatbot
]
