import datetime
import wikipedia
import webbrowser
import pywhatkit
import requests
import pyjokes
import wolframalpha
import json
import random
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
import difflib

def home(request):
    return render(request, 'home.html')

GREETINGS = [
    "Hi there! How can I help you today?",
    "Hello! What can I assist you with?",
    "Hey! What's on your mind?",
    "Greetings! How may I be of service?",
    "Hi! I'm your virtual assistant. What brings you here today?"
]

SMALL_TALK_RESPONSES = [
    "The weather has been quite interesting lately. Have you been enjoying it?",
    "Did you know that octopuses have three hearts and blue blood? Nature is fascinating!",
    "I was just thinking about how technology changes so quickly. Remember flip phones?",
    "Sometimes I wonder if coffee tastes better in the morning because we need it more.",
    "Fun fact: honey never spoils. Archaeologists have found 3,000-year-old honey that's still edible!"
]

QUESTIONS = [
    "What's the most interesting thing you've learned recently?",
    "If you could travel anywhere tomorrow, where would you go?",
    "Do you prefer coffee or tea? It seems to divide people more than you'd expect!",
    "What book or movie has influenced you the most?",
    "If you could master any skill overnight, what would it be?"
]

IDLE_MESSAGES = [
    "Just checking in. Is there anything I can help you with?",
    "I'm here if you need anything!",
    "Anything on your mind? I'm all ears... well, metaphorically speaking.",
    "Need some assistance or just want to chat? I'm here.",
    "If you have any questions or just want to talk, I'm ready!"
]

@csrf_exempt
def process_command(request):
    if request.method == 'POST':
        try:
           
            data = json.loads(request.body)
            command = data.get('command', '').lower()
            
        
            if is_greeting(command):
              return JsonResponse({'response': random.choice(GREETINGS)})
                
        
            if any(word in command for word in ['random talk', 'talk to me', 'say something', 'random', 'chat']):
                response_type = random.choice(['small_talk', 'question'])
                if response_type == 'small_talk':
                    return JsonResponse({'response': random.choice(SMALL_TALK_RESPONSES)})
                else:
                    return JsonResponse({'response': random.choice(QUESTIONS)})
            

            if 'time' in command:
                time = datetime.datetime.now().strftime('%H:%M:%S')
                response = f"The current time is {time}"

            elif 'date' in command:
                date = datetime.datetime.now().strftime('%B %d, %Y')
                response = f"Today is {date}"

            elif 'who is' in command or 'what is' in command:
                try:
                    query = command.replace('who is', '').replace('what is', '').strip()
                    response = wikipedia.summary(query, sentences=2)
                except wikipedia.exceptions.DisambiguationError as e:
                    response = f"There are multiple results for '{query}'. Please be more specific."
                except wikipedia.exceptions.PageError:
                    response = f"I couldn't find any information about '{query}'."
                except Exception as e:
                    response = f"Error retrieving information: {str(e)}"

            elif 'search' in command:
                query = command.replace('search', '').strip()
                try:
                    pywhatkit.search(query)
                    response = f"Searching for '{query}' on the web."
                except Exception as e:
                    response = f"Error searching: {str(e)}"

            elif 'play' in command:
                song = command.replace('play', '').strip()
                try:
                    pywhatkit.playonyt(song)
                    response = f"Playing '{song}' on YouTube."
                except Exception as e:
                    response = f"Error playing: {str(e)}"

            elif 'joke' in command:
                try:
                    response = pyjokes.get_joke()
                except Exception as e:
                    response = "I couldn't think of a joke right now."

            
            elif 'open youtube' in command:
                webbrowser.open_new_tab("https://www.youtube.com")
                response = "Opening YouTube in a new tab."

            elif 'open google' in command:
                webbrowser.open_new_tab("https://www.google.com")
                response = "Opening Google in a new tab."

            elif 'thank' in command:
                response = "You're welcome! Is there anything else I can help you with?"

            elif 'weather' in command:
              
                response = "I'd need to connect to a weather service to provide that information."

            elif 'exit' in command or 'quit' in command or 'bye' in command:
                response = "Thanks for chatting! Feel free to type something when you need assistance again."
                
           
            elif command.strip() == "":
                response = random.choice(IDLE_MESSAGES)
                
            else:
                response = "I'm not sure how to help with that. Try asking something like 'What time is it?' or 'Tell me a joke'."

        except json.JSONDecodeError:
            response = "Invalid request format. Please send a proper JSON object."
        except Exception as e:
            response = f"An error occurred: {str(e)}"
            
        return JsonResponse({'response': response})

    return render(request, 'index.html')

 
def get_random_conversation():
    category = random.choice(['greeting', 'small_talk', 'question'])
    if category == 'greeting':
        return random.choice(GREETINGS)
    elif category == 'small_talk':
        return random.choice(SMALL_TALK_RESPONSES)
    else:
        return random.choice(QUESTIONS)
    
def is_greeting(command):
    greetings = ['hi', 'hello', 'hey']
    match = difflib.get_close_matches(command, greetings, n=1, cutoff=0.5)
    return bool(match)