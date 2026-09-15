# 📚 Multi-PDF RAG Assistant

A **Multi-Document Retrieval-Augmented Generation (RAG) system** that allows users to ask questions across a collection of PDF documents and receive answers grounded in the retrieved document content.

The system loads multiple PDFs, splits their content into chunks, generates semantic embeddings, stores them in a FAISS vector index, retrieves the most relevant chunks for a user query, and uses an LLM through the **Groq API** to generate a grounded answer.

---

## 🚀 Features

* 📄 **Multi-PDF Document Support**

  * Load and process multiple PDF documents from a single folder.

* ✂️ **Document Chunking**

  * Splits extracted PDF text into smaller overlapping chunks for efficient retrieval.

* 🧠 **Semantic Embeddings**

  * Uses `all-MiniLM-L6-v2` from Sentence Transformers to convert document chunks and queries into vector representations.

* 🔎 **Semantic Retrieval**

  * Uses FAISS to efficiently retrieve the most relevant document chunks.

* 🎯 **Distance-Based Filtering**

  * Filters retrieved chunks using a similarity-distance threshold to reduce irrelevant context.

* 🤖 **LLM-Powered Answers**

  * Uses the Groq API with `openai/gpt-oss-120b` to generate answers based only on retrieved context.

* 📚 **Source Attribution**

  * Displays the PDF documents that contributed information to the generated answer.

* 🔄 **Interactive Question Loop**

  * Users can ask multiple questions in a single session.
  * Type `exit` or `quit` to terminate the application.

* 🧩 **Modular Architecture**

  * PDF loading, chunking, embeddings, retrieval, prompting, and LLM generation are separated into individual modules.

---

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │   PDF Documents  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    PDF Loader    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Chunker      │
                    │  500 / 50 overlap│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Embeddings    │
                    │ all-MiniLM-L6-v2 │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   FAISS Index    │
                    └────────┬─────────┘
                             │
                             │
              User Query ────┤
                             ▼
                    ┌──────────────────┐
                    │ Query Embedding  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Retriever     │
                    │ Top-K + Filtering│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Retrieved Context│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Prompt Generator │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Groq LLM      │
                    │ GPT-OSS-120B     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Answer + Sources │
                    └──────────────────┘
```

---

## 📁 Project Structure

```text
Multi PDF RAG/
│
├── documents/
│   ├── Artificial Intelligence.pdf
│   ├── Computer Vision.pdf
│   ├── Data Science.pdf
│   ├── Deep Learning.pdf
│   ├── Generative AI.pdf
│   ├── Large Language Models.pdf
│   ├── Machine Learning.pdf
│   ├── Natural Language Processing.pdf
│   ├── Python.pdf
│   ├── RAG.pdf
│   ├── SQL.pdf
│   └── Transformers.pdf
│
├── modules/
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── faiss_index.py
│   ├── retriever.py
│   ├── prompts.py
│   └── llm.py
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Technologies Used

| Technology                | Purpose                         |
| ------------------------- | ------------------------------- |
| **Python**                | Core programming language       |
| **PyPDF**                 | PDF text extraction             |
| **Sentence Transformers** | Semantic embeddings             |
| **all-MiniLM-L6-v2**      | Embedding model                 |
| **FAISS**                 | Vector similarity search        |
| **NumPy**                 | Numerical operations            |
| **Groq API**              | LLM inference                   |
| **GPT-OSS-120B**          | Answer generation               |
| **python-dotenv**         | Environment variable management |

---

## 🔄 How It Works

### 1. PDF Loading

All PDF files placed inside the `documents/` directory are loaded automatically.

Each document is represented with:

```python
{
    "text": "...",
    "source": "Machine Learning.pdf"
}
```

The `source` metadata is preserved throughout the pipeline so the system can identify where retrieved information came from.

---

### 2. Chunking

Large PDF documents are divided into smaller chunks.

Current configuration:

```text
Chunk size: 500
Overlap:     50
```

The overlap helps preserve context between neighboring chunks.

---

### 3. Embedding Generation

Each chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

The resulting embeddings are stored as a matrix and used for semantic retrieval.

---

### 4. FAISS Vector Index

The embeddings are stored in a FAISS index using:

```python
faiss.IndexFlatL2
```

This allows the system to search for chunks that are semantically close to the user's query.

---

### 5. Query Processing

