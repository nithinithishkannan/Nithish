import speech_recognition as sr
import moviepy.editor as mp
from gtts import gTTS as gs
from deep_translator import GoogleTranslator as gt
from io import BytesIO
import time
from pygame import mixer
from gtts import gTTS as gs
from io import BytesIO
# Convert video to audio
clip = mp.VideoFileClip(r'C:\Users\91948\Downloads\child.mp4')
clip.audio.write_audiofile(r'C:\Users\91948\Downloads\child12.wav')

r = sr.Recognizer()

audio = sr.AudioFile(r'C:\Users\91948\Downloads\child12.wav')
with audio as source:
    audio_data = r.record(source)

# Perform speech recognition
result = r.recognize_google(audio_data)
print("Recognized speech:", result)

# Initialize mixer
mixer.init()

def speak(txt, ln):
    mp3_fp = BytesIO()
    tts = gs(text=txt, lang=ln)
    tts.write_to_fp(mp3_fp)
    return mp3_fp


lng_code = ['ta', 'te', 'hi', 'kn', 'en', 'es', 'ml', 'ja', 'mr']
txt = result
translated_texts = ""

# Iterate over languages
for i in lng_code:
    t = gt(source='auto', target=i).translate(txt)
    print(t, 'langauage code', i)

    # Speak the translated text
    sound = speak(t, i)
    sound.seek(0)
    mixer.music.load(sound)
    mixer.music.play()
    time.sleep(1)

    # Append translated text to the variable
    translated_texts += f"{t}\n"

# Save the translated texts to a text file
# Save the translated texts to a text file with UTF-8 encoding
text_file_path = r'C:\Users\91948\Downloads\translated_speech03.txt'
with open(text_file_path, 'w', encoding='utf-8') as file:
    file.write(translated_texts)

print("Translated speech saved to this path for verification:", text_file_path)

