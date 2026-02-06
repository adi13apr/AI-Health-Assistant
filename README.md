# 🩺 AI Health Assistant

An AI-powered health insights application that analyzes medical blood reports and provides structured, easy-to-understand health interpretations using LLM-based intelligence.

## 🚀 Overview

AI Health Assistant is a healthcare-focused intelligent system designed to help users interpret blood test reports. It extracts medical parameters from uploaded PDFs and generates personalized health insights using AI models.

This project demonstrates practical implementation of:

* AI-driven report analysis
* Multi-model response architecture
* Secure authentication
* Healthcare data handling

## 🌟 Key Features

* 📄 Upload and analyze blood reports (PDF)
* 🤖 AI-generated health insights
* 🧠 Multi-model fallback system for reliable responses
* 🔐 User authentication & session management
* 📊 History tracking of previous analyses
* ⚡ Responsive Streamlit-based interface

## 🛠️ Tech Stack

**Frontend**

* Streamlit

**Backend & AI**

* Python
* Groq LLM API
* Multi-model orchestration

**Database**

* Supabase

**Processing**

* PDFPlumber for report text extraction

## 📁 Project Structure

```
src/
 ├── main.py
 ├── agents/
 ├── services/
 ├── auth/
 ├── components/
 └── utils/
```

## ⚙️ Installation

### Requirements

* Python 3.8+
* Streamlit
* Supabase account
* Groq API key

### Steps

1. Clone the repository:

```
git clone https://github.com/adi13apr/AI-Health-Assistant.git
cd AI-Health-Assistant
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Add environment variables in:

```
.streamlit/secrets.toml
```

4. Run the app:

```
streamlit run src/main.py
```

## 💡 Learning Outcomes

Through this project, I worked on:

* AI integration in real-world healthcare use cases
* LLM prompt engineering
* Multi-agent response orchestration
* Secure session handling
* Medical data interpretation pipelines

## 🔮 Future Improvements

* Add ML-based disease risk prediction
* Deploy on cloud for public access
* Add chatbot-based symptom assistant
* Improve UI/UX

## 📌 Project Purpose

This project was developed to explore the application of AI in healthcare analytics and to build a system capable of assisting users in understanding complex medical reports.

## 👨‍💻 Developer

Aditya Chauhan
B.Tech | AI & ML Enthusiast
