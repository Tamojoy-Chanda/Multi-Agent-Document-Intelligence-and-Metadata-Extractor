# Multi-Agent Document Intelligence & Metadata Extractor

An AI-powered web application designed to automatically read, classify, and extract structured data from unstructured documents (like Invoices, Contracts, and Technical Specifications) using a multi-agent workflow.

## Overview

This system utilizes Large Language Models (LLMs) via GitHub Models to comprehend uploaded PDF documents. It employs a graph-based multi-agent architecture (using LangGraph) where:
1. **Classifier Agent:** Reads the document and determines its type.
2. **Extractor Agent:** Dynamically extracts specific, structured metadata based on the document's classified type (e.g., extracting "Total Amount" and "Vendor" for an Invoice).

## Tech Stack

- **Frontend:** Angular (Modern UI, responsive data tables, asynchronous uploads)
- **Backend:** Python, FastAPI, Uvicorn
- **AI Orchestration:** LangGraph, LangChain, OpenAI Python SDK
- **LLM Inference:** GitHub Models (`gpt-4o-mini`)
- **PDF Parsing:** PyMuPDF (`fitz`)
- **Database:** MySQL

## Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js & npm** (for the frontend)
- **Python 3.9+** (for the backend)
- **MySQL Server**
- A valid **GitHub Personal Access Token** with access to GitHub Models.

## Setup Instructions

### 1. Database Setup
1. Ensure your local MySQL server is running.
2. Create the database and tables by running the initialization script located in the `database` folder:
   ```bash
   mysql -u root -p < database/init.sql
   ```

### 2. Backend Setup
1. Open a terminal and navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Activate the virtual environment:
   ```powershell
   # Windows
   .\venv\Scripts\Activate.ps1
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your environment variables. Create a `.env` file in the `backend` folder with the following contents:
   ```env
   OPENAI_API_KEY=your_github_pat_here
   DB_HOST=localhost
   DB_NAME=document_intelligence
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   ```
   *(Note: Never commit your `.env` file to version control!)*
5. Start the backend server:
   ```bash
   python main.py
   ```
   *The API will be available at http://localhost:8000*

### 3. Frontend Setup
1. Open a new terminal and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install the necessary Node modules:
   ```bash
   npm install
   ```
3. Start the Angular development server:
   ```bash
   npm start
   ```
4. Open your browser and navigate to `http://localhost:4200` to start extracting metadata!

## Security Note

Do not hardcode or commit API keys or database credentials to GitHub. Always use the `.env` file, and ensure `.gitignore` is properly configured to ignore it.
