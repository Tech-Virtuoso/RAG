from flask import Flask, render_template, request, jsonify
from loaders import load_pdf
from splitter import split_docs
from vectorstore import create_vectorstore
from llm_config import get_llm
from chatbot import build_chatbot
from logger_config import setup_logger
import os
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# Setup logging
logger = setup_logger()

app = Flask(__name__)

# Global variable to store chatbot instance
chatbot_instance = None
initialization_lock = False

def initialize_chatbot():
    """Initialize chatbot with detailed logging and optimization"""
    global chatbot_instance, initialization_lock
    
    if chatbot_instance is not None:
        logger.info("Chatbot already initialized, returning existing instance")
        return chatbot_instance
    
    if initialization_lock:
        logger.info("Initialization in progress, waiting...")
        return None
    
    initialization_lock = True
    
    try:
        total_start_time = time.time()
        logger.info("=== Starting RAG Chatbot Initialization ===")
        
        # Step 1: Load PDF
        pdf_start = time.time()
        logger.info("Step 1/5: Loading PDF document...")
        pdf_path = r"D:\Inside AIML\Projects\RAG\data\cs224n-self-attention-transformers-2023_draft.pdf"
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"PDF path exists: {pdf_path}")
        pages = load_pdf(pdf_path)
        
        if not pages:
            raise Exception("No pages loaded from PDF")
            
        pdf_time = time.time() - pdf_start
        logger.info(f"✓ PDF loaded successfully in {pdf_time:.2f} seconds ({len(pages)} pages)")
        logger.info(f"First page content preview: {pages[0].page_content[:100]}...")
        
        # Step 2: Split documents
        split_start = time.time()
        logger.info("Step 2/5: Splitting documents into chunks...")
        documents = split_docs(pages)
        
        if not documents:
            raise Exception("No documents created after splitting")
            
        split_time = time.time() - split_start
        logger.info(f"✓ Documents split successfully in {split_time:.2f} seconds ({len(documents)} chunks)")
        logger.info(f"First chunk content preview: {documents[0].page_content[:100]}...")
        
        # Step 3: Create vectorstore
        vector_start = time.time()
        logger.info("Step 3/5: Creating/loading vectorstore with nomic embeddings...")
        vectorstore = create_vectorstore(documents)
        
        if vectorstore is None:
            raise Exception("Failed to create or load vectorstore")
        
        vector_time = time.time() - vector_start
        logger.info(f"✓ Vectorstore ready in {vector_time:.2f} seconds")
        
        # Step 4: Initialize LLM
        llm_start = time.time()
        logger.info("Step 4/5: Initializing Mistral LLM...")
        llm = get_llm("mistral")
        llm_time = time.time() - llm_start
        logger.info(f"✓ LLM initialized successfully in {llm_time:.2f} seconds")
        
        # Step 5: Build chatbot
        build_start = time.time()
        logger.info("Step 5/5: Building RAG chatbot chain...")
        chatbot_instance = build_chatbot(llm, vectorstore)
        build_time = time.time() - build_start
        logger.info(f"✓ Chatbot chain built successfully in {build_time:.2f} seconds")
        
        # Summary
        total_time = time.time() - total_start_time
        logger.info("=== Initialization Summary ===")
        logger.info(f"PDF Loading:        {pdf_time:>8.2f} seconds")
        logger.info(f"Document Splitting: {split_time:>8.2f} seconds")
        logger.info(f"Vectorstore:        {vector_time:>8.2f} seconds")
        logger.info(f"LLM Initialization: {llm_time:>8.2f} seconds")
        logger.info(f"Chatbot Building:   {build_time:>8.2f} seconds")
        logger.info(f"Total Time:         {total_time:>8.2f} seconds")
        logger.info("=== Initialization Complete ===")
        
        return chatbot_instance
        
    except Exception as e:
        logger.error(f"❌ Initialization failed: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        initialization_lock = False
        raise
    finally:
        initialization_lock = False

def initialize_with_timeout():
    """Initialize chatbot with timeout"""
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(initialize_chatbot)
        try:
            return future.result(timeout=600)  # 10 minutes timeout
        except TimeoutError:
            logger.error("❌ Initialization timed out after 10 minutes")
            raise

@app.route('/')
def home():
    logger.info("Home page accessed")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            logger.warning("Empty message received")
            return jsonify({"error": "No message provided"}), 400

        logger.info(f"Processing chat request: '{user_message[:50]}...'")
        
        # Get chatbot instance
        chatbot = initialize_chatbot()
        if chatbot is None:
            logger.error("Chatbot not initialized")
            return jsonify({"error": "Chatbot not ready. Please try again."}), 503
        
        # Time the response
        start_time = time.time()
        logger.info("Generating response...")
        
        response = chatbot.run({"question": user_message})
        
        response_time = time.time() - start_time
        logger.info(f"✓ Response generated in {response_time:.2f} seconds")
        
        return jsonify({"response": response})
    
    except Exception as e:
        logger.error(f"❌ Error processing chat request: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request. Please try again."}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        if chatbot_instance is not None:
            return jsonify({"status": "healthy", "chatbot": "ready"})
        else:
            return jsonify({"status": "initializing", "chatbot": "not_ready"})
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == '__main__':
    try:
        logger.info("🚀 Starting RAG Chatbot Application...")
        
        # Initialize chatbot in background
        initialize_with_timeout()
        
        logger.info("🌐 Starting Flask web server...")
        app.run(debug=False, port=5000, host='0.0.0.0')
        
    except Exception as e:
        logger.error(f"❌ Failed to start application: {str(e)}")
        raise