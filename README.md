
### ✅ Option 1: Use Startup Script *(Recommended)*

**Windows Command Prompt:**
```bash
start_app.bat
````

**PowerShell:**

```powershell
.\start_app.ps1
```

### 🔧 Option 2: Manual Setup

1. **Activate Conda Environment:**

   ```bash
   conda activate chatbot
   ```

2. **Start Ollama Server (in separate terminal):**

   ```bash
   ollama serve
   ```

3. **Launch Flask Application:**

   ```bash
   python app.py
   ```

4. **Access in Browser:**

   ```
   http://localhost:5000
   ```

---

## 📦 Prerequisites

* **Conda Environment:** `chatbot` (with all required packages)
* **Ollama Installed:** [https://ollama.ai/](https://ollama.ai/)
* **Required Models via Ollama:**

  * `nomic-embed-text` (embeddings)
  * `mistral` (text generation)

---

## 🖥️ Ollama Server Requirements

### 🔁 Why It Must Be Started Every Time

* Ollama **does not auto-start** as a service on Windows
* LLMs must be **loaded into memory** (Mistral: \~4.1 GB, Nomic: \~274 MB)
* **Flask app connects to Ollama** at `http://localhost:11434`
* Startup time varies depending on model load status

---

### ⚙️ Ollama Startup Options

#### 🟢 Easy: Use Startup Scripts

These scripts will:

* Start Ollama in background
* Wait for models to load
* Launch Flask server

```bash
start_app.bat       # CMD
start_app.ps1       # PowerShell
```

#### 🟡 Manual: Use Two Terminals

```bash
# Terminal 1
ollama serve

# Terminal 2
conda activate chatbot
python app.py
```

#### 🔵 Optional: Windows Service Setup

To run Ollama automatically on Windows boot:

```bash
# Run once as Administrator
setup_ollama_service.bat
```

---

### 🧠 Model Load Times

| Scenario            | Duration  |
| ------------------- | --------- |
| First-time startup  | 10–30 sec |
| Subsequent startups | 5–15 sec  |
| Memory Usage        | \~4.5 GB  |

---

## ✨ Features

* 🧠 Conversational AI powered by **Mistral-7B**
* 📄 PDF support for contextual chat (e.g., CS224n notes)
* 🔍 Semantic search via `nomic-embed-text`
* 💬 Floating modern chat UI
* ⚡ Real-time query response
* 📊 Timestamped logs for monitoring

---

## 📁 Project Structure

```
rag_chatbot_modular/
├── app.py                      # Flask entry point
├── chatbot.py                  # Core RAG logic
├── vectorstore.py              # ChromaDB operations
├── loaders.py                  # PDF/document loaders
├── splitter.py                 # Text chunking logic
├── llm_config.py               # Ollama model configuration
├── logger_config.py            # Logging setup
├── qa_chain.py                 # RAG chain logic
├── templates/
│   └── index.html              # Web UI (chat interface)
├── chroma_db/                  # Vector database storage
├── logs/                       # Log files
├── start_app.bat               # CMD startup script
├── start_app.ps1               # PowerShell startup script
├── setup_ollama_service.bat    # (Optional) Auto-start setup
└── requirements.txt            # Python dependencies
```

---

## 🛠️ Troubleshooting

### 🔴 Ollama Server Not Running

* Ensure Ollama is installed: `https://ollama.ai/`
* Start Ollama: `ollama serve`
* Check available models: `ollama list`
* Pull models:

  ```bash
  ollama pull nomic-embed-text  
  ollama pull mistral
  ```

### 🔴 Conda Environment Issues

* Create: `conda create -n chatbot python=3.9`
* Install dependencies: `pip install -r requirements.txt`

### 🔴 Port 5000 Already in Use

* Modify the port in `app.py`
* Kill process using port:

  ```bash
  netstat -ano | findstr :5000  
  taskkill /PID <PID> /F
  ```

### 🔴 Insufficient RAM

* Ensure your system has at least **8GB RAM** available

---

## 📜 Logs

* Located in `./logs/`
* Named with timestamps
* Used for debugging, monitoring, and auditing

---

## 🧠 Models Used

| Task            | Model                 | Source |
| --------------- | --------------------- | ------ |
| Embeddings      | `nomic-embed-text`    | Ollama |
| LLM             | `Mistral-7B-Instruct` | Ollama |
| Vector Database | `ChromaDB`            | Local  |
| PDF Parsing     | `PyPDF2`, LangChain   | Python |

---

## ✅ Summary

This RAG chatbot delivers a modern, modular, and production-ready pipeline for question answering over documents using Ollama and LangChain. With real-time semantic search and responsive UI, it’s ideal for document understanding, study assistance, or custom enterprise chatbots.

---

## 📬 Questions or Feedback?

Feel free to open an [issue](https://github.com/your-repo/issues) or contact the maintainer for support.

---

