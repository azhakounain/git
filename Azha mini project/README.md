# 📄 AI Resume Analyzer

A beginner-friendly Python application that analyzes PDF resumes and provides an **ATS (Applicant Tracking System) score**, detects **technical skills**, and gives **improvement suggestions**.

Built with **Streamlit**, **pdfplumber**, and pure Python — no AI API keys required!

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or above installed on your system.

### Installation

```bash
# 1. Clone or download this project
cd "Azha mini project"

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
Azha mini project/
├── app.py              # Main Streamlit web application
├── resume_parser.py    # Extracts text from PDF files
├── analyzer.py         # Skill detection, ATS scoring, suggestions
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation (this file)
```

---

## 🖥️ Example Output

After uploading a sample software-developer resume:

```
ATS Score: 58 / 100  — Average

Detected Skills:
  Programming Languages : Python, Java, JavaScript
  Web Development       : HTML, CSS, React, Node.js
  Databases             : SQL, MongoDB

Improvement Suggestions:
  📌 Add Data Science & AI skills (e.g., Machine Learning, Deep Learning).
  📌 Add Cloud & DevOps skills (e.g., AWS, Docker).
  💡 Include a Projects section to showcase hands-on experience.
  📝 Use a clean, ATS-friendly resume format.
  🎯 Tailor your resume to each job description.
```

---

## ✨ Features

| Feature | Description |
|---|---|
| PDF Parsing | Extracts text from uploaded PDF resumes |
| Skill Detection | Matches 60+ technical & soft skills across 6 categories |
| ATS Scoring | Calculates a 0–100 score based on skills & category coverage |
| Suggestions | Actionable tips to improve your resume |
| Modern UI | Dark-themed Streamlit interface with badges & progress bars |

---

## 🔮 Future Improvements

- **AI-Powered Analysis** — Integrate OpenAI / Gemini API for deeper resume insights.
- **Job Description Matching** — Compare resume against a specific job posting for a tailored score.
- **Multiple File Formats** — Support DOCX and plain text uploads.
- **Experience & Education Parser** — Extract work history and degrees using NLP (spaCy).
- **Export Report** — Generate a downloadable PDF report of the analysis.
- **User Accounts** — Save analysis history with a simple database (SQLite / Firebase).
- **Deployment** — Host on Streamlit Community Cloud for free public access.

---

## 🛠️ Technologies Used

- **Python 3** — Core programming language
- **Streamlit** — Web interface framework
- **pdfplumber** — PDF text extraction

---

## 📜 License

This project is open-source and available for educational purposes. Feel free to modify and use it for your internship or portfolio!
