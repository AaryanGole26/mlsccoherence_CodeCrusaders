import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr
import requests
import json

WIT_ACCESS_TOKEN = "XZF3P3IDPPTU2YG5O6FUIU36E6654G77"

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speech_to_text():
    with sr.Microphone() as source:
        response_text.insert(tk.END, "Listening...\n", "bold")
        response_text.see(tk.END)
        root.update()
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        response_text.insert(tk.END, "Transcribing...\n", "bold")
        response_text.see(tk.END)
        root.update()
        text = recognizer.recognize_google(audio)
        response_text.insert(tk.END, f"You said: {text}\n", "normal")
        return text
    except sr.UnknownValueError:
        response_text.insert(tk.END, "Sorry, I couldn't understand what you said.\n", "normal")
        return ""
    except sr.RequestError as e:
        response_text.insert(tk.END, f"Speech recognition service error; {e}\n", "normal")
        return ""

def analyze_intent(text):
    headers = {"Authorization": f"Bearer {WIT_ACCESS_TOKEN}"}
    params = {"q": text}
    response = requests.get("https://api.wit.ai/message", headers=headers, params=params)
    data = response.json()
    intent = data['intents'][0]['name'] if data.get('intents') else "Unknown"
    return intent

def extract_information(intent):
    if intent == "warranty_claim":
        speak("Please provide your full name.")
        full_name = speech_to_text()
        speak("Please provide your contact information.")
        contact_info = speech_to_text()
        contact_info = ''.join(filter(str.isdigit, contact_info))  # Remove non-digit characters
        while not (len(contact_info) == 10):
            speak("Please provide a valid 10-digit phone number.")
            contact_info = speech_to_text()
            contact_info = ''.join(filter(str.isdigit, contact_info))  # Remove non-digit characters
        contact_info = int(contact_info)  # Convert to integer
        speak("Please provide your address.")
        address = speech_to_text()
        speak("Please describe the technical issue.")
        issue_details = speech_to_text()
        speak("What is your preferred date and time for technician visit?")
        preferred_time = speech_to_text()
    elif intent == "technical_issue":
        speak("Please provide your full name.")
        full_name = speech_to_text()
        speak("Please provide your contact information.")
        contact_info = speech_to_text()
        contact_info = ''.join(filter(str.isdigit, contact_info))  # Remove non-digit characters
        while not (len(contact_info) == 10):
            speak("Please provide a valid 10-digit phone number.")
            contact_info = speech_to_text()
            contact_info = ''.join(filter(str.isdigit, contact_info))  # Remove non-digit characters
        contact_info = int(contact_info)  # Convert to integer
        speak("Please provide your address.")
        address = speech_to_text()
        speak("Please describe the technical issue.")
        issue_details = speech_to_text()
        speak("What is your preferred date and time for technician visit?")
        preferred_time = speech_to_text()
    else:
        full_name = ""
        contact_info = ""
        address = ""
        issue_details = ""
        preferred_time = ""

    return full_name, contact_info, address, issue_details, preferred_time


def speak(text):
    response_text.insert(tk.END, f"Assistant: {text}\n", "italic")
    response_text.see(tk.END)
    root.update()
    engine.say(text)
    engine.runAndWait()

def process_request():
    audio_text = speech_to_text()
    if audio_text:
        intent = analyze_intent(audio_text)
        response_text.insert(tk.END, f"Recognized Intent: {intent}\n", "normal")
        root.update()
        params = {"q": audio_text}
        if intent == "warranty_claim" or intent == "technical_issue":
            full_name, contact_info, address, issue_details, preferred_time = extract_information(intent)
            speak("Thank you. Your information has been recorded.")
            extracted_info.set(f"Full Name: {full_name}\nContact Information: {contact_info}\nAddress: {address}\nIssue Details: {issue_details}\nPreferred Time: {preferred_time}")
            save_to_json(full_name, contact_info, address, issue_details, preferred_time)
        else:
            speak("Sorry, I couldn't understand your request.")
            extracted_info.set("")

def save_to_json(full_name, contact_info, address, issue_details, preferred_time):
    data = {
        "Full Name": full_name,
        "Contact Information": contact_info,
        "Address": address,
        "Issue Details": issue_details,
        "Preferred Time": preferred_time
    }
    with open("user_data.json", "a") as file:
        json.dump(data, file, indent=4)
        file.write("\n")

root = tk.Tk()
root.title("Customer Virtual Assistant")

# Styles
style = ttk.Style()
style.configure("Bold.TLabel", font=("Helvetica", 12, "bold"))
style.configure("Normal.TLabel", font=("Helvetica", 10))
style.configure("Italic.TLabel", font=("Helvetica", 10, "italic"))

# Header
header_label = ttk.Label(root, text="Customer Virtual Assistant", style="Bold.TLabel")
header_label.grid(row=0, column=0, columnspan=2, pady=10)

# Load Image
img = Image.open(r"C:\Users\Lucky\Documents\Coherence 1.0\cocru\mic_icon.png")
img = img.resize((50, 50))  # Resize the image
img = ImageTk.PhotoImage(img)

# Button
button = ttk.Button(root, image=img, command=process_request)
button.grid(row=1, column=0, columnspan=2, pady=5)

# Response Text
response_text = scrolledtext.ScrolledText(root, width=50, height=10)
response_text.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# Extracted Info
extracted_info = tk.StringVar()
info_label = ttk.Label(root, textvariable=extracted_info, style="Normal.TLabel")
info_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
