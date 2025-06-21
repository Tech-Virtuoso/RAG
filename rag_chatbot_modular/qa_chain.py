from langchain.chains.question_answering import load_qa_chain

def get_qa_chain(llm, chain_type="stuff"):
    return load_qa_chain(llm, chain_type=chain_type)
