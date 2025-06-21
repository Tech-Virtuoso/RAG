import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logger():
    """Setup logging with file rotation and timestamps"""
    
    # Create logs directory if it doesn't exist
    logs_dir = "./logs"
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create timestamp for log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(logs_dir, f"rag_chatbot_{timestamp}.log")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # File handler with rotation (max 10MB per file, keep 5 files)
            RotatingFileHandler(
                log_file, 
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            ),
            # Console handler
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")
    return logger 