<h1 align="center">🤖 VI ASSISTANT</h1>

 
 ## VI ASSISTANT- Interactive Web Assistant


This project is  Django-powered virtual assistant web application that provides users with an intuitive conversational interface to perform various tasks, access information, and engage in natural dialogue.  integrated web services, VI  offers a seamless experience for users seeking information or assistance through simple conversation.
✅ No external APIs — built entirely using Python libraries like pywhatkit, wikipedia, pyjokes, and more.
No API keys, no complex setup — just pure Python functionality under the hood.

If you find this repository helpful or interesting, please consider giving it a star⭐ and Follow Me for cool Projects

### [⭐ **Star this project**](https://github.com/sayyedrabeeh/artist)
### [👤 **Follow Me**](https://github.com/sayyedrabeeh)

 


## Why Star This Repository?

- It helps others discover the project.
- It motivates the me to keep improving it.
- It supports open-source development!

## How to Contribute

If you want to contribute, feel free to fork the repository and submit a pull request. Also, don’t forget to star the repo!

Thanks for your support! ❤

 
### HOME 
![SmartChat Banner](/vihome%20.png)
#### VI assistant 
![SmartChat Banner](/vi1.png)

##  Features

###  Conversational Intelligence
- **Dynamic Greetings**: Responds with varied, friendly greetings to keep interactions fresh
- **Smart Small Talk**: Engages users with interesting facts and conversation starters
- **Thoughtful Questions**: Asks insightful questions to maintain engaging conversation
- **Idle Check-ins**: Periodically checks in if a user hasn't interacted in a while

###  Information Retrieval
- **Wikipedia Integration**: Answers factual "who is" and "what is" questions using Wikipedia's extensive knowledge base
- **Web Search**: Opens search results for user queries when requested
- **Time & Date**: Provides accurate time and date information on demand

### 🎵 Media & Entertainment
- **Multi-Platform Media Playback**: Intelligently routes media requests to:
  - YouTube
  - Spotify
  - SoundCloud
  - Gaana
 
- **Platform Detection**: Automatically detects which music platform the user wants to use
- **Humor**: Delivers jokes on request through pyjokes integration

###  Web Navigation
- **Quick Website Access**: Opens popular websites in new tabs including:
  - Social media (Facebook, Twitter, Instagram, LinkedIn)
  - Information (Google, Wikipedia, Stack Overflow, Quora)
  - Entertainment (YouTube, Netflix, Spotify)
  - Shopping (Amazon)
  - Utilities (GitHub, Weather, News)

##  Technology Stack

- **Backend**: Django web framework
- **Language**: Python 3.x
- **Libraries**:
  - `wikipedia`: Knowledge retrieval
  - `pywhatkit`: YouTube playback and web searches
  - `pyjokes`: Humor generation
  - `difflib`: Fuzzy text matching for better command recognition
  - `webbrowser`: Website navigation
  - `datetime`: Time and date functions
  - `google-generativeai` – AI-powered conversational chat (Gemini API)

## 📋 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/jarvis-ai.git
cd jarvis

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

##  Usage

1. Navigate to `http://localhost:8000` in your web browser
2. Type your request in the chat input field
3. Interact with SmartChat using natural language commands:

```
"What time is it?"
"Tell me about Albert Einstein"
"Play Bohemian Rhapsody on Spotify"
"Open GitHub"
"Tell me a joke"
```

##  How It Works

SmartChat processes user input through a command interpretation pipeline:

1. **Command Recognition**: Identifies request type using fuzzy matching
2. **Intent Analysis**: Determines user's intended action
3. **Service Routing**: Selects appropriate backend service
4. **Response Generation**: Creates natural language responses
5. **Action Execution**: Performs requested tasks

## 🔄 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the home page |
| `/process_command/` | POST | Processes user commands and returns responses |

 

##  License

This project is licensed under the MIT License - see the LICENSE file for details.

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

##  Acknowledgements

- Django community for the robust web framework
- Wikipedia API for knowledge access
- PyWhatKit for YouTube integration
- All open-source contributors whose libraries made this project possible

---

⭐ **Star this repo if you find it useful!** ⭐

<p align="center">Developed with ❤️ME for Poeples</p>

 
<h3 align="center">Happy Coding </h3>
 
