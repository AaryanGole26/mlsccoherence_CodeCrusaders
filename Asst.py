import speech_recognition as sr
import pyttsx3
import requests

# Set up Wit.ai access token
WIT_ACCESS_TOKEN = "XZF3P3IDPPTU2YG5O6FUIU36E6654G77"

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Initialize speech synthesizer
engine = pyttsx3.init()

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

# Main function
if __name__ == "__main__":
    while True:
        speak("Press Enter to start speaking...")
        input("Press Enter to start speaking...")
        audio_text = speech_to_text()
        if audio_text:
            intent = analyze_intent(audio_text)
            print("Recognized Intent:", intent)
            params = {"q": audio_text}  
            if intent == "warranty claim":
                speak("Please provide your full name.")
                full_name = speech_to_text()
                speak("Please provide your contact information.")
                contact_info = speech_to_text()
                speak("Please provide your address.")
                address = speech_to_text()
                speak("Thank you. Your information has been recorded.")
            elif intent == "technical issue":
                speak("Please describe the technical issue.")
                issue_details = speech_to_text()
                speak("What is your preferred date and time for technician visit?")
                preferred_time = speech_to_text()
                speak("Thank you. Your information has been recorded.")
            else:
                speak("Sorry, I couldn't understand your request.")

            # Extract information based on intent and print it
            full_name, contact_info, address, issue_details, preferred_time = extract_information(intent)
            print("Extracted Information:")
            print("Full Name:", full_name)
            print("Contact Information:", contact_info)
            print("Address:", address)
            print("Issue Details:", issue_details)
            print("Preferred Time:", preferred_time)
