import os

# Define directory and files
base_dir = "rag_chatbot_modular"
files = {
    "loaders.py": '''from langchain.document_loaders import PyPDFLoader

def load_pdf(path):
    loader = PyPDFLoader(path)
    return loader.load()
''',

    "splitter.py": '''from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_docs(pages, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(pages)
''',

    "vectorstore.py": '''from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings

def create_vectorstore(docs, model_name='nomic-embed-text'):
    embedding_model = OllamaEmbeddings(model=model_name)
    return FAISS.from_documents(docs, embedding_model)
''',

    "llm_config.py": '''from langchain.llms import Ollama

def get_llm(model_name='mistral'):
    return Ollama(model=model_name)
''',

    "qa_chain.py": '''from langchain.chains.question_answering import load_qa_chain

def get_qa_chain(llm, chain_type="stuff"):
    return load_qa_chain(llm, chain_type=chain_type)
''',

    "chatbot.py": '''from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

def build_chatbot(llm, vectorstore):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    retriever = vectorstore.as_retriever()
    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
    return qa_chain
''',

    "main.py": '''from loaders import load_pdf
from splitter import split_docs
from vectorstore import create_vectorstore
from llm_config import get_llm
from chatbot import build_chatbot

if __name__ == "__main__":
    pdf_path = r"D:\\Inside AIML\\Projects\\RAG\\data\\cs224n-self-attention-transformers-2023_draft.pdf"
    pages = load_pdf(pdf_path)
    documents = split_docs(pages)

    vectorstore = create_vectorstore(documents)
    llm = get_llm("mistral")
    chatbot = build_chatbot(llm, vectorstore)

    print("Chatbot is ready! Type 'exit' to stop.")
    while True:
        query = input("You: ")
        if query.lower() == 'exit':
            break
        response = chatbot.run({"question": query})
        print("Bot:", response)
'''
}

# Create base directory
os.makedirs(base_dir, exist_ok=True)

# Create each file with corresponding content
for filename, content in files.items():
    with open(os.path.join(base_dir, filename), "w", encoding="utf-8") as f:
        f.write(content)

print(f"Project structure created in '{base_dir}' directory.")
