import sqlite3
import re

# Step 1: Database Connection
def create_connection():
    """Connect to SQLite database."""
    return sqlite3.connect('laws.db')

# Step 2: Database Query Functions (unchanged)
def get_all_acts():
    """Get list of all Acts from the database."""
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM acts")
        return [row[0] for row in cursor.fetchall()]

def get_sections_by_keyword(keyword: str) -> list:
    """Get sections matching a specific keyword."""
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
    SELECT acts.name, sections.section_number, sections.description 
    FROM acts 
    JOIN sections ON acts.id = sections.act_id 
    WHERE LOWER(acts.keywords) LIKE LOWER('%' || ? || '%') 
    OR LOWER(acts.name) LIKE LOWER('%' || ? || '%')
''', (keyword.strip(), keyword.strip()))
        return cursor.fetchall()

def get_act_by_keyword(keyword: str) -> list:
    """Get Acts and sections matching a keyword."""
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT acts.name, sections.section_number, sections.description 
            FROM acts 
            JOIN sections ON acts.id = sections.act_id 
            WHERE LOWER(acts.keywords) LIKE LOWER('%' || ? || '%')
        ''', (keyword.strip(),))
        return cursor.fetchall()

# Helper function to get act summary
def get_act_summary(act_name: str) -> str:
    """Get summary of an Act from the database."""
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT summary FROM acts WHERE name = ?', (act_name,))
        result = cursor.fetchone()
        return result[0] if result else "No summary available."

# Step 3: Chatbot Logic (UPDATED WITH SUMMARIES)
def get_legal_response(query: str) -> str:
    query = query.lower()
    
    # Handle section queries
    if "section" in query:
        match = re.search(r'section\s+(\d+[A-Za-z]*)\s+of\s+(.*?)\s+act', query)
        if match:
            section_num = match.group(1).strip()
            act_name = f"%{match.group(2).strip()}%"
            with create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT acts.name, sections.section_number, sections.description 
                    FROM acts 
                    JOIN sections ON acts.id = sections.act_id 
                    WHERE LOWER(acts.name) LIKE LOWER(?) AND sections.section_number = ?
                ''', (act_name, section_num))
                result = cursor.fetchone()
                if result:
                    act, section, desc = result
                    summary = get_act_summary(act)
                    return f"{act}, Section {section}:\n{desc}\n\n--- Summary ---\n{summary}"
                else:
                    return "Section not found. Check the Act name and section number."
        else:
            return "Specify section properly, e.g., 'Section 8 of Indian Explosives Act'."
    
    # Handle keyword-based queries
    keywords = re.findall(r'\b\w+\b', query)
    section_results = []
    act_results = []
    
    for keyword in keywords:
        sections = get_sections_by_keyword(keyword)
        if sections:
            section_results.extend((keyword, act, section, desc) for (act, section, desc) in sections)
        acts = get_act_by_keyword(keyword)
        if acts:
            act_results.extend((keyword, act, section, desc) for (act, section, desc) in acts)
    
    # Build response
    response = []
    for kw, act, sec, desc in section_results:
        response.append(f"{act}, Section {sec} ({kw.capitalize()}):\n{desc}")
    for kw, act, sec, desc in act_results:
        response.append(f"{act}, Section {sec} (Act Keyword: {kw.capitalize()}):\n{desc}")
    
    if response:
        # Collect unique Acts and add summaries
        unique_acts = {act for _, act, _, _ in section_results + act_results}
        summaries = [f"--- {act} Summary ---\n{get_act_summary(act)}" for act in unique_acts]
        return "\n\n".join(response + ["\n".join(summaries)])
    
    # Fallback
    return """I can help with queries about mining laws. Try:
- 'Section 8 of Indian Explosives Act'
- 'Safety regulations in Coal Mines Act'
- 'Production quotas'"""

# Step 4: User Interface (unchanged)
print("Mining Legal Chatbot: Ask about Acts, Rules, or Regulations (type 'exit' to quit)")
while True:
    user_input = input("\nYour query: ").strip()
    if user_input.lower() == "exit":
        print("Goodbye! Stay compliant!")
        break
    response = get_legal_response(user_input)
    print("\nChatbot:", response)