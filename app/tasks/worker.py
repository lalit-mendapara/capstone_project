# This uses Celery + Redis to read your faqs.txt and move it into Qdrant so the AI can find it. It includes File I/O logic.

from celery import Celery
from langchain_community.document_loaders import TextLoader
from langchain_classic.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from app.core.config import settings
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

celery_app = Celery("tasks", broker=settings.REDIS_URL)

@celery_app.task
def ingest_faq_file(file_path: str):
    # 1. Standard Loading and Splitting
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    
    # 2. Setup Embeddings
    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.OPENROUTER_KEY,
        base_url=settings.OPENROUTER_BASE_URL
    )

    # 3. MANUAL QDRANT SETUP (To avoid the 'init_from' error)
    client = QdrantClient(url=settings.QDRANT_URL)
    collection_name = "faq_collection"

    # We manually handle the collection creation
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=rest.VectorParams(
            size=1536, # Standard size for OpenAI/OpenRouter embeddings
            distance=rest.Distance.COSINE
        )
    )

    # 4. Use the stable 'add_documents' method instead of 'from_documents'
    vector_store = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings
    )
    vector_store.add_documents(docs)
    
    return "FAQ Indexing Successful"