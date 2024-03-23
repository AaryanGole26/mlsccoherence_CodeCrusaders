import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    # Welcome message
    print("Welcome to the Virtual Assistant.")
    text_to_speech("Welcome to the Virtual Assistant. Please provide your details.")

    # Ask for user details
    name = input("What's your name? ")
    text_to_speech(f"Nice to meet you, {name}!")

    text_to_speech(f"How old are you?")
    age = input("How old are you? ")
    text_to_speech(f"You are {age} years old.")

    text_to_speech(f"Where are you from?")
    location = input("Where are you from? ")
    text_to_speech(f"Great! You are from {location}.")

    # Say goodbye
    print("Thank you for providing your details. Goodbye!")
    text_to_speech("Thank you for providing your details. Goodbye!")

if __name__ == "__main__":
    main()