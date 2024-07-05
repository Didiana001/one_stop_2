

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import openai

openai.api_key = 'sk-proj-LcxuEINy1XgPpZiFT9CDT3BlbkFJyHMQCP5TTJzq2Yify2gI'

with open('chatbot/policies.json') as f:
    policies = json.load(f)

def find_policy_details(query):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Find the relevant policy details for the following query: '{query}'\n\n{json.dumps(policies)}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        response_message = find_policy_details(user_message)
        return JsonResponse({'response': response_message})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def chatbot_page(request):
    return render(request, 'chatbot.html')


@csrf_exempt


def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        if user_message:
            response_message = f"Hello! Welcome to onstop ."
        else:
            response_message = "Hello! How can I assist you today?"
        return JsonResponse({'response': response_message})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
import json

def chatbot(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        message = received_json_data.get('message', '').strip().lower()

        if message == 'hello':
            response_data = {
                'message': 'Hello! How can I assist you today?'
            }
        else:
            response_data = {
                'message': f'Echo: {message}'
            }

        return JsonResponse(response_data)

    else:
        return HttpResponseBadRequest('This endpoint accepts only POST requests.')





