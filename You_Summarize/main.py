import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

load_dotenv()  # Load environment variables

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 500 words. Please provide the summary of the text given here : """

# Extract transcript details from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[-1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

        transcript = ""
        for entry in transcript_text:
            transcript += " " + entry["text"]

        return transcript

    except NoTranscriptFound:
        st.error("Transcript not found for the video. Ensure that the video has a transcript available in English.")
        return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Generate summary based on prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"An error occurred while generating content: {str(e)}")
        return None

# Streamlit app
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("v=")[-1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        if summary:
            st.markdown("## Detailed Notes:")
            st.write(summary)
