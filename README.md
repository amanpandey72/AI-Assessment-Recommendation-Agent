# SHL AI Assessment Recommendation Agent

## Overview

The SHL AI Assessment Recommendation Agent is an intelligent recommendation system that helps recruiters and hiring managers identify the most suitable SHL assessments based on job roles, required skills, and hiring requirements.

The application uses semantic search powered by Sentence Transformers and FAISS to retrieve relevant assessments from the official SHL Product Catalog. It also supports assessment comparison, clarification questions, and guardrails to ensure responses remain within the SHL assessment domain.

---

## Features

* Scrapes the latest SHL Product Catalog
* Cleans and structures assessment metadata
* Generates semantic embeddings using Sentence Transformers
* Stores embeddings in a FAISS vector index
* Retrieves relevant assessments using semantic search
* Recommends the most suitable SHL assessments
* Compares multiple assessments
* Asks clarification questions for ambiguous queries
* Rejects out-of-domain questions using guardrails
* REST API built with FastAPI
* Interactive Swagger documentation

---

## Tech Stack

* Python 3.10+
* FastAPI
* FAISS
* Sentence Transformers (all-MiniLM-L6-v2)
* Requests
* BeautifulSoup
* NumPy
* PyTest

---

## Project Structure

```
SHL AI AGENT/

├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── api.py
│   ├── clarification.py
│   ├── comparison.py
│   ├── embeddings.py
│   ├── guardrails.py
│   ├── main.py
│   ├── prompt_builder.py
│   ├── retriever.py
│   └── schemas.py
│
├── scraper/
│   ├── scrape_catalog.py
│   └── clean_catalog.py
│
├── data/
│   ├── raw_catalog.json
│   ├── catalog.json
│   ├── assessments.json
│   ├── faiss.index
│   └── metadata.pkl
│
├── tests/
│   ├── test_health.py
│   └── test_chat.py
│
├── README.md
├── requirements.txt
└── approach.pdf
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd SHL-AI-Agent
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Building the Dataset

Download the SHL Product Catalog:

```bash
python scraper/scrape_catalog.py
```

Clean the catalog:

```bash
python scraper/clean_catalog.py
```

Generate embeddings and create the FAISS index:

```bash
python app/embeddings.py
```

---

## Running the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Health Check

**GET**

```
/health
```

Response

```json
{
  "status": "ok"
}
```

---

### Chat Endpoint

**POST**

```
/chat
```

Request

```json
{
  "message": "Recommend an assessment for a Java Developer."
}
```

Example Response

```json
{
  "status": "success",
  "response": "...",
  "results": [...]
}
```

---

## Supported Query Types

Examples:

* Recommend Java assessments
* Recommend Python assessments
* Recommend assessments for graduates
* Compare Java 8 and Core Java assessments
* Suggest assessments for software developers
* Assessments for data analysts
* Remote testing assessments
* Adaptive assessments

---

## System Workflow

1. Download SHL Product Catalog
2. Clean and normalize assessment data
3. Generate semantic embeddings
4. Store vectors in FAISS
5. Receive user query
6. Validate query using guardrails
7. Ask clarification if required
8. Retrieve relevant assessments
9. Return recommendations or comparisons

---

## Testing

Run all tests:

```bash
python -m pytest
```

---

## Future Improvements

* Conversation memory
* Hybrid retrieval (keyword + semantic search)
* Result reranking
* Metadata-based filtering
* LLM-powered response generation
* Docker deployment
* Cloud deployment

---

## Author

Aman Pandey

AI Assessment Recommendation Agent Assignment
