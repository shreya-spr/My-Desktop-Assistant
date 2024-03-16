import pyttsx3
from decouple import config
from datetime import datetime

import speech_recognition as sr
from random import choice
from utils import opening_text

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

# To check if text to speech is working
# engine = pyttsx3.init()
# engine.say("Hello I am Samantha from her.")
# engine.runAndWait() 

engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female) 0 -> male, 1 -> female
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""
    print(f"IN speak: {text}")
    engine.say(text)
    engine.runAndWait()

# speak("Hello , how you doin") 

# Greet the user
def greet_user():
    """Greets the user according to the time"""
    print("in greeeting")
    print(datetime.now())

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")

# greet_user() 

# Takes Input from User
def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            # The user hasn said 'stop' or 'exit' so end the conversation
            if 21 <= hour < 6:
                speak(f"Good night {USERNAME}, take care!")
            else:
                speak('Have a good day!')
            exit()
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query


import requests
from functions.online_ops import get_latest_news, get_random_advice, get_random_joke, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notion
from pprint import pprint

if __name__ == '__main__':
    print("in main")
    greet_user()
    while True:
        query = take_user_input().lower()
        print(query)

        if 'open notion' in query:
            open_notion()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'wikipedia' in query:
            speak('Anything specific you want to search on Wikipedia?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen too.")
            print(results)

        elif 'youtube' in query:
            speak('What do you want to play on Youtube?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            speak('What do you want to search on Google,  Parzival?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "send whatsapp message" in query:
            speak('On what number should I send the message  ? Please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message.")

        elif "send an email" in query:
            speak("On what email address do I send? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject?")
            subject = take_user_input().capitalize()
            speak("What is the message?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("I've sent the email.")
            else:
                speak("Something went wrong while I was sending the mail. Please check the error logs.")

        elif 'joke' in query:
            speak(f"Hope you like this one 👀")
            joke = get_random_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen.")
            pprint(joke)

        elif "advice" in query:
            speak(f"Here's an advice for you, Parzival")
            advice = get_random_advice()
            speak(advice)
            speak("For your convenience, I am printing it on the screen.")
            pprint(advice)

        elif 'news' in query:
            speak(f"I'm reading out the latest news headlines, Parzival")
            speak(get_latest_news())
            speak("For your convenience, I am printing it on the screen.")
            print(*get_latest_news(), sep='\n')


