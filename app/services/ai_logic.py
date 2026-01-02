# This file now checks the "Score" from Qdrant. If the score is high, it uses your FAQ. If the score is low, it uses the LLM's general knowledge.
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from app.core.config import settings

def get_dynamic_answer(user_input: str):
    # 1. Setup the Client
    client = QdrantClient(url=settings.QDRANT_URL)
    
    # 2. Setup Embeddings 
    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.OPENROUTER_KEY,
        base_url=settings.OPENROUTER_BASE_URL
    )
    
    # 3. Use the updated QdrantVectorStore class 
    vector_store = QdrantVectorStore(
        client=client, 
        collection_name="faq_collection", 
        embedding=embeddings
    )
    
    # 4. Search for FAQ matches
    found_docs = vector_store.similarity_search_with_score(user_input, k=1)
    
    context = ""
    is_faq_match = False
    
    # Logic: Only use FAQ if it's a strong match (Score > 0.7)
    if found_docs and found_docs[0][1] > 0.7:
        context = found_docs[0][0].page_content
        is_faq_match = True

    # 5. Setup the LLM
    llm = ChatOpenAI(
        model_name=settings.MODEL,
        openai_api_key=settings.OPENROUTER_KEY,
        openai_api_base=settings.OPENROUTER_BASE_URL
    )

    if is_faq_match:
        prompt = f"Use this FAQ data to answer: {context}. Question: {user_input}"
    else:
        prompt = f"Answer this general question: {user_input}"

    response = llm.invoke(prompt)

    return str(response.content)