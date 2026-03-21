# 🤖 LangChain Prompt Engineering & Chains Demo

## 🚀 Overview

This project demonstrates the **core concepts of LangChain**, including:

* Prompt Templates
* Chat Prompt Templates
* Output Parsing
* Sequential Chains (LCEL)
* OpenAI LLM integration

It is a beginner-friendly implementation to understand how **LLMs interact with structured prompts and chains**.

---

## 🧠 Concepts Covered

### 1. PromptTemplate

Used to create structured prompts for LLMs.

### 2. ChatPromptTemplate

Supports **system + human messages**, useful for chat-based applications.

### 3. Output Parsers

Converts LLM output into readable string format.

### 4. LCEL (LangChain Expression Language)

Pipeline syntax for chaining components:

```
prompt | llm | parser
```

### 5. Sequential Chain

Passing output from one LLM step to another.

---

## 📂 Project Structure

```
.
├── main.py
├── .env
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

---

### 2. Install Dependencies

```bash
pip install langchain langchain-openai python-dotenv
```

---

### 3. Add Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 🧪 Features Implemented

---

### 🔹 1. Basic Prompt Chain

Generates a response using a simple prompt template.

```python
prompt | llm | StrOutputParser()
```

✔ Example:

* Input: "What is Agentic AI?"
* Output: Cheerful explanation with emojis 😊

---

### 🔹 2. Chat Prompt (System + Human)

Defines role-based responses using system instructions.

✔ Example:

* Role: Hindi Teacher
* Style: Friendly
* Output: AI explained in conversational Hindi tone

---

### 🔹 3. Sequential Chain (Multi-Step Reasoning)

Two-step LLM pipeline:

```
Subject → Topic → Content
```

✔ Step 1: Generate topic
✔ Step 2: Generate paragraph using topic

---

## 🔄 Workflow

```
User Input → Prompt → LLM → Output Parser → Result
```

For sequential chain:

```
Input → Topic Generator → Content Generator → Final Output
```

---

## 🎯 Use Cases

* Chatbots 🤖
* Content generation ✍️
* Educational tools 📚
* AI assistants
* Prompt engineering experiments

---

## 🧠 Interview Questions

**Q1: What is PromptTemplate?**
👉 It helps structure inputs for LLMs dynamically.

**Q2: Difference between PromptTemplate & ChatPromptTemplate?**
👉 PromptTemplate is for simple text, while ChatPromptTemplate supports role-based messaging.

**Q3: What is LCEL?**
👉 A pipeline-based syntax (`|`) to chain components in LangChain.

**Q4: What is Sequential Chain?**
👉 Output of one LLM step is used as input for another.

---

## 🚀 Future Improvements

* Add Memory (conversation history)
* Integrate RAG (Retrieval-Augmented Generation)
* Build API using FastAPI
* Create frontend using React

---

## 🏁 Conclusion

This project provides a solid foundation for understanding how to:

* Design prompts
* Chain LLM operations
* Build structured GenAI workflows

---

## 👩‍💻 Author

**Gayatri Jadhav**

---

⭐ If you found this helpful, give it a star!
