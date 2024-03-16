import datetime
import random
from AppOpener import open as op
import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import openai
from config import apikey
import time

chat_response = ''

news_api_key = apikey

print("Desktop Assistant Samantha")
def chat(prompt):
    global chat_response
    openai.api_key = apikey
    chat_response += f"Parzival: {prompt}\n Samantha: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chat_response,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    try:
        say(response['choices'][0]['text'])
        chat_response += f"{response['choices'][0]['text']}\n"
        return response['choices'][0]['text']

    except Exception as e:
        return "There has occurred some error..."



def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for prompt: {prompt}\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    try:
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        print(response['choices'][0]["text"])
        text += response['choices'][0]["text"]
        with open(f"Openai/{''.join(prompt.lower().split('Samantha'))[1:60].strip()}.txt", 'w+') as f:
            f.write(text)

    except Exception as e:
        return "There has occurred some error..."

    return response['choices'][0]["text"]

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occured..."


say("Hello I am Samantha")
while True:
    print("Listening...")
    query = takeCommand()
    
    #say(text)

    if 'the time' in query.lower():
        strftime = datetime.datetime.now().strftime("%H:%M:%S")
        say(f"The time is {strftime}")

    # adding open AI features

    elif "AI Samantha ".lower() in query.lower():
        response = ai(prompt=query)
        say(response)

    elif "Samantha Quit".lower() in query.lower():
        exit()

    elif "reset chat".lower() in query.lower():
        chat_response += ''
    else:
        print("Chatting...")
        chat(query)