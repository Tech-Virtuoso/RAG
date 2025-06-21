from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_docs(pages, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(pages)
