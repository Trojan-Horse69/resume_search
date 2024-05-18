from langchain.indexes import SQLRecordManager, index
from utils import hf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma

collection_name = "resume_index2_chroma"

embedding = hf

vectorstore = Chroma(embedding_function=hf, persist_directory="./index2_resume_chroma_db")

namespace = f"chroma/{collection_name}"
record_manager = SQLRecordManager(
    namespace, db_url="sqlite:///record_manager_index2_chroma_cache.sql"
)

record_manager.create_schema()

loader = PyPDFDirectoryLoader("./resumes")
resumes = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000, chunk_overlap=500)

resume = text_splitter.split_documents(resumes)

index(resume, record_manager, vectorstore, cleanup="incremental", source_id_key="source")
