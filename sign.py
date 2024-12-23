import speech_recognition as sr
import cv2
import pyttsx3
import os
recognizer = sr.Recognizer()
engine = pyttsx3.init()
def get_voice_input():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)  
        print("Listening for voice input...")
        try:
            audio = recognizer.listen(source, timeout=10)  
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError:
            print("Network issue. Try again.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def map_to_sign_language(text):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return [char.upper() for char in text if char.isalpha()]

def load_images_for_letters(letters):
    path = r'C:/Users/mahit/Downloads/images-20241217T153119Z-001/images'
    images = []

    for letter in letters:
        image_path_png = os.path.join(path, f"{letter}.png")  
        image_path_jpg = os.path.join(path, f"{letter}.jpg")  

        
        if os.path.exists(image_path_png):
            images.append(cv2.imread(image_path_png))
        elif os.path.exists(image_path_jpg):
            images.append(cv2.imread(image_path_jpg))
        else:
            print(f"Sign image for {letter} not found in .png or .jpg formats.")
            images.append(None)  

    return images


def resize_images(images, target_width=100, target_height=100):
    resized_images = []
    for image in images:
        if image is not None:
            resized_images.append(cv2.resize(image, (target_width, target_height)))
        else:
            resized_images.append(None)
    return resized_images


def display_all_signs(images):
    
    images = resize_images(images, target_width=100, target_height=100)  
    
    combined_image = None
    for image in images:
        if image is not None:
            if combined_image is None:
                combined_image = image  
            else:
                combined_image = cv2.hconcat([combined_image, image])  

    
    if combined_image is not None:
        cv2.imshow("All Signs", combined_image)
        cv2.waitKey(10000)  
        cv2.destroyAllWindows()
    else:
        print("No valid images to display.")


def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def main():
    print("Starting Voice to Sign Language Recognition System...")
    text = get_voice_input()  
    if text:
        letters = map_to_sign_language(text)  
        if letters:
            print(f"Displaying signs for: {', '.join(letters)}")
            images = load_images_for_letters(letters)  
            display_all_signs(images)  
        else:
            text_to_speech("No valid alphabet found in your input.")
    else:
        text_to_speech("Could not understand your input. Please try again.")


if __name__ == "__main__":
    main()
