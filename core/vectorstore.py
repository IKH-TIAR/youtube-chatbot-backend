from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')

def get_vectordb(video_id: str):

    embedding = GoogleGenerativeAIEmbeddings(
        model='models/gemini-embedding-001',
        google_api_key=GOOGLE_API_KEY
    )

    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        timeout=60
    )

    collection_name = f"video_{video_id}"

    collections = [col.name for col in qdrant_client.get_collections().collections]

    if collection_name not in collections:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=3072,
                distance=Distance.COSINE
            ),
        )

    vectordb = QdrantVectorStore(
        client=qdrant_client,
        collection_name=collection_name,
        embedding=embedding
    )
    return vectordb
