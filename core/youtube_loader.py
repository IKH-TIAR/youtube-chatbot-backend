from urllib.parse import urlparse, parse_qs
import re
from pytubefix import YouTube

def extract_video_id(url: str) -> str:
    """
    Extract the video ID from a YouTube URL.
    """
    parsed = urlparse(url)

    if parsed.hostname == 'youtu.be':
        return parsed.path[1:]
    if parsed.hostname in ['www.youtube.com', 'youtube.com']:
        return parse_qs(parsed.query).get('v', [None])[0]
    return None

def fetch_youtube_transcript(video_url: str) -> str:
    try:
        yt = YouTube(video_url)
        caption = yt.captions.get('en') or yt.captions.get('a.en')
        print("Fetched YouTube transcript successfully.")
    except Exception as e:
        print("Error fetching YouTube transcript:", e)
        return "Transcript not available."

    if caption:
        srt_captions = caption.generate_srt_captions()
        text_only = re.sub(r'\d+\n\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d\n', '', srt_captions)
        text_only = re.sub(r'\n+', ' ', text_only).strip()
        print(text_only)
        return text_only
    else:
        return "Transcript not available."
