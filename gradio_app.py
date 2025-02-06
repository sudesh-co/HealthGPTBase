import os
import gradio as gr
import gtts
from pydub import AudioSegment
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq

# Load environment variables if necessary
# from dotenv import load_dotenv
# load_dotenv()

system_prompt = """You have to act as a professional doctor. What's in this image? Do you find anything wrong with
it medically? If you make a differential, suggest some remedies for them. Always provide advice that is safe and 
non-harmful. Do not add any numbers or special characters in your response. Your response should be in one long paragraph. 
Always answer as if you are answering to a real person. Do not say 'In the image I see' but say 'With what I see, 
I think you have ....' Do not respond as an AI model in markdown, your answer should mimic that of an actual doctor,
not an AI bot. Keep your answer concise (max 2 sentences). No preamble, start your answer right away please.
"""

# Convert MP3 to WAV using pydub (required for SoundPlayer to work)
def convert_mp3_to_wav(mp3_filepath, wav_filepath):
    audio = AudioSegment.from_mp3(mp3_filepath)
    audio.export(wav_filepath, format="wav")

# Use gtts to generate MP3 from text
def text_to_speech_with_gtts(input_text, output_filepath):
    tts = gtts.gTTS(input_text, lang='en')
    tts.save(output_filepath)  # Saves as MP3 by default

# Function to process both audio and image inputs
def process_inputs(audio_filepath, image_filepath):
    # Transcribe audio to text
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                                                 audio_filepath=audio_filepath,
                                                 stt_model="whisper-large-v3")

    # Handle the image input and run analysis
    if image_filepath:
        doctor_response = analyze_image_with_query(query=system_prompt + speech_to_text_output,
                                                   encoded_image=encode_image(image_filepath),
                                                   model="llama-3.2-11b-vision-preview")
    else:
        doctor_response = "No image provided for me to analyze"

    # Convert doctor response to speech (MP3 file)
    mp3_output_path = "final.mp3"
    text_to_speech_with_gtts(input_text=doctor_response, output_filepath=mp3_output_path)

    # Optionally, convert MP3 to WAV (if using SoundPlayer for WAV playback)
    wav_output_path = "final.wav"
    convert_mp3_to_wav(mp3_output_path, wav_output_path)

    # Return the result: speech-to-text, doctor response, and the audio file
    return speech_to_text_output, doctor_response, mp3_output_path  # Or return wav_output_path if using WAV

# Create the Gradio interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("final.mp3")  
    ],
    title="AI Doctor with Vision and Voice"
)

iface.launch(debug=True)