When the user enters a question, the query is converted into an embedding using the same embedding model.

For example:

```text
How are transformers used in large language models?
```

The query embedding is compared against the document chunk embeddings.

---

### 6. Retrieval

The system retrieves the top relevant chunks.

The retriever also applies a distance threshold to remove chunks that are too far from the query in the embedding space.

Current configuration:

```text
Top-K: 3
Maximum distance: 1.2
```

These values are experimental and can be tuned during evaluation.

---

### 7. Context Construction

The retrieved chunks are combined into a context containing their source information.

Example:

```text
Source: Transformers.pdf

Transformers are a deep learning architecture...

--------------------

Source: Generative AI.pdf

Transformers have become the foundation
of most modern language models...

--------------------
```

---

### 8. Prompt Generation

The retrieved context and user question are inserted into a prompt that instructs the LLM to answer using only the provided information.

If the answer cannot be found in the retrieved documents, the model is instructed to say:

```text
I could not find the answer in the provided documents.
```

---

### 9. LLM Generation

The prompt is sent to the Groq API using:

```text
openai/gpt-oss-120b
```

The generated response is then displayed to the user.

---

### 10. Source Attribution

The system extracts the unique PDF filenames from the retrieved chunks.

For example:

```text
Sources:
- Transformers.pdf
- Generative AI.pdf
```

This provides basic traceability for the generated answer.

---

## 💬 Example

```text
============================================================
MULTI-PDF RAG ASSISTANT
============================================================

Ask questions about your PDF documents.
Type 'exit' to quit.

You: How are transformers used in large language models?

Assistant:

Transformers form the core architecture of large language
models. LLMs are built as transformer-based models that
process sequential data using attention mechanisms. They
provide the foundation for modern LLMs and enable models
to learn complex patterns from large datasets.

Sources:
- Generative AI.pdf
- Transformers.pdf

You: exit

Exiting Multi-PDF RAG Assistant...
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Do **not** commit your `.env` file to GitHub.

Add it to `.gitignore`:

```text
.env
```

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

### 2. Navigate to the project

```bash
cd "Multi PDF RAG"
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### 5. Add PDF documents

Place your PDF files inside:

```text
documents/
```

### 6. Run the application

```bash
python main.py
```

---

## 🧪 Current Capabilities

The system has been tested with a collection of **12 PDF documents** covering topics such as:

* Artificial Intelligence
* Machine Learning
* Deep Learning
* Generative AI
* Large Language Models
* Transformers
* Natural Language Processing
* Computer Vision
* Data Science
* Python
* SQL
* RAG

The system can retrieve information from different PDFs for a single query and provide the combined information to the LLM.

---

## 📌 Current Limitations

* The FAISS index is rebuilt every time the application starts.
* Conversation history is not yet maintained.
* Retrieval currently operates using a fixed `top_k` value.
* The distance threshold is manually configured.
* PDF text extraction quality depends on the structure of the source PDF.
* There is currently no automated retrieval evaluation framework.
* The application currently uses a command-line interface.

---

## 🔮 Future Improvements

Planned improvements include:

* [ ] Conversation memory
* [ ] RAG evaluation and retrieval metrics
* [ ] Improved retrieval strategies
* [ ] Better document-level source ranking
* [ ] Persistent FAISS index
* [ ] Metadata-based filtering
* [ ] Streamlit interface
* [ ] Improved error handling
* [ ] Production deployment
* [ ] RAG performance monitoring

---

## 🎯 Learning Objectives

This project focuses on understanding how **Multi-Document RAG systems** work beyond a basic single-document RAG pipeline.

Key concepts explored:

* Multi-document ingestion
* Metadata preservation
* Collection-level semantic retrieval
* Shared vector indexes
* Retrieval noise
* Distance-based filtering
* Multi-document context construction
* Source attribution
* LLM-grounded generation
* Interactive RAG workflows

---

## 👨‍💻 Author

**Ananth Jeeth Vuppala**

B.Tech in Electronics & Communication Engineering
Aspiring Software Engineer | AI/ML | NLP | LLMs

---

## ⭐ Project Goal

The goal of this project is to build a practical **Multi-Document RAG system from scratch** while understanding each component of the pipeline rather than relying on high-level RAG frameworks.

The project is being developed incrementally, with each stage focusing on a specific RAG concept.