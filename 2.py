import subprocess
import pyttsx3
import json
import speech_recognition as sr
import datetime
import webbrowser
import os
import winshell
import pyjokes
import ctypes
import time
import requests
import fileinput
import getpass
import os
from pathlib import Path
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
import random

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Predefined responses for common questions
RESPONSES = {
    "greeting": [
        "Hello! How can I assist you today?",
        "Hi there! What can I help you with?",
        "Greetings! How may I help you?",
        "Hello! I'm here to help. What's on your mind?"
    ],
    "farewell": [
        "Goodbye! Have a great day!",
        "See you later! Take care!",
        "Bye! Come back if you need anything!",
        "Goodbye! It was nice talking to you!"
    ],
    "thanks": [
        "You're welcome!",
        "Happy to help!",
        "My pleasure!",
        "Anytime! Is there anything else you need?"
    ],
    "unknown": [
        "I'm not sure I understand. Could you please rephrase that?",
        "I didn't quite catch that. Could you say it differently?",
        "I'm still learning. Could you try asking that another way?",
        "I'm not sure how to answer that. Could you please rephrase your question?"
    ],
    "error": [
        "I'm having trouble understanding. Could you please repeat that?",
        "I didn't catch that. Could you speak a bit more clearly?",
        "I'm having trouble with my hearing. Could you try again?",
        "I'm not sure what you said. Could you repeat that?"
    ]
}

DIRECTORIES = {
    "HTML": [".html5", ".html", ".htm", ".xhtml"],
    "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
               ".heif", ".psd"],
    "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng",
               ".qt", ".mpg", ".mpeg", ".3gp", ".mkv"],
    "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                  "pptx"],
    "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
                 ".dmg", ".rar", ".xar", ".zip"],
    "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
              ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
    "PLAINTEXT": [".txt", ".in", ".out"],
    "PDF": [".pdf"],
    "PYTHON": [".py",".pyi"],
    "XML": [".xml"],
    "EXE": [".exe"],
    "SHELL": [".sh"]
}
FILE_FORMATS = {file_format: directory
                for directory, file_formats in DIRECTORIES.items()
                for file_format in file_formats}

def speak(audio):
    try:
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speech synthesis: {e}")

def get_random_response(response_type):
    return random.choice(RESPONSES.get(response_type, RESPONSES["unknown"]))

def countdown(n):
    while n > 0:
        print(n)
        n = n - 1
    if n == 0:
        print('BLAST OFF!')

def wishMe():
    try:
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            speak("Good Morning!")
        elif hour >= 12 and hour < 18:
            speak("Good Afternoon!")
        else:
            speak("Good Evening!")
        speak("I am your voice assistant. I'm here to help you with your questions.")
    except Exception as e:
        print(f"Error in wishMe: {e}")
        speak("Hello! I'm your voice assistant.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("No speech detected")
            return "None"

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        speak(get_random_response("error"))
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        speak("I'm having trouble connecting to the speech recognition service.")
        return "None"
    except Exception as e:
        print(f"Error in takeCommand: {e}")
        speak("I encountered an error. Please try again.")
        return "None"

def handle_question(query):
    # Basic greetings
    if any(word in query for word in ['hello', 'hi', 'hey']):
        return get_random_response("greeting")
    
    # Farewell
    elif any(word in query for word in ['bye', 'goodbye', 'exit', 'quit']):
        speak(get_random_response("farewell"))
        exit()
    
    # Gratitude
    elif any(word in query for word in ['thank', 'thanks']):
        return get_random_response("thanks")
    
    # Time related
    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        return f"The current time is {strTime}"
    
    # Jokes
    elif 'joke' in query or 'funny' in query or 'laugh' in query:
        try:
            return pyjokes.get_joke()
        except:
            return "Why don't scientists trust atoms? Because they make up everything!"
    
    # Personal questions
    elif 'your name' in query:
        return "My name is TARS."
    
    elif 'who made you' in query:
        return "Yogi Developed Me."
    
    elif 'who created you' in query:
        return "Yogi Created Me."
    
    elif 'who are you' in query:
        return "I Am just a voice assistant."
    
    elif 'what can you do' in query:
        return "I can just answer your questions."
    
    elif 'how do you work' in query:
        return "I Will be work by answering your questions."
    
    elif 'how do you function' in query:
        return "I will just answer your questions."
    
    # Philosophical questions
    elif 'what is love' in query:
        return "Love is a complex emotion that can mean different things to different people. It's often described as a deep affection, care, and connection between people."
    
    elif 'meaning of life' in query or 'purpose of life' in query:
        return "That's a profound philosophical question that has been debated for centuries. Different people and cultures have different perspectives on this. Some find meaning in relationships, others in purpose, and some in personal growth."
    
    # Technical questions
    elif 'what technologies do you use' in query:
        return "I use speech recognition to understand your voice, natural language processing to understand your questions, and text-to-speech synthesis to respond to you."
    
    elif 'how do you understand me' in query:
        return "I use speech recognition technology to convert your voice into text, and then process that text to understand your questions."
    
    elif 'how do you speak' in query:
        return "I use text-to-speech synthesis technology to convert my responses into spoken words."
    
    # Capability questions
    elif 'what are your features' in query:
        return "I can answer questions, tell jokes, tell time, and engage in conversation. I'm designed to be helpful and informative."
    
    elif 'what are your functions' in query:
        return "My main function is to answer your questions and engage in conversation. I can provide information, tell jokes, and tell time."
    
    elif 'how can you help me' in query:
        return "I can help you by answering your questions, providing information, telling jokes, and engaging in conversation. Just ask me anything!"
    
    # Default response for unknown queries
    else:
        return get_random_response("unknown")

if __name__ == '__main__':
    try:
        clear = lambda: os.system('cls')
        clear()
        wishMe()
        
        while True:
            query = takeCommand()
            if query != "None":
                response = handle_question(query)
                speak(response)
    except KeyboardInterrupt:
        speak("Goodbye! Have a great day!")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("I encountered an error. Please restart the program.")