import streamlit as st
import os

st.title("Persona Adaptive Support Agent")

msg = st.text_input("Ask Question")

def detect_persona(message):
    msg = message.lower()

    if any(word in msg for word in
           ["api", "log", "authentication", "config", "error"]):
        return "Technical Expert"

    elif any(word in msg for word in
             ["angry", "frustrated", "worst", "nothing works", "urgent"]):
        return "Frustrated User"

    else:
        return "Business Executive"

def search_documents(query):
    data_folder = "data"

    for file in os.listdir(data_folder):
        path = os.path.join(data_folder, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

            if any(word.lower() in content.lower()
                   for word in query.split()):
                return file, content

    return None, None

if msg:

    persona = detect_persona(msg)

    source, content = search_documents(msg)

    st.subheader("Detected Persona")
    st.write(persona)

    if source:

        st.subheader("Retrieved Source")
        st.write(source)

        if persona == "Technical Expert":
            response = f"""
Technical Details:

Based on {source}

{content[:500]}
"""

        elif persona == "Frustrated User":
            response = f"""
I understand your frustration.

Please follow these steps:

{content[:500]}
"""

        else:
            response = f"""
Business Summary:

Issue information from {source}

{content[:500]}
"""

        st.subheader("Response")
        st.write(response)

        st.subheader("Escalation Status")
        st.success("No Escalation Required")

    else:

        st.subheader("Escalation Status")
        st.error("Escalated To Human Support")

        st.json({
            "persona": persona,
            "issue": msg,
            "recommendation": "Human review required"
        })