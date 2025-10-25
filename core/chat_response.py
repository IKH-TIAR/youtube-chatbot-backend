from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from .vectorstore import get_vectordb
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def chat_response(query: str, video_id: str):
    vector_store = get_vectordb(video_id)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = PromptTemplate(
        template="""You are an AI assistant that helps users by providing information based on the following context from a YouTube video transcript:
        Context:
        {context}
        Question:
        {question}
        Answer clearly and concisely.
        """,
        input_variables=["context", "question"]
    )

    chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY)
    final_prompt = prompt.format(context=context, question=query)
    response = chat.invoke(final_prompt)
    return response.content


