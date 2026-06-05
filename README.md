<h1 align="center">🧬 MedCOCO-Search</h1>
<h2 align="center"><i>AI-Powered Medical Imaging Search & Captioning Platform</i></h2>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688.svg" alt="FastAPI Badge"/>
  <img src="https://img.shields.io/badge/Frontend-Flutter-42A5F5.svg" alt="Flutter Badge"/>
  <img src="https://img.shields.io/badge/Database-ChromaDB-orange.svg" alt="ChromaDB Badge"/>
  <img src="https://img.shields.io/badge/AI-MedCLIP%20%7C%20BLIP--2-purple.svg" alt="AI Badge"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License Badge"/>
</p>

<p align="center">
  Upload X-ray, MRI, CT images &nbsp;•&nbsp; Search with natural language &nbsp;•&nbsp; AI-generated captions &nbsp;•&nbsp; For doctors & students
</p>

---

## 📋 Overview

**MedCOCO-Search** is an intelligent multimodal AI system for **semantic search and automatic captioning of medical images** using **natural language queries**. It leverages **BLIP-2** and **MedCLIP** to bridge the gap between medical vision and language understanding, enabling healthcare professionals and medical students to explore large radiology datasets through simple descriptive text.

The system retrieves semantically similar images and generates AI-based medical captions automatically — eliminating the need for manual labeling.

### 💬 Example Queries

```
"Show MRI scans showing brain tumor."
"Chest X-ray with pneumonia."
"X-ray showing bone fracture."
```

**System Output:**
- Displays top visually and semantically similar medical images
- AI Caption: *"X-ray of a fractured tibia bone."*

---

## ✨ Key Features

- 🔍 **Semantic Search** — Query medical images using plain English, no tags or metadata needed
- 🧠 **Automatic Captioning** — Generate clinically relevant image descriptions via BLIP-2
- ⚡ **Multimodal Intelligence** — Combines MedCLIP vision and text encoders for contextual understanding
- 🩻 **Medical Image Upload** — Upload X-ray, MRI, and CT raw images securely
- 🌐 **Fast & Scalable** — Built with FastAPI and ChromaDB for real-time similarity search
- 🔐 **Secure Authentication** — Multi-factor authentication with OTP verification
- 📱 **Cross-Platform** — Runs on mobile, desktop, and web via Flutter

---

---

## 🧩 Technology Stack

### AI / ML

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Vision-Language Model | **MedCLIP** | Medical image-text embedding for semantic search |
| Caption Generation | **MedBLIP (BLIP-2)** | Automatic clinical caption generation |
| Vector Search | **ChromaDB** | Embedding storage and similarity search |

### Backend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| API Framework | **FastAPI (Python 3.10+)** | High-performance REST API for model inference |
| Local Storage | **SQLite** | Lightweight data persistence and caching |

### Frontend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Mobile & Desktop App | **[Flutter (Dart)](https://github.com/Marwan9Atef/MedCocoApp)** | Cross-platform UI for mobile, desktop, and web |

### Dataset

**ROCO — Radiology Objects in Context**
- 📸 Over 81,000 radiology images paired with captions
- Includes modalities: X-ray, CT, MRI, and Ultrasound
- Ideal for multimodal AI tasks: retrieval, captioning, and diagnosis support

---

## 🏗 Architecture

### System Architecture

```
┌─────────────────────────────────────┐
│          Flutter Frontend           │
│  (Mobile / Desktop / Web Client)    │
└──────────────┬──────────────────────┘
               │ REST API (HTTP)
┌──────────────▼──────────────────────┐
│         FastAPI Backend             │
│  (Model Inference & API Routing)    │
└──────────┬───────────┬──────────────┘
           │           │
┌──────────▼──┐  ┌─────▼──────────────┐
│  MedCLIP /  │  │    ChromaDB        │
│   BLIP-2    │  │  (Vector Search)   │
│  AI Models  │  │                    │
└─────────────┘  └────────────────────┘
```

---

## 📁 Project Structure

```
MedCOCO-Search/
├── backend/                          # Python FastAPI backend
│   ├── models/                       # MedCLIP & BLIP-2 model wrappers
│   ├── routes/                       # API route handlers
│   ├── services/                     # Search, caption, embedding services
│   ├── database/                     # ChromaDB & SQLite setup
│   └── main.py                       # FastAPI entry point
│
└── frontend/                         # → See github.com/Marwan9Atef/MedCocoApp
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **Flutter SDK** — [flutter.dev](https://docs.flutter.dev/get-started/install) *(for running the mobile/desktop app)*
- **Git** — [git-scm.com](https://git-scm.com/)

---

### 1. Clone the Repository

```bash
git clone https://github.com/Zarathos01/MedCOCO-Search.git
cd MedCOCO-Search
```

---

### 2. Backend Setup (FastAPI + AI Models)

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

> **Note:** The first run will download the MedCLIP and BLIP-2 model weights automatically. This may take several minutes depending on your internet connection.

**Start the backend server:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.  
Interactive API docs: `http://localhost:8000/docs`

---

### 3. Frontend Setup (Flutter Mobile/Desktop App)

The frontend application lives in a separate repository:

> 📱 **[https://github.com/Marwan9Atef/MedCocoApp](https://github.com/Marwan9Atef/MedCocoApp)**

```bash
git clone https://github.com/Marwan9Atef/MedCocoApp.git
cd MedCocoApp

flutter pub get
flutter run
```

> **Note:** Make sure the backend is running before launching the app. Refer to the app repo's README for any additional setup steps.

---

### 4. Environment Configuration

Create a `.env` file in the `backend/` directory (if required by the project):

```env
CHROMA_DB_PATH=./chroma_store
SQLITE_DB_PATH=./medcoco.db
MODEL_CACHE_DIR=./model_cache
```

---

## 🎯 How It Works

1. **Upload** — A user uploads a medical image (X-ray, MRI, CT) through the mobile/desktop app
2. **Embed** — The backend passes the image through **MedCLIP** to generate a vector embedding
3. **Store** — The embedding and image metadata are stored in **ChromaDB**
4. **Search** — A user types a natural language query (e.g., *"chest X-ray with pneumonia"*)
5. **Retrieve** — The query is encoded and matched against stored embeddings via cosine similarity
6. **Caption** — **BLIP-2** generates a clinically relevant caption for the retrieved images
7. **Display** — Results are shown ranked by semantic similarity in the app UI

---

## 🧬 Dataset

This project uses the **ROCO (Radiology Objects in Context)** dataset:

- 📸 81,000+ radiology images with paired captions
- Modalities: X-ray, CT, MRI, Ultrasound
- Sourced from open-access medical literature

To prepare the dataset, follow the instructions in `backend/data/README.md` (if included), or download ROCO from its [official source](https://github.com/razorx89/roco-dataset).

---

---

## 📜 License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it for research and educational purposes.

---

## 🌐 Acknowledgements

- 📱 [MedCocoApp](https://github.com/Marwan9Atef/MedCocoApp) — Flutter frontend application
- 🧬 [ROCO Dataset](https://github.com/razorx89/roco-dataset) — Radiology Objects in Context
- 🤖 [MedBLIP](https://github.com/Qybc/MedBLIP) — Medical vision-language captioning model
- 🔍 [MedCLIP](https://github.com/RyanWangZf/MedCLIP) — Medical image-text embedding model
- 🗃️ [ChromaDB](https://www.trychroma.com/) — Open-source vector database for embeddings
- ⚡ [FastAPI](https://fastapi.tiangolo.com/) — Modern Python web framework
- 📱 [Flutter](https://flutter.dev/) — Cross-platform UI toolkit

---

<div align="center">
  <p><i>Developed as part of the October 6 University Graduation Project 2025–2026.</i></p>
  <b>MedCOCO-Search — Empowering Medical AI through Vision and Language.</b>
  <br/><br/>
  Built with ❤️ using Python & Flutter &nbsp;•&nbsp; <a href="#-medcoco-search">⬆ Back to Top</a>
</div>