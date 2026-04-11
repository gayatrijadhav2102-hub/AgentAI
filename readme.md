# 📄 Text Splitter in LangChain

## 🚀 Overview

Text Splitters in LangChain are used to **break large documents into smaller chunks** so that they can be processed efficiently by language models and embedding systems.

Large Language Models (LLMs) have **token limits**, so splitting text ensures:

* Better performance
* Accurate retrieval
* Efficient memory usage

---

## 🧠 Why Text Splitting is Important

When working with:

* PDFs 📄
* Large documents 📚
* Websites 🌐

You cannot directly send full content to LLM because:

* Token limits will be exceeded
* Retrieval quality will be poor

👉 Solution: **Split text into smaller meaningful chunks**

---

## ⚙️ Common Text Splitter Used

### 🔹 RecursiveCharacterTextSplitter

This is the most commonly used splitter in LangChain.

It splits text:

* Based on characters
* Maintains context
* Avoids breaking sentences abruptly

---

## 🧩 Example Code

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

texts = text_splitter.split_text("This is a long document...")
print(texts)
```

---

## 🔍 Parameters Explained

### 1. `chunk_size`

* Maximum size of each chunk
* Example: 100 characters

### 2. `chunk_overlap`

* Overlap between chunks
* Helps maintain context

👉 Example:

```
Chunk 1: ABCDEFGHIJ
Chunk 2:      FGHIJKLMNO
```

---

## 📊 Why Overlap is Important

Without overlap ❌:

* Context breaks
* Poor retrieval

With overlap ✅:

* Better understanding
* Improved answer quality

---

## 🔄 How It Works in RAG

```
Document → Text Splitter → Chunks → Embeddings → Vector DB → Retrieval → LLM
```

---

## 🧪 Example in Your Project

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10
)

splits = text_splitter.split_documents(documents)
```

---

## 🎯 Best Practices

* Use **small chunk size (200–500)** for better accuracy
* Use **overlap (10–20%)** to preserve context
* Avoid very large chunks (bad retrieval)

---

## ⚡ Different Types of Splitters

| Splitter                       | Use Case              |
| ------------------------------ | --------------------- |
| CharacterTextSplitter          | Simple splitting      |
| RecursiveCharacterTextSplitter | Best general use ✅    |
| TokenTextSplitter              | Token-based splitting |
| MarkdownTextSplitter           | Markdown documents    |
| HTMLTextSplitter               | Web pages             |

---

## 🧠 Interview Answer

**Q: Why use Text Splitter in LangChain?**

👉 Text Splitters are used to divide large documents into smaller chunks so they can be efficiently processed, embedded, and retrieved in RAG pipelines without exceeding token limits.

---

## 🚀 Conclusion

Text Splitters are a **core component in RAG systems**.
They ensure that:

* Data is structured properly
* Retrieval is accurate
* LLM responses are meaningful

Without text splitting, building scalable GenAI applications is not possible.
