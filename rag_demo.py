import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompt import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


def create_sample_documents():
    documents = [
        Document(
            page_content="Milo the Mouse",
            metadata={"source": "langchain_intro", "topic": "overview"},
        ),
        Document(
            page_content="Nila and umbrella",
            metadata={"source": "langchain_intro", "topic": "technical"},
        ),
    ]
    return documents


def demo_rag():

    llm = ChatOpenAI(
        temperature=0,
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    )

    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small")
    )

    documents = create_sample_documents()

    for doc in documents:
        topic = doc.metadata.get("topic", "unknown")
        preview = doc.page_content.strip()[:60] + "..."
        print(topic)
        print(preview)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)

    splits = text_splitter.split_documents(documents)
    print(splits)

    vectorstore = FAISS.from_documents(splits, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    return retriever, llm


def demo_rag_chain(retriever, llm):
    template = """
    Answer the question based only on the following context:

    Context:
    {context}

    Question: {question}

    Answer:
    """

    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    result = rag_chain.invoke("Who is Milo?")
    print(result)


if __name__ == "__main__":
    retriever, llm = demo_rag()
    demo_rag_chain(retriever, llm)
