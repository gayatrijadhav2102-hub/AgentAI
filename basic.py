from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv


load_dotenv()  # 👈 don't forget to call this!

llm = ChatOpenAI(temperature=0.3, model="gpt-4o")


def demo_basic_prompt():
    template = """
    You are a helpful assistant who always replies cheerfully and with emojis
    Question: {question}
    Answer: 
    """

    prompt = PromptTemplate(input_variables=["question"], template=template)

    chain = prompt | llm | StrOutputParser()  # SYNTAX: langchain Expression language
    # prompt sent to llm. Then llm process it and return ouput. convert str output.
    result = chain.invoke({"question": "what is Agentic AI?"})
    print(result)


demo_basic_prompt()  # 👈 don't forget to call the function!


def demo_chat_prompt():  # System Prompt
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "you are a {role} who speaks in a {style} manner.")(
                "human", "{user_input}"
            ),
        ]
    )

    chain = chat_prompt | llm | StrOutputParser()
    result = chain.invoke({"role": "Hindi Teacher"})
    print(result)


demo_chat_prompt


def demo_sequential():

    topic_prompt = PromptTemplate.from_template(
        "Generate a creative topic about {subject} in one sentence."
    )

    content_prompt = PromptTemplate.from_template(
        "Write a short paragrapg (2-3 sentences) about: {topic}"
    )

    topic_runnable = topic_prompt | llm | StrOutputParser()
    content_runnable = content_prompt | llm | StrOutputParser()

    sequential = (
        RunnablePassthrough()  # pass information from 1 LLM to 2nd LLM
        .assign(topic=topic_runnable)
        .assign(content=content_runnable)
    )

    result = sequential.invoke({"subject": "artifical Intelligence"})

    print(result)

    demo_sequential()
