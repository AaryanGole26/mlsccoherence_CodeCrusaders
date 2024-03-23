import csv
import pyttsx3
import speech_recognition as sr

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        return text if text else ""  # Return empty string if no speech is recognized
    except sr.UnknownValueError:
        print("Could not understand audio. Please speak clearly and try again.")
        return ""  # Return empty string if no speech is recognized
    except sr.RequestError as e:
        print(f"Error fetching results; {e}")
        return ""  # Return empty string if no speech is recognized

def load_issues_from_csv(csv_file):
    issues = {}
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            issues[row['Issue']] = row['Suggestion']
    return issues

def get_issue_category(ivr_responses):
    print("\nPlease select the category of the issue:")
    for index, (category, issues) in enumerate(ivr_responses.items(), start=1):
        text_to_speech(f"Press {index} for {category}")
        print(f"{index}. {category}")
    while True:
        try:
            selected_index = int(input("Enter your choice: "))  # Accept input from keyboard
            if 1 <= selected_index <= len(ivr_responses):
                selected_category = list(ivr_responses.keys())[selected_index - 1]
                return selected_category
            else:
                print("Invalid input. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_issue(ivr_responses, selected_category):
    print(f"\nPlease select the issue under {selected_category}:")
    issues = ivr_responses[selected_category]
    for index, issue in enumerate(issues, start=1):
        text_to_speech(f"Press {index} for {issue}")
        print(f"{index}. {issue}")
    while True:
        try:
            selected_index = int(input("Enter your choice: "))  # Accept input from keyboard
            if 1 <= selected_index <= len(issues):
                return issues[selected_index - 1]
            else:
                print("Invalid input. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():
    # Load issues from CSV
    issues = load_issues_from_csv('issues.csv')

    print("Welcome to the Virtual Assistant.")
    text_to_speech("Welcome to the Virtual Assistant, this is Max. What's your name?")

    name = recognize_speech()
    text_to_speech(f"Nice to meet you, {name}!")

    while True:
        text_to_speech(f"How old are you?")
        age = recognize_speech()
        try:
            age = int(age)
            if age < 0 or age > 150:
                text_to_speech("Please provide a valid age between 0 and 150.")
            else:
                break  # Break out of loop if input is successfully converted to an integer
        except ValueError:
            text_to_speech("Please enter a valid integer for age.")

    text_to_speech(f"Where are you from?")
    location = recognize_speech()

    # Define IVR responses (category: [issues])
    ivr_responses = {
        "Technical Issues": ["Product not working", "Slow internet connection", "Forgot password"],
        "Order Related Issues": ["Item out of stock", "Incorrect billing"],
        "Delivery Issues": ["Delivery delayed", "Package damaged upon arrival"]
    }

    # Get issue category using IVR numbers
    selected_category = get_issue_category(ivr_responses)
    text_to_speech(f"You have selected {selected_category}.")

    # Get issue under the selected category
    selected_issue = get_issue(ivr_responses, selected_category)
    suggestion = issues.get(selected_issue, "We don't have suggestions for this issue.")

    # Provide suggestion
    print(f"\nWe suggest: {suggestion}")
    text_to_speech(f"We suggest: {suggestion}")

    # Say goodbye
    print("\nThank you for providing your details. Goodbye!")
    text_to_speech("Thank you for providing your details. Goodbye!")

if __name__ == "__main__":
    main()
