from google.cloud import texttospeech
from google.cloud.speech import enums
from google.cloud.speech import types

import os
import re
import sys
import requests
from bs4 import BeautifulSoup

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/shie/desktop/My First Project-db5ead32661e.json"


def main():
    
        
    text = []
    html = raw_input("Provide URL:  ")
 
    
    r = requests.get(html, allow_redirects=True)
    open('page2.html', 'wb').write(r.content)
    f = open ('page2.html', 'r')

    soup = BeautifulSoup(f.read(), 'html.parser')
    
    visible_text = ''    
    
    paragraphs = soup.findAll(['title', 'p'])
    
    for div in soup.find_all({'aside'}): 
        div.decompose()
        
    for div in soup.find_all("p", {'class':'message'}): 
        div.decompose()

        
    for paragraph in paragraphs:
        visible_text += '\n' + ''.join(paragraph.findAll(text = True))
    


    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=visible_text)

    # Build the voice request, select the language code ("en-US") 
    # ****** the NAME
    # and the ssml voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-GB',
        name='en-GB-Wavenet-B',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
if __name__ == '__main__':
    main()