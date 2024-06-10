Welcome to the Note Processing Script! This project helps you process markdown notes by generating YAML front matter based on the content of those notes using a language model.

## Description

This project provides tools to read markdown notes and generate YAML front matter for each note based on its content. It uses a language model to infer relationships and metadata, making it ideal for organizing notes in Obsidian or other note-taking systems.

## Installation

Ensure you have [VS Code](https://code.visualstudio.com/) and the latest version of [Python](https://www.python.org/downloads/) installed.

You will also need to download [LM Studio](https://www.lm-studio.com/). This code uses local models to generate the YAML front matter, which means you will need to download a model and identify it in the code. A GPU capable of running the model locally is required.

### Step 1: Get the Code into VS Code

To get started, choose one of the following:

- **Clone the Repository**: Open a new window in VS Code (File > New Window) and paste the below link into the top search bar that pops up:
  ```
  https://github.com/ProfSynapse/Obsidian_Properties.git
  ```

- **Download the ZIP Version**: Click "Code" in the top right of the GitHub page and select "Download ZIP". Uncompress and save to a folder you have easy access to. In VS Code, open a new folder (File > Open Folder) and open the folder containing the code.

  **Note**: Ensure the folder structure is correct (i.e., the `Obsidian_Properties` folder should not be nested inside another folder with the same name).

### Step 2: Set Up a Virtual Environment in VS Code

Open a new terminal in VS Code (Terminal > New Terminal), and type:
```bash
python -m venv myenv
```
Press Enter/Return.

Then activate the virtual environment:

- For macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- For Windows:
  ```bash
  venv\Scripts\activate
  ```

### Step 3: Install Dependencies

In the terminal, type:
```bash
pip install -r requirements.txt
```

### Step 4: Choose Your Model

Download your preferred model in LM Studio and open the local server tab (it looks like ⬅️➡️).
- Set your context length.
- Ensure GPU Offload is on and set it in a way that works for your specs.
- Note the server port (likely 1234) and ensure it matches the code configuration:
  ```python
  url = "http://localhost:1234/v1/chat/completions"
  ```
- Ensure the model name in the code matches the model you chose in LM Studio. For example:
  ```python
  "model": "bartowski/Phi-3-medium-128k-instruct-GGUF"
  ```

### Step 5: Find the Path to Your Notes

Ensure you have markdown notes (.md files) you want to process. Update the path in the script where it says:
```python
notes_directory = "G:/My Drive/Professor Synapse"
```
Replace with your actual path, e.g., `C:/Users/Name/Documents/My Vault`.

### Step 6: Run the Main Script

Execute the main script to process the notes.

In your terminal, type:
```bash
python frontmatter.py
```

You can watch it process the notes and generate the front matter.

### Step 7: Check the Output

The script updates each note with the generated YAML front matter. You can open the markdown files to see the added front matter at the top of each note.

---

## Files

- **`frontmatter.py`**: Main script that processes the notes.
- **`requirements.txt`**: Lists the dependencies needed to run the script.

---

## Example

Given a note with the following content:
```
# Quantum Mechanics
Quantum mechanics is a fundamental theory in physics that describes the physical properties of nature at the scale of atoms and subatomic particles.
```

The script will generate and add the following front matter:
```yaml
---
title: Quantum Mechanics
description: Fundamental theory in physics that describes the nature of matter and energy at the atomic and subatomic levels.
type: concept
tags: [Physics, Science, Quantum Theory]
relationships:
- "#developed_by [[Max Planck]], [[Werner Heisenberg]], [[Erwin Schrödinger]]"
- "#explains [[Wave-Particle Duality]], [[Uncertainty Principle]]"
- "#applies_to [[Atoms]], [[Molecules]], [[Subatomic Particles]]"
- "#differs_from [[Classical Mechanics]]"
---
```
