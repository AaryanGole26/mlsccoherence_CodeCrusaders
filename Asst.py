import speech_recognition as sr
import pyttsx3
import requests
import json
import os


WIT_ACCESS_TOKEN = "XZF3P3IDPPTU2YG5O6FUIU36E6654G77"


recognizer = sr.Recognizer()

# Initialize speech synthesizer
engine = pyttsx3.init()

# Initialize a list to store user data
all_user_data = []

# Function to load existing JSON data from file
def load_existing_data():
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as json_file:
            return json.load(json_file)
    else:
        return []

# Function to save all user data to JSON file
def save_user_data():
    with open("user_data.json", "w") as json_file:
        json.dump(all_user_data, json_file, indent=4)

def speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Transcribing...")
        text = recognizer.recognize_google(audio) 
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Speech recognition service error; {0}".format(e))
        return ""

def analyze_intent(text):
    headers = {"Authorization": f"Bearer {WIT_ACCESS_TOKEN}"}
    params = {"q": text}
    response = requests.get("https://api.wit.ai/message", headers=headers, params=params)
    data = response.json()
    print("Wit.ai Response:", data)
    intent = data['intents'][0]['name'] if data.get('intents') else "Unknown"
    return intent

def extract_information(intent):
    if intent == "warranty_claim":
        speak("Please provide your full name.")
        full_name = speech_to_text()  
        speak("Please provide your contact information.")
        contact_info = speech_to_text() 
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
        speak("Please provide your address.")
        address = speech_to_text()  
        speak("Please describe the technical issue.")
        issue_details = speech_to_text()  
        speak("What is your preferred date and time for technician visit?")
        preferred_time = speech_to_text()  
    else:
        # Default values
        full_name = ""
        contact_info = ""
        address = ""
        issue_details = ""
        preferred_time = ""

    return full_name, contact_info, address, issue_details, preferred_time


def speak(text):
    engine.say(text)
    engine.runAndWait()

# Inside the main function
if __name__ == "__main__":
    all_user_data = []
    all_user_data.extend(load_existing_data())  # Load existing user data
    
    while True:
        speak("Press Enter to start speaking...")
        input("Press Enter to start speaking...")
        audio_text = speech_to_text()
        print("Recognized Text:", audio_text)  # Print the recognized text for debugging
        if audio_text:
            intent = analyze_intent(audio_text)
            print("Recognized Intent:", intent)
            params = {"q": audio_text}  # Include the audio text in the params
            if intent == "warranty_claim":
                speak("Please provide your full name.")
                full_name = speech_to_text()
                speak("Please provide your contact information.")
                contact_info = speech_to_text()
                speak("Please provide your address.")
                address = speech_to_text()
                speak("Thank you. Your information has been recorded.")
            elif intent == "technical_issue":
                speak("Please describe the technical issue.")
                issue_details = speech_to_text()
                speak("What is your preferred date and time for technician visit?")
                preferred_time = speech_to_text()
                speak("Thank you. Your information has been recorded.")
            else:
                speak("Sorry, I couldn't understand your request.")

            # Extract information based on intent and append it to the list
            full_name, contact_info, address, issue_details, preferred_time = extract_information(intent)
            user_data = {
                "intent": intent,
                "full_name": full_name,
                "contact_info": contact_info,
                "address": address,
                "issue_details": issue_details,
                "preferred_time": preferred_time
            }
            all_user_data.append(user_data)

            # Save all user data to the JSON file
            save_user_data()

