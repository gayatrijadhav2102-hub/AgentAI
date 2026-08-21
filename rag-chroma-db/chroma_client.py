# import os
# from functools import lru_cache

# import chromadb
# from dotenv import load_dotenv
# from langchain_chroma import Chroma
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# load_dotenv()


# DEFAULT_COLLECTION = os.getenv("CHROMA_COLLECTION", "practice-demo")
# DEFAULT_TOP_K = int(os.getenv("CHROMA_TOP_K", "4"))


# @lru_cache
# def get_vectorstore():
#     return Chroma(
#         collection_name=DEFAULT_COLLECTION, embedding_function=OpenAIEmbeddings()
#     )

import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)

load_dotenv()

DEFAULT_COLLECTION = os.getenv("CHROMA_COLLECTION", "practice-demo")
DEFAULT_TOP_K = int(os.getenv("CHROMA_TOP_K", "4"))


def get_vectorstore(collection_name=DEFAULT_COLLECTION):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        chroma_cloud_api_key=os.getenv("CHROMA_API_KEY"),
        tenant=os.getenv("CHROMA_TENANT"),
        database=os.getenv("CHROMA_DATABASE"),
    )


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )
