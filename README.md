<h1 align="center">🧬 MedCOCO-Search</h1> <h2 align="center"><i>Context-Aware Medical Image Captioning & Retrieval using Multimodal AI</i></h2> <p align="center"> <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Badge"/> <img src="https://img.shields.io/badge/Backend-FastAPI-009688.svg" alt="FastAPI Badge"/> <img src="https://img.shields.io/badge/Frontend-Flutter-42A5F5.svg" alt="Flutter Badge"/> <img src="https://img.shields.io/badge/Database-ChromaDB-orange.svg" alt="ChromaDB Badge"/> <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License Badge"/> </p>
<h2>🩺 Overview</h2> <p align="justify"> <b>MedCOCO-Search</b> is an intelligent multimodal AI system for <b>semantic search and captioning of medical images</b> using <b>natural language queries</b>. It leverages <b>BLIP-2</b> and <b>MedCLIP</b> to bridge the gap between <b>medical vision</b> and <b>language understanding</b>, enabling users to explore medical datasets through descriptive text input. </p>

💬 <b>Example Queries:</b>
• “Show MRI scans showing brain tumor.”
• “Chest X-ray with pneumonia.”

<p align="justify"> The system retrieves <b>semantically similar images</b> and generates <b>AI-based medical captions</b> automatically — eliminating the need for manual labeling. </p>
<h2>💡 Key Features</h2>

🔍 Semantic Search: Query medical images using plain English.

🧠 Automatic Captioning: Generate clinically relevant image descriptions.

⚡ Multimodal Intelligence: Combines vision and text for contextual understanding.

🌐 Fast & Scalable: Built with FastAPI and ChromaDB for real-time similarity search.

<h2>Dataset</h2>

ROCO (Radiology Objects in Context)

📸 Over 81,000 radiology images paired with captions.

- Includes modalities such as X-ray, CT, MRI, and Ultrasound.

• Ideal for multimodal AI tasks like retrieval, captioning, and diagnosis support.

<h2>🧩 Technology Stack</h2> <table> <tr> <th style="text-align:center;">Layer</th> <th style="text-align:center;">Technology</th> <th style="text-align:center;">Description</th> </tr> <tr> <td><b>AI Models</b></td> <td>MedCLIP, BLIP-2</td> <td>Medical vision-language understanding and caption generation</td> </tr> <tr> <td><b>Backend</b></td> <td>FastAPI (Python)</td> <td>High-performance REST API for model inference and requests</td> </tr> <tr> <td><b>Database</b></td> <td>ChromaDB</td> <td>Vector storage and similarity search for image-text embeddings</td> </tr> <tr> <td><b>Frontend</b></td> <td>Flutter (Dart)</td> <td>Modern cross-platform interface for search and results</td> </tr> <tr> <td><b>Storage</b></td> <td>SQLite</td> <td>Efficient local caching and lightweight data persistence</td> </tr> </table>
<h2>🎯 Objectives</h2>

Build a natural language–driven retrieval system for large-scale medical image datasets.

Generate accurate, context-aware medical captions to assist radiologists and researchers.

Explore multimodal AI applications in healthcare, education, and diagnostics.

Deliver a scalable full-stack AI architecture adaptable to real-world medical systems.

<h2>🧬 Example Query</h2>

- User Query: “X-ray showing bone fracture.”

🤖 System Output:
• Displays top visually and semantically similar medical images.
• AI Caption: “X-ray of a fractured tibia bone.”

<h2>License</h2>

This project is licensed under the MIT License —
You are free to use, modify, and distribute it for research and educational purposes.

<h2>🌐 Acknowledgements</h2>

🧬 ROCO Dataset
 — Radiology Objects in Context

🤖 Salesforce BLIP-2
 — Vision-language captioning model

🔍 MedCLIP
 — Medical image-text embedding model

🗃️ ChromaDB
 — Open-source vector database for embeddings

<p align="center"> <i>Developed as part of the October 6 University Graduation Project 2025–2026.</i><br/> <b>MedCOCO-Search — Empowering Medical AI through Vision and Language.</b> </p>
