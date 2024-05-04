from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from app.config import PINECONE_INDEX
from langchain_core.prompts import PromptTemplate
import asyncio
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler


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

    PineconeVectorStore.from_documents(texts, embeddings, index_name=PINECONE_INDEX)
    print("Embedding Created")


async def conversational_qa_chain(question: str, chat_history=[], callback=None):
    try:
        embeddings = OpenAIEmbeddings()
        vectorstore = PineconeVectorStore(
            embedding=embeddings, index_name=PINECONE_INDEX
        )
        llm = ChatOpenAI(
            model="gpt-3.5-turbo", temperature=0, streaming=True, callbacks=[callback]
        )
        retriever = vectorstore.as_retriever()
        template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know; don't try to make up an answer. Provide your answer in markdown format if necessary.
        context: {context}
        Question: {question}"""

        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"], template=template
        )

        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT},
            verbose=True,
        )
        return chain
        # input = {"question": question, "chat_history": chat_history}
        # result = chain.invoke(input)
        # return result
    except Exception as e:
        print(e)
        raise e


async def chat(question: str, chat_history=[]):
    try:
        chain = await conversational_qa_chain(question, chat_history)
        input = {"question": question, "chat_history": chat_history}
        result = chain.invoke(input)
        return result
    except Exception as e:
        print(e)
        raise e


async def chat_stream(question: str, chat_history=[]):
    try:
        callback = AsyncIteratorCallbackHandler()
        chain = await conversational_qa_chain(question, chat_history, callback)
        input = {"question": question, "chat_history": chat_history}
        task = asyncio.create_task(chain.ainvoke(input=input))
        print("Stream start")
        async for token in callback.aiter():
            print(token)
            yield token

        await task
    except Exception as e:
        print(e)
        raise e
