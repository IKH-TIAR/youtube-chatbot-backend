from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

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
    ytt = YouTubeTranscriptApi()
    video_id = extract_video_id(video_url)
    if not video_id:
        return "Invalid YouTube URL"

    try:
        transcript = ytt.fetch(video_id)
        return " ".join([entry.text for entry in transcript])
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."