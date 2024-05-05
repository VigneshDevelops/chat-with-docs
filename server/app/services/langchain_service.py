from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from app.config import PINECONE_INDEX
import asyncio
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.schema import AIMessage, HumanMessage


from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain


async def create_embeddings_for_docs(url):
    loader = DirectoryLoader(url)
    docs = loader.load()
    print(len(docs))
    print("Document(s) loaded")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    texts = text_splitter.split_documents(docs)
    print("Completed: Text Split")

    # embedding model
    embeddings = OpenAIEmbeddings()
    
    # delete all 
    try:
        PineconeVectorStore(embedding=embeddings, index_name=PINECONE_INDEX).delete(
            delete_all=True
        )
    except Exception:
        pass

    PineconeVectorStore.from_documents(texts, embeddings, index_name=PINECONE_INDEX)
    print("Embedding Created")


def form_history_obj(history):
    new_history = []
    for entry in history:
        if entry["type"] == "ai_response":
            ai_message = AIMessage(entry["message"])
            new_history.append(ai_message)
        elif entry["type"] == "user_prompt":
            human_message = HumanMessage(entry["message"])
            new_history.append(human_message)

    return new_history


async def qa_chain(callback=AsyncIteratorCallbackHandler()):
    contextualize_q_system_prompt = """
Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is.
"""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    embeddings = OpenAIEmbeddings()
    vectorstore = PineconeVectorStore(embedding=embeddings, index_name=PINECONE_INDEX)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    retriever = vectorstore.as_retriever()
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    qa_system_prompt = """
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.

    {context}
    
     Always provide your answers in markdown format
    """
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    streaming_llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        streaming=True,
        callbacks=[callback],
        verbose=True,
    )
    question_answer_chain = create_stuff_documents_chain(streaming_llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return rag_chain


async def chat(question: str, chat_history=[]):
    try:
        chain = await qa_chain()
        history = form_history_obj(chat_history)
        input = {"input": question, "chat_history": history}
        result = chain.invoke(input)
        return result
    except Exception as e:
        print(e)
        raise e


async def chat_stream(question: str, chat_history=[]):
    try:
        callback = AsyncIteratorCallbackHandler()
        chain = await qa_chain(callback)
        history = form_history_obj(chat_history)
        input = {"input": question, "chat_history": history}
        task = asyncio.create_task(chain.ainvoke(input=input))
        print("Stream start")
        async for token in callback.aiter():
            print(token)
            yield token

        await task
    except Exception as e:
        print(e)
        raise e
