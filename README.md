# Sammy - AI Writing Assistant

![Under Development](https://img.shields.io/badge/Status-Under%20Development-orange.svg)

## Project Overview

Sammy is an intelligent AI writing assistant designed to help users outline, draft, and refine their creative projects across various genres, including essays, novels, cinematic scripts, and TV series episodes. Sammy aims to be a collaborative partner, enhancing the user's creativity rather than replacing it.

## Features

- **Multi-genre Expertise:** Sammy is proficient in assisting with different writing forms, from academic essays to complex screenplays.
- **Collaborative Approach:** The assistant is designed to ask clarifying questions, offer constructive feedback, and present multiple options to align with the user's creative vision.
- **File Uploads:** Users can upload `.txt` or `.pdf` files, and Sammy will process their content to provide context-aware assistance.
- **Streamlined UI:** A clean and intuitive chat interface built with Streamlit.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.9+
- `ollama` (for running the language model locally)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sammy_AI_writing_assistant.git
   cd sammy_AI_writing_assistant
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure `ollama` is running and the `gemma3:4b` model is downloaded:
   ```bash
   ollama run gemma3:4b
   ```

### Running the Application

Once the prerequisites are met and `ollama` is running with the specified model, you can start the Streamlit application:

```bash
streamlit run app.py
```

This will open the Sammy AI Writing Assistant in your web browser.

## Development Status

This project is currently in active development. Features, design, and documentation (including this `README.md` file) are subject to change.

## Contributing

We welcome contributions! If you're interested in helping improve Sammy, please consider the following:

- **Reporting Bugs:** If you find any issues, please report them.
- **Suggesting Features:** Have an idea for a new feature? Let us know!
- **Code Contributions:** Feel free to fork the repository and submit pull requests.
