from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

def build_chatbot(llm, vectorstore):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    retriever = vectorstore.as_retriever()
    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
    return qa_chain
