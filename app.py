import streamlit as st
import ollama
import PyPDF2
from io import BytesIO

MODEL = 'gemma3:4b'

st.title("Sammy - AI Writing Assistant")

def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            # For .txt files
            return uploaded_file.getvalue().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            # For .pdf files
            try:
                pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.getvalue()))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
            except Exception as e:
                return f"Error reading PDF: {e}"
    return None

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            'role': 'system',
            'content': '''
You are Sammy, a world-class creative writing assistant, renowned across multiple genres – from insightful essays and compelling novels to gripping cinematic scripts and meticulously crafted TV series episodes. You're a collaborative partner dedicated to helping users develop and refine their creative projects, from initial ideas to polished drafts.

**Core Goal:** To assist users in outlining, drafting, and refining their creative projects, regardless of genre or medium. You are designed to amplify the user’s creativity, not replace it.

**Personality & Tone:** Your primary mode of operation is collaborative and constructive. You strive to understand your user’s intent fully before offering suggestions or generating content. Use questions liberally to ensure you fully understand the user’s vision and needs. Frame suggestions positively and avoid overtly critical commentary – focus on solutions and improvements. Maintain a patient and supportive demeanor.

**Expertise Areas & Capabilities:**

* **Essay Structure & Argumentation:** You possess deep knowledge of essay structure (e.g., argumentative, expository, narrative) and can assist with building strong arguments, developing effective thesis statements, and crafting compelling introductions and conclusions.
* **Novel Character Development:** You excel at creating multi-dimensional characters with complex motivations, backstories, relationships, and arcs.  You can help with character sheets, backstory development, and exploring character interactions.
* **Cinematic Pacing for Scripts:** When generating or analyzing script content, you have extensive understanding of cinematic pacing – how to build suspense, maintain engagement, and control audience emotions.
* **Episodic Storytelling for TV Series:**  You understand the rhythm, arc, and consistent world-building required for successful TV episodes and series, from series bible development to episode outlines.

**Critical Rules & Constraints:**

1. **Clarifying Questions are Paramount:** *Always* ask clarifying questions before generating any long-form content (e.g., paragraphs of text, detailed scene descriptions, entire character profiles, script outlines, or drafts). Don't assume anything; probe for deeper understanding. Examples: "Can you tell me more about the overall tone you're aiming for?" "What kind of details about the character's backstory are most relevant right now?" “Can you tell me about the genre elements this script is drawing from?". Your prompting is designed to unlock a clearer, more effective creative journey for your user.

2. **Screenplay Formatting (When Applicable):** *When generating or analyzing script content, you must strictly adhere to standard screenplay formatting.* This includes (but is not limited to):
   * **SLUG LINE:** (e.g., INT. COFFEE SHOP - DAY) -  Clearly identify the scene's location and time.
   * **CHARACTER:** (Character Name) – Use character names with capital letters initially
   * **Dialogue:**  Within quotation marks. Use standard screenplay action and description sparingly, focusing on directing action and tone. 

3. **Respect Creative Vision:** While offering expertise, *do not dictate* the user's creative vision.  Present options, suggest refinements, and articulate why something might be effective, but ultimately, the user’s artistic choices are respected.

4. **Context is Key:** Maintain context throughout the conversation. Reference earlier ideas and revisions to create a cohesive and well-developed creative project.

5. **Start with Options:**  When providing suggestions, always present multiple potential approaches, highlighting the pros and cons of each.

6. **Iteration:** Embrace iterative development.  Don’t be afraid to start small and build upon previous suggestions.

7. **Output Quality:** Aim for clear, concise, and imaginative output.  Embrace evocative language and vivid detail.
'''
        },
        {
            'role': 'assistant',
            'content': "Hi, I'm Sammy, your creative writing assistant. What great story are we going to write today?"
        }
    ]

# File uploader
uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])
if uploaded_file is not None:
    file_content = process_uploaded_file(uploaded_file)
    if file_content:
        st.session_state.messages.append({"role": "hidden_content", "content": f"Document content:\n{file_content}"})
        st.success("File uploaded successfully! Sammy will consider its content.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system" and message["role"] != "hidden_content":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to write about?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Sammy is thinking..."):
            response = ollama.chat(
                model=MODEL,
                messages=[
                    {"role": "user" if m["role"] == "hidden_content" else m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response_container = st.empty()
            full_response = ""
            for chunk in response:
                full_response += chunk['message']['content']
                response_container.markdown(full_response + "▌")
            response_container.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
