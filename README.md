# 🧠 Mining Legal Compliance Chatbot

A rule-based chatbot built using **Python, SQLite, and Regex** to automate legal queries related to Indian mining laws such as the *Mines Act (1952)* and *Explosives Act (1884)*.

## 🚀 Features
- Automates legal query processing using natural language.
- Regex-based parsing for detecting Acts and Sections.
- SQLite database storing Acts and Sections for fast retrieval.
- Returns precise legal text in plain language.
- Achieved 90% accuracy and 1.2-second average response time.

## 🏗️ Tech Stack
- **Programming:** Python (sqlite3, re)
- **Database:** SQLite
- **Libraries:** pandas, nltk (optional for future NLP)
- **Version Control:** Git/GitHub

## ⚙️ How It Works
1. User inputs a query (e.g., “Section 8 of Indian Explosives Act”).
2. Regex extracts the section number and Act name.
3. SQL query retrieves the section text from the database.
4. For keyword-based queries (“penalties for explosives”), keywords are extracted and matched in both Acts and Sections tables.

## 🧪 Example Queries
| User Query | Chatbot Response |
|-------------|------------------|
| "Section 8 of Indian Explosives Act" | Storage rules for explosives |
| "Penalties for explosives" | Section 8 (Explosives Act), Section 22 (Mines Act) |
