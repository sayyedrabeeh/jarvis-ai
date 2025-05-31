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
from difflib import get_close_matches




try:
    import pywhatkit
    PYWHATKIT_AVAILABLE = True
except Exception as e:
    print("pywhatkit not available:", e)
    PYWHATKIT_AVAILABLE = False

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
                
        
            if any(phrase in command for phrase in [
               'random talk', 'talk to me', 'say something', 'random', 'chat', 
               'tell me something', 'tell something', 'tell me anything', 'something interesting', 
               'talk something', 'speak to me', 'anything to say'
           ]):
               response_type = random.choice(['small_talk', 'question'])
               if response_type == 'small_talk':
                   return JsonResponse({'response': random.choice(SMALL_TALK_RESPONSES)})
               else:
                   return JsonResponse({'response': random.choice(QUESTIONS)})
           
            question_phrases = ['who is', 'what is', "who's", "what's", 'whats', 'whos']
            words = command.split()
            if len(words) >= 2:
                phrase_candidate = words[0] + ' ' + words[1]
                matched = next((phrase for phrase in question_phrases if phrase in get_close_matches(phrase_candidate, question_phrases, n=1, cutoff=0.6)), None)
            else:
                matched = None

            if 'time' in command:
                time = datetime.datetime.now().strftime('%H:%M:%S')
                response = f"The current time is {time}"

            elif 'date' in command:
                date = datetime.datetime.now().strftime('%B %d, %Y')
                response = f"Today is {date}"
           
            elif matched:
                try:
                    query = command.replace(matched, '').strip()
                    response = wikipedia.summary(query, sentences=3)
                except wikipedia.exceptions.DisambiguationError as e:
                    response = f"There are multiple results for '{query}'. Please be more specific."
                except wikipedia.exceptions.PageError:
                    response = f"I couldn't find any information about '{query}'."
                except Exception as e:
                    response = f"Error retrieving information: {str(e)}"

            elif any(difflib.get_close_matches(word, ['search'], cutoff=0.8) for word in command.split()):
                try:
                  possible_words = command.split()
                  search_keyword = difflib.get_close_matches("search", possible_words, n=1, cutoff=0.8)
                  if search_keyword:
                     query = command.replace(search_keyword[0], '').strip()
                  else:
                     query = command.strip()
         
                  
                  if PYWHATKIT_AVAILABLE:
                    pywhatkit.search(query)
                  else:
                    webbrowser.open(f"https://www.google.com/search?q={query}")
                    response = f"Searching for '{query}' on the web."
                except Exception as e:
                      response = f"Error searching: {str(e)}"

          

 
            elif any(difflib.get_close_matches(word, ['play'], cutoff=0.75) for word in command.split()):
                try:
                    words = command.lower().split()
                    play_word = difflib.get_close_matches("play", words, n=1, cutoff=0.75)
                    if not play_word:
                        response = "It looks like you're trying to play something, but I couldn't understand the command. Try 'play <song name>'."
                        return JsonResponse({'response': response})
                    command = command.replace(play_word[0], '', 1).strip()
                    platforms = {
                        "youtube": ["youtube", "utub", "youtub", "you tube"],
                        "spotify": ["spotify", "spotfy", "spootify", "spotifi"],
                        "jiosaavn": ["jiosaavn", "saavn", "jio saavan", "saavan"],
                        "soundcloud": ["soundcloud", "sound cloudd", "sndcld"],
                        "gaana": ["gaana", "ganaa", "gana"]
                    }
                    platform = "youtube"  
                    for p_key, p_aliases in platforms.items():
                        for word in words:
                            match = difflib.get_close_matches(word, p_aliases, n=1, cutoff=0.75)
                            if match:
                                platform = p_key
                                break
                    for aliases in platforms.values():
                        for alias in aliases:
                            command = command.replace(alias, '').strip()
                    command = ' '.join([word for word in command.split() if word not in ['on', 'in', 'by']])
                    song = command.strip()
                    if not song:
                        response = "Please mention the song you want to play."
                        return JsonResponse({'response': response})
                    if platform == "spotify":
                        webbrowser.open_new_tab(f"https://open.spotify.com/search/{song}")
                        response = f"Opening '{song}' on Spotify."
                    elif platform == "soundcloud":
                        webbrowser.open_new_tab(f"https://soundcloud.com/search?q={song}")
                        response = f"Opening '{song}' on SoundCloud."
                    elif platform == "gaana":
                        webbrowser.open_new_tab(f"https://gaana.com/search/{song}")
                        response = f"Opening '{song}' on Gaana."
                    else:
                        try:
                                if PYWHATKIT_AVAILABLE:
                                   pywhatkit.playonyt(song)
                                else:
                                   webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
                                response = f"Playing '{song}' on YouTube."
                        except Exception as e:
                               response = f"Error playing song: {str(e)}"
                except Exception as e:
                    response = f"Error playing song: {str(e)}"
            

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
            
            elif 'open facebook' in command:
                webbrowser.open_new_tab("https://www.facebook.com")
                response = "Opening Facebook in a new tab."
            
            elif 'open twitter' in command:
                webbrowser.open_new_tab("https://www.twitter.com")
                response = "Opening Twitter in a new tab."
            
            elif 'open instagram' in command:
                webbrowser.open_new_tab("https://www.instagram.com")
                response = "Opening Instagram in a new tab."
            
            elif 'open linkedin' in command:
                webbrowser.open_new_tab("https://www.linkedin.com")
                response = "Opening LinkedIn in a new tab."
            
            elif 'open github' in command:
                webbrowser.open_new_tab("https://www.github.com")
                response = "Opening GitHub in a new tab."
            
            elif 'open reddit' in command:
                webbrowser.open_new_tab("https://www.reddit.com")
                response = "Opening Reddit in a new tab."
            
            elif 'open stackoverflow' in command:
                webbrowser.open_new_tab("https://www.stackoverflow.com")
                response = "Opening Stack Overflow in a new tab."
            
            elif 'open pinterest' in command:
                webbrowser.open_new_tab("https://www.pinterest.com")
                response = "Opening Pinterest in a new tab."
            
            elif 'open quora' in command:
                webbrowser.open_new_tab("https://www.quora.com")
                response = "Opening Quora in a new tab."
            
            elif 'open wikipedia' in command:
                webbrowser.open_new_tab("https://www.wikipedia.org")
                response = "Opening Wikipedia in a new tab."
            
            elif 'open spotify' in command:
                webbrowser.open_new_tab("https://www.spotify.com")
                response = "Opening Spotify in a new tab."
            
            elif 'open netflix' in command:
                webbrowser.open_new_tab("https://www.netflix.com")
                response = "Opening Netflix in a new tab."
            
            elif 'open amazon' in command:
                webbrowser.open_new_tab("https://www.amazon.com")
                response = "Opening Amazon in a new tab."
            
            elif 'open imdb' in command:
                webbrowser.open_new_tab("https://www.imdb.com")
                response = "Opening IMDb in a new tab."
            
            elif 'open weather' in command:
                webbrowser.open_new_tab("https://www.weather.com")
                response = "Opening Weather.com in a new tab."
            
            elif 'open news' in command:
                webbrowser.open_new_tab("https://www.bbc.com/news")
                response = "Opening the news page in a new tab."
            
            elif 'open cnn' in command:
                webbrowser.open_new_tab("https://www.cnn.com")
                response = "Opening CNN in a new tab."
            
            elif 'open reddit' in command:
                webbrowser.open_new_tab("https://www.reddit.com")
                response = "Opening Reddit in a new tab."
            
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