# 🤖 AI Assistant for Internal Project Managers

This project is a Streamlit-based GPT-powered tool that assists internal project managers with document summarization, task generation, chat-based guidance, and real-time feedback collection. It helps streamline communication, improve task clarity, and visualize assistant performance.

---

## 🔍 Problem Statement

Internal project managers often juggle multiple tasks — from reporting and documentation to stakeholder updates and sprint planning. They need quick access to synthesized project insights and reliable guidance without combing through lengthy files or scattered notes.

This project answers:

- How can PMs quickly summarize key project documents?
- How can action items be automatically extracted from updates?
- Can an AI assistant consistently support project-related questions?
- How useful is the assistant’s output over time?

---

## 📦 Files & Features

Core Features Included:

- `main.py`: Full Streamlit app source code
- `feedback_log.csv`: Captures feedback on each AI response
- 🧠 **AI Chat Assistant** with chat history
- 📄 **PDF Summarization** with PyMuPDF
- ✅ **Task Generator** from AI summaries
- 📣 **Feedback Loop** (👍 / 👎 + comments)
- 📊 **Performance Dashboard** with history display

---

## 🛠️ Tools & Technologies

- **Streamlit** – web UI framework  
- **OpenAI GPT-3.5** – language model API  
- **PyMuPDF (fitz)** – PDF parsing  
- **Pandas** – data collection + feedback log  
- **Python** – app logic and orchestration  

---

## ⚙️ How It Works

### 1. Upload and Summarize PDFs
- PM uploads a project document
- App extracts all page text using `fitz`
- GPT-3.5 condenses it into a manager-friendly summary

### 2. Task Generator
- A “Generate Tasks” button uses the summary
- GPT returns bullet-pointed, actionable project steps

### 3. AI Chat Assistant
- PMs type questions like “How do I write a status update?”
- Responses are contextual and logged in the session
- Each response stored with timestamp for review

### 4. Feedback Collection
- After each answer, PM gives 👍 or 👎
- Optional comment box for improvement ideas
- Feedback saved to `feedback_log.csv`

### 5. History & Dashboard
- App maintains a full chat history
- Users can view all past questions, answers, and feedback
- Data table view for dashboard integration later

---

## 📈 Sample Output

Sample question:  
**"How do I write a stakeholder report?"**

AI Output:
> To write a stakeholder report, follow these steps:  
> 1. Identify stakeholders  
> 2. Define the report’s purpose  
> 3. Gather progress data  
> 4. Structure updates clearly  
> 5. Use simple, direct language  
> 6. Share and collect feedback  

---

## ✅ Business Value

📋 Helps PMs respond faster with AI summaries  
⚡ Speeds up task planning via GPT task extraction  
💬 Provides 24/7 internal assistance for project-related queries  
📊 Enables performance tracking of AI outputs  
📁 Reduces time spent reading lengthy reports

---

## 🚀 Future Work

🧾 Add export to Notion or Confluence  
🔐 Support multiple users with login and private chat logs  
📦 Switch to SQLite or Supabase for scalable feedback storage  
🧠 Integrate with scheduling tools like Asana or ClickUp  
📊 Auto-generate charts from PDFs for reporting

---

## 👨‍💻 Author

**Nithin Sai Adru**  
📧 nithin.adru@email.ucr.edu
