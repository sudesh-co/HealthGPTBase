import os
import subprocess
import platform
from gtts import gTTS
import pydub
from pydub import AudioSegment
import elevenlabs
from elevenlabs.client import ElevenLabs

# Step 1a: Convert MP3 to WAV using pydub
def convert_mp3_to_wav(mp3_filepath, wav_filepath):
    audio = AudioSegment.from_mp3(mp3_filepath)
    audio.export(wav_filepath, format="wav")

# Step 1b: Setup Text to Speech (TTS) with gTTS
def text_to_speech_with_gtts_old(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

# Step 1c: Setup Text to Speech (TTS) with ElevenLabs
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",  # You can change the voice name here
        output_format="mp3_22050_32",  # Define your audio format
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

# Optional: Uncomment this to test ElevenLabs TTS
# text_to_speech_with_elevenlabs_old(input_text="Hello from ElevenLabs!", output_filepath="elevenlabs_testing.mp3")

# Step 2: Use Model for Text Output to Voice (main function with OS-based playback)
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)
    
    # Convert the MP3 file to WAV (useful for compatibility with other tools)
    convert_mp3_to_wav(output_filepath, "gtts_testing_autoplay.wav")

    os_name = platform.system()
    
    # Playback based on OS
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])  # macOS-specific audio player
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath]) 
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Example usage
input_text = "Hi, this is AI with Sudesh! Autoplay testing."
text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")


def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text= input_text,
        voice= "Aria",
        output_format= "mp3_22050_32",
        model= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

#text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")