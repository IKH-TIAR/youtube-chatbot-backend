from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.query_request import QueryRequest
from models.video_request import VideoRequest
from core.chat_response import chat_response
from core.youtube_loader import extract_video_id, fetch_youtube_transcript
from core.vectorstore import get_vectordb
from core.text_splitter import split_text

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    print("✅ ROOT ENDPOINT HIT")
    return {"message": "Server is running!", "status": "ok"}

@app.post("/api/load_video")
def load_video(video_link: VideoRequest):
    print( "Received video link:", video_link.video_link)
    link = video_link.video_link
    video_id = extract_video_id(link)
    transcript = fetch_youtube_transcript(link)
    chunks = split_text(transcript)

    vectordb = get_vectordb(video_id)
    vectordb.add_documents(chunks)

    return {"message": "Video transcript loaded and processed successfully.",
            "video_id": video_id
            }

@app.post("/api/query")
def handle_query(query: QueryRequest):
    query_text = query.query
    video_id = query.video_id
    response = chat_response(query_text, video_id)
    return {"response": response}