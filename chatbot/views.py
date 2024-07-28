import os
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from openai import OpenAI

# Instantiate the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Load policies JSON
with open('chatbot/policies.json') as f:
    policies = json.load(f)

def find_policy_details(query):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that helps answer questions about university policies."},
            {"role": "user", "content": f"You are to respond to the following query '{query}' using the json provided: {json.dumps(policies)}"}
        ],
        max_tokens=150
    )
    return completion.choices[0].message.content.strip()

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            
            response_message = find_policy_details(user_message)
            return JsonResponse({'response': response_message})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def chatbot_page(request):
    return render(request, 'chatbot.html')

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        try:
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
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request method.')
