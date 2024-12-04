from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
from django.conf import settings

# openai.api_key = settings.OPENAI_API_KEY
client = openai.OpenAI(api_key = settings.OPENAI_API_KEY)

def chatbot_page(request):
    """Renders the chatbot page."""
    # print(openai.api_key)
    return render(request, "chatbot/chat.html")

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            # Parse the user message from the request
            data = json.loads(request.body)
            instruction = "Dont respond to any query that doesnt contain a question related to healthcare and smart bpmn \n"
            user_message = instruction + data.get("message", "")

            if not user_message:
                return JsonResponse({"error": "Message cannot be empty."}, status=400)

            # Generate a response using the OpenAI ChatCompletion API
            response = client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message},
                ],
                )  

            bot_message = response.choices[0].message.content
            # print(response.choices[0].message.content)
            return JsonResponse({"reply": bot_message})

        except openai.error.OpenAIError as e:
            # Handle OpenAI API errors
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method. Only POST allowed."}, status=405)
