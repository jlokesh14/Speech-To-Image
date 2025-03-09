import os
import requests
from PIL import Image
import speech_recognition as sr
from translate import Translator
from monsterapi import client
from langdetect import detect

recognizer = sr.Recognizer()

with sr.Microphone() as Source:
    print('Say Something!...')
    recognizer.adjust_for_ambient_noise(Source) #remove the background noise
    audio = recognizer.listen(Source)

    try:
        text = recognizer.recognize_google(audio)
        detected_lang = detect(text)
        translator = Translator(from_lang=detected_lang, to_lang='en')
        translator_text = translator.translate(text)
        print(translator_text)
    except sr.UnknownValueError:
        print("Can't Understand")
    except sr.RequestError:
        print('Google API Error')

try:

    api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjQ5ODI4OGY3MDJhMzA4MDcxNThjMDMxM2EwYjI4YTU4IiwiY3JlYXRlZF9hdCI6IjIwMjUtMDItMjRUMDg6MzM6MDYuNDU1Njg3In0.ZdPUJoVJFjnqYuW8kDwxrU3CtFl9OXRMdDdrMwSF2TQ'  # Replace 'your-api-key' with your actual Monster API key
    monster_client = client(api_key)

    model = 'txt2img' 
    input_data = {
        'prompt': translator_text,
        'negprompt': 'deformed, bad anatomy, disfigured, poorly drawn face',
        'samples': 1,
        'steps': 50,
        'aspect_ratio': 'square',
        'guidance_scale': 7.5,
        'seed': 2414,
    }

    result = monster_client.generate(model, input_data)

    #print(result['output'])

    img_url = result['output'][0]
    file_name = 'image.png'
    response = requests.get(img_url)
except NameError:
    print('Please provide data to generate the image')
else:
    if response.status_code == 200:
        with open(file_name, 'wb') as file: #for reading image 'wb'
            file.write(response.content)
            print('Image downloaded')
            img = Image.open(file_name)
            #img.show(title='translator_text')
        os.system(f'start {file_name}')
    else:
        print("Something went wrong, please try again!... (or) Image is not downloaded")