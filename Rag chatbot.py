from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

loader = PyPDFLoader("D:\\Rag and LLm\\sodapdf-converted.pdf")
doc=loader.load()
text=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=200
)
documents=text.split_documents(doc)
print(f"Number of documents:{len(documents)}")  
embedding=HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}
)
db=FAISS.from_documents(documents,embedding)
db.save_local("faiss_index")
retriever = db.as_retriever(search_kwargs={"k": 3})
llm=ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key="Your key"
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
    return_source_documents=True
)
query = "What is Rag chatbot?"
result = qa.run(query)
print("Answer:", result)


