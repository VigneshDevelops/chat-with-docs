from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from app.config import PINECONE_INDEX
from langchain_core.prompts import PromptTemplate


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


async def chat(question: str, chat_history=[]):
    try:
        embeddings = OpenAIEmbeddings()
        vectorstore = PineconeVectorStore(
            embedding=embeddings, index_name=PINECONE_INDEX
        )
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        retriever = vectorstore.as_retriever()
        template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer. 
        Provide your answer in markdown format if necessary
        {context}
        Question: {question}
        Helpful Answer:"""

        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"], template=template
        )

        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT},
        )
        input = {"question": question, "chat_history": chat_history}
        result = chain.invoke(input)
        print(result)
        return result
    except Exception as e:
        print(e)
        raise e
