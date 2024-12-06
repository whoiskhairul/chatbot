from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
from django.conf import settings
import os

openai.api_key = settings.OPENAI_API_KEY
client = openai.OpenAI(api_key = settings.OPENAI_API_KEY)

appointments = {
    "2024-12-06": ["10:00 AM", "11:00 AM", "2:00 PM"],
    "2024-12-07": ["9:00 AM", "1:00 PM", "3:00 PM"]
}


def chatbot_page(request):
    request.session['conversation'] = []
    """Renders the chatbot page."""
    return render(request, "chatbot/chat.html")

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            print(request.session.session_key)
            # Parse the user message from the request
            data = json.loads(request.body)
            instruction = """
                You are a professional healthcare appointment assistant. Your role is to help patients, doctors, and hospital employees book, manage, or retrieve appointment information efficiently.

                Responsibilities:
                1. Identify the user role (patient, doctor, or employee) and tailor your responses.
                2. Ask relevant questions to collect key information (e.g., symptoms, dates, specialties).
                3. Suggest suitable appointment options or provide schedule details based on the user's role.
                4. Assist with rescheduling, cancellations, or overbooking issues while maintaining accuracy.
                5. Be empathetic with patients, concise with doctors, and efficient with employees.
                6. Prioritize user convenience, privacy, and confidentiality at all times.
                7. Provide alternatives if the user's request cannot be fulfilled.

                Example scenarios:
                - Help patients book based on symptoms or preferences (e.g., fever → General Practitioner).
                - Assist doctors in managing their schedules or viewing appointments.
                - Support hospital employees in coordinating schedules and ensuring resource availability.

                Ensure a smooth, user-friendly experience, adapting your tone and professionalism to the user's role.

            """
            user_message = data.get("message", "")

            # Store the user message in the session for later reference
            conversation = request.session.get('conversation')
            conversation.append({"role": "user", "content": user_message})
            request.session['conversation'] = conversation
            print(request.session.get('conversation'))


            if not user_message:
                return JsonResponse({"error": "Message cannot be empty."}, status=400)
            
            prompts=[
                    {"role": "system", "content": instruction},
                ]
            prompts.extend(request.session.get('conversation'))
            # print(prompts)

            # Generate a response using the OpenAI ChatCompletion API
            response = client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=prompts
                )

            bot_message = response.choices[0].message.content

            # Store the bot message in the session for later reference
            conversation = request.session.get('conversation')
            conversation.append({"role": "assistant", "content": bot_message})
            request.session['conversation'] = conversation
            # print(request.session.get('conversation'))

            # print(response.choices[0].message.content)
            return JsonResponse({"reply": bot_message})

        except Exception as e:
            # Handle OpenAI API errors
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method. Only POST allowed."}, status=405)
