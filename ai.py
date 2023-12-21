import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

import openai

openai.api_key = OPENAI_KEY


# Function to convert text to speech
def SpeakText(command):
    # Initializing the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


r = sr.Recognizer()


def record_text():
    # Loop in case of error
    while True:
        try:
            # Using microphone as source of input
            with sr.Microphone() as source2:
                # Prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)

                print("I'm Listening")

                # Listens for the user input
                audio2 = r.listen(source2)

                # Using Google to recognize audio
                MyText = r.recognize_google(audio2)

                return MyText

        except sr.RequestError as e:
            print("Could not request result; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occurred")


def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message


print("Jarvis at your service")
SpeakText("Jarvis at your service")
messages = [{"role": "system", "content": "Please !! Act Like Jarvis from Iron Man."}]
activate_chat = False
while True:
    text = record_text()
    if "AI" in text.upper():
        activate_chat = True
        print("AI mode activated.")
        SpeakText("AI mode activated.")
        messages.append({"role": "user", "content": text})
        continue
    elif "DEACTIVATE" in text.upper():
        activate_chat = False
        print("AI mode deactivated.")
        SpeakText("AI mode deactivated.")
        messages.append({"role": "user", "content": text})
        continue
    if activate_chat:
        messages.append({"role": "user", "content": text})
        response = send_to_chatGPT(messages)
        SpeakText(response)
        print(response)
    elif "the time" in text.lower():
        hour = datetime.datetime.now().strftime("%I")
        min = datetime.datetime.now().strftime("%M %p")
        print(f"Sir, the time is {hour} : {min} ")
        SpeakText(f"Sir, the time is {hour} : {min} ")

    elif "thank you for your service" in text.lower():
        SpeakText("You're welcome! Goodbye.")
        break
    else:
        print("Listening...")
        SpeakText("I'm Listening")
