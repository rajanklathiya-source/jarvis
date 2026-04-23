import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# Set voice: 0 for male (Jarvis), 1 for female (Friday)
engine.setProperty('voice', voices[0].id) 

def speak(audio):
    """Function to make the assistant speak"""
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    """Function to greet the user based on the time of day"""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning, sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon, sir!")   
    else:
        speak("Good Evening, sir!")  
    speak("I am Jarvis. Online and ready. How may I help you?")

try:
    import pyaudio
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False
    import sounddevice as sd
    import numpy as np

def take_command():
    """Takes microphone input from the user and returns string output"""
    r = sr.Recognizer()
    
    if HAS_PYAUDIO:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            r.adjust_for_ambient_noise(source, duration=1)  # Adjusts for 1 second to calibrate energy threshold
            print("Listening...")
            r.pause_threshold = 1  # 1 second of non-speaking audio before a phrase is considered complete
            r.energy_threshold = 300 # minimum audio energy to consider for recording
            audio = r.listen(source)
    else:
        print("PyAudio not found. Falling back to fixed-duration recording using sounddevice.")
        print("Listening (for 5 seconds)...")
        fs = 16000
        duration = 5  # seconds
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        audio = sr.AudioData(recording.tobytes(), fs, 2)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio. Say that again please...")  
        return "None"
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return "None"
    except Exception as e:
        print("Say that again please...")  
        return "None"
    return query

if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command().lower()

        # Logic for executing tasks based on voice query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak("I encountered an issue fetching that information.")

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("google.com")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
            print(f"Time: {strTime}")

        elif 'open code' in query or 'open vs code' in query:
            speak("Opening Visual Studio Code")
            # This path is usually right for VS Code on Windows, but might need adjustment
            code_path = os.getenv("LOCALAPPDATA") + "\\Programs\\Microsoft VS Code\\Code.exe"
            if os.path.exists(code_path):
                os.startfile(code_path)
            else:
                speak("I could not find the path to VS code.")

        elif 'quit' in query or 'exit' in query or 'sleep' in query:
            speak("Goodbye Sir. Shutting down systems.")
            break
