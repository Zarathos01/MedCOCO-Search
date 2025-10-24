# MedCOCO-Search
🧬 MedCOCO-Search

Context-Aware Medical Image Captioning & Retrieval using Multimodal AI

🩺 Overview

MedCOCO-Search is an intelligent multimodal AI system that allows semantic search and captioning of medical images using natural language.
Built upon BLIP-2 and MedCLIP, it bridges the gap between text and visual medical data, enabling users to search massive image collections like:

🗣️ “Show MRI scans showing brain tumor.”
🗣️ “Chest X-ray with pneumonia.”

The system returns semantically similar images and AI-generated medical captions without manual tagging or metadata.

💡 Key Features

✅ Semantic Search: Query medical images using plain English.
✅ Automatic Captioning: Generate accurate medical image descriptions.
✅ Multimodal AI: Combines vision and language models for contextual understanding.
✅ Fast & Scalable: Built with FastAPI and ChromaDB for efficient search.
✅ Cross-Platform: Modern Flutter frontend for mobile, web, and desktop.

🧠 Dataset

ROCO (Radiology Objects in Context)

81,000+ radiology images paired with natural language captions.

Includes multiple modalities (X-ray, CT, MRI, Ultrasound, etc.).

Suitable for training and evaluating image–text understanding models.

🧩 Technology Stack
Layer	Technology	Description
AI Models	MedCLIP, BLIP-2	Vision-language understanding & caption generation
Backend	FastAPI (Python)	REST API for model serving and search logic
Database	ChromaDB	Vector-based embedding storage and retrieval
Frontend	Flutter (Dart)	Cross-platform mobile & web interface
Storage	SQLite	Lightweight on-device caching for user data
🚀 Project Objectives

Enable natural language search through large-scale medical image datasets.

Generate contextually relevant captions for unlabeled medical images.

Evaluate the effectiveness of multimodal AI in the healthcare domain.

Demonstrate a scalable and practical full-stack AI architecture for real-world use.

🧬 Example Query

User Query: “X-ray showing bone fracture.”
Result:

Displays the top similar radiology images.

Caption: “X-ray of a fractured tibia bone.”

🧾 License

This project is licensed under the MIT License — you are free to use, modify, and distribute it for research or educational purposes.

🌐 Acknowledgements

ROCO Dataset – Radiology Objects in Context (roco-dataset.org)

Salesforce BLIP-2 – Image captioning and vision-language understanding

MedCLIP – Foundation model for medical image-text alignment

ChromaDB – Open-source vector database for embedding retrieval
