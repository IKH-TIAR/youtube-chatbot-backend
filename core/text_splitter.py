from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text: str):
    """
    Split the given text into smaller chunks using RecursiveCharacterTextSplitter.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    docs = text_splitter.create_documents([text])
    return docs