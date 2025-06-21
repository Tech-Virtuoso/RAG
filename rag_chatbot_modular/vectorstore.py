from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings, HuggingFaceEmbeddings
import logging
import os
import time
from typing import List, Optional

logger = logging.getLogger(__name__)

class OptimizedVectorstore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = None
        self.vectorstore = None
        
    def initialize_embeddings(self):
        """Initialize embeddings with fallback to local model if Ollama is not available"""
        try:
            logger.info("Attempting to initialize nomic-embed-text embeddings via Ollama...")
            start_time = time.time()
            
            # Test Ollama connection first
            logger.info("Testing Ollama connection...")
            import requests
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=5)
                if response.status_code != 200:
                    raise Exception(f"Ollama server not responding properly. Status: {response.status_code}")
                logger.info("✓ Ollama server is running")
            except Exception as e:
                logger.warning(f"Ollama server not accessible: {str(e)}")
                logger.info("Falling back to local sentence-transformers embeddings...")
                return self._initialize_local_embeddings()
            
            self.embeddings = OllamaEmbeddings(
                model="nomic-embed-text:latest",
                base_url="http://localhost:11434"
            )
            
            # Test the embeddings
            logger.info("Testing embedding generation...")
            test_embedding = self.embeddings.embed_query("test")
            if not test_embedding or len(test_embedding) == 0:
                raise Exception("Embedding generation failed - empty result")
            
            logger.info(f"✓ Nomic embeddings initialized successfully in {time.time() - start_time:.2f} seconds")
            logger.info(f"✓ Test embedding generated with {len(test_embedding)} dimensions")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize nomic embeddings: {str(e)}")
            logger.info("Falling back to local sentence-transformers embeddings...")
            return self._initialize_local_embeddings()
    
    def _initialize_local_embeddings(self):
        """Initialize local sentence-transformers embeddings"""
        try:
            logger.info("Initializing local sentence-transformers embeddings...")
            start_time = time.time()
            
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            # Test the embeddings
            logger.info("Testing local embedding generation...")
            test_embedding = self.embeddings.embed_query("test")
            if not test_embedding or len(test_embedding) == 0:
                raise Exception("Local embedding generation failed - empty result")
            
            logger.info(f"✓ Local embeddings initialized successfully in {time.time() - start_time:.2f} seconds")
            logger.info(f"✓ Test embedding generated with {len(test_embedding)} dimensions")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize local embeddings: {str(e)}")
            return False
    
    def load_or_create_vectorstore(self, documents: List) -> Optional[Chroma]:
        """Load existing vectorstore or create new one with caching"""
        try:
            # Check if vectorstore exists
            if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
                logger.info(f"Loading existing vectorstore from cache: {self.persist_directory}")
                start_time = time.time()
                
                try:
                    self.vectorstore = Chroma(
                        persist_directory=self.persist_directory,
                        embedding_function=self.embeddings
                    )
                    
                    # Test the loaded vectorstore
                    test_result = self.vectorstore.similarity_search("test", k=1)
                    logger.info(f"✓ Vectorstore loaded from cache in {time.time() - start_time:.2f} seconds")
                    return self.vectorstore
                    
                except Exception as e:
                    logger.warning(f"Failed to load cached vectorstore: {str(e)}")
                    logger.info("Will create new vectorstore...")
                    # Continue to create new vectorstore
            
            logger.info(f"Creating new vectorstore with {len(documents)} documents...")
            start_time = time.time()
            
            # Create new vectorstore
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            
            # Persist to disk
            logger.info("Persisting vectorstore to disk...")
            self.vectorstore.persist()
            
            logger.info(f"✓ New vectorstore created and saved in {time.time() - start_time:.2f} seconds")
            return self.vectorstore
                
        except Exception as e:
            logger.error(f"❌ Error in load_or_create_vectorstore: {str(e)}")
            logger.error(f"Documents count: {len(documents) if documents else 0}")
            logger.error(f"Persist directory: {self.persist_directory}")
            return None
    
    def get_vectorstore(self, documents: List) -> Optional[Chroma]:
        """Main method to get vectorstore with optimization"""
        if not self.embeddings:
            if not self.initialize_embeddings():
                return None
        
        return self.load_or_create_vectorstore(documents)

# Global instance
vectorstore_manager = OptimizedVectorstore()

def create_vectorstore(documents):
    """Optimized vectorstore creation with fallback embeddings"""
    try:
        logger.info(f"Starting vectorstore creation with {len(documents)} documents")
        result = vectorstore_manager.get_vectorstore(documents)
        
        if result is None:
            logger.error("❌ Vectorstore creation failed")
            return None
            
        logger.info("✓ Vectorstore creation completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"❌ Unexpected error in create_vectorstore: {str(e)}")
        return None
