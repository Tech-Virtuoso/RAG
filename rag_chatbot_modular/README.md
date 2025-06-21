# RAG Chatbot Application

A professional Retrieval-Augmented Generation (RAG) chatbot built with Flask, Ollama, and LangChain.

## Quick Start

### Option 1: Using the Startup Script (Recommended)

**For Windows Command Prompt:**
```bash
start_app.bat
```

**For PowerShell:**
```powershell
.\start_app.ps1
```

### Option 2: Manual Steps

1. **Activate the conda environment:**
   ```bash
   conda activate chatbot
   ```

2. **Start Ollama server (in a separate terminal):**
   ```bash
   ollama serve
   ```

3. **Run the Flask application:**
   ```bash
   python app.py
   ```

4. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

## Prerequisites

- **Conda environment named `chatbot`** with all required packages
- **Ollama** installed and running
- **Models available in Ollama:**
  - `nomic-embed-text` (for embeddings)
  - `mistral` (for text generation)

## Important: Ollama Server Requirements

### Why Ollama Server Must Be Started Each Time

The RAG chatbot requires the **Ollama server to be running** because:

1. **Ollama is not a Windows service** - it doesn't start automatically with Windows
2. **Models need to be loaded into memory** - Mistral (4.1GB) and nomic-embed-text (274MB)
3. **API endpoints are provided by Ollama** - your Flask app connects to `localhost:11434`
4. **Server startup takes time** - models need to be loaded and initialized

### Startup Process

Every time you want to use the RAG chatbot:

1. **Ollama server must be started first** (loads models into memory)
2. **Flask application connects to Ollama** on port 11434
3. **Models become available** for embeddings and text generation

### Solutions

#### 🟢 **Easiest: Use Startup Scripts**
The provided scripts (`start_app.bat` or `start_app.ps1`) automatically:
- Start Ollama server in background
- Wait for server to be ready
- Launch Flask application
- Handle all the startup sequence

#### 🟡 **Manual: Two Terminal Approach**
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Run Flask app
conda activate chatbot
python app.py
```

#### 🔵 **Advanced: Windows Service (One-time setup)**
Make Ollama start automatically with Windows:
```bash
# Run as administrator once:
setup_ollama_service.bat
```

### Model Loading Time

- **First startup:** 10-30 seconds (models load into memory)
- **Subsequent startups:** 5-15 seconds (models already cached)
- **Memory usage:** ~4.5GB total (Mistral + nomic-embed-text)

## Features

- 🤖 Professional ChatGPT-like UI
- 📄 PDF document processing (CS224n lecture notes)
- 🔍 Semantic search with nomic embeddings
- 💬 Conversational AI with Mistral LLM
- 📊 Detailed logging to `./logs/` folder
- 🎨 Modern floating chat interface
- ⚡ Real-time responses

## File Structure

```
rag_chatbot_modular/
├── app.py                 # Main Flask application
├── chatbot.py            # Chatbot logic
├── vectorstore.py        # Vector database operations
├── loaders.py            # Document loading utilities
├── splitter.py           # Text splitting utilities
├── llm_config.py         # LLM configuration
├── logger_config.py      # Logging configuration
├── qa_chain.py           # Question-answering chain
├── templates/
│   └── index.html        # Web interface
├── chroma_db/            # Vector database storage
├── logs/                 # Application logs
├── start_app.bat         # Windows startup script
├── start_app.ps1         # PowerShell startup script
├── setup_ollama_service.bat # Ollama Windows service setup
└── requirements.txt      # Python dependencies
```

## Troubleshooting

### Ollama Server Not Running
- Make sure Ollama is installed: https://ollama.ai/
- Start Ollama server: `ollama serve`
- Check if models are available: `ollama list`
- **Use startup scripts** to avoid manual server management

### Conda Environment Issues
- Create environment: `conda create -n chatbot python=3.9`
- Install requirements: `pip install -r requirements.txt`

### Port Already in Use
- Change port in `app.py` or kill existing process
- Default port: 5000

### Model Loading Issues
- Check available models: `ollama list`
- Pull missing models: `ollama pull nomic-embed-text` or `ollama pull mistral`
- Ensure sufficient RAM (8GB+ recommended)

## Logs

Detailed logs are saved in the `./logs/` folder with timestamps for debugging and monitoring.

## Models Used

- **Embeddings:** nomic-embed-text (via Ollama)
- **Language Model:** Mistral-7B-Instruct-v0.3 (via Ollama)
- **Vector Database:** ChromaDB
- **Document Processing:** PyPDF2, LangChain 