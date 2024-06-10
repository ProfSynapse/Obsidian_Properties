import os
import requests
import json
import re

# Specify the directory containing the notes
notes_directory = "C:/Users/Joseph/Documents/Professor Synapse_6.2.24/02 - 🚀 Learning/🏺 History and Culture/Art"

# Prompt for generating front matter
front_matter_prompt = """
# MISSION
Act as an expert in YAML, specializing in Obsidian's front matter by inferring relationships from the note content. Your job is to take the content of a note, and generate the front matter in the EXPLICIT way as defined in this prompt.

# INSTRUCTIONS
1. Review the provided content by the user.
2. Review the ONTOLOGY and EXAMPLES
3. Output ONLY the YAML front matter, nothing before or after, adhering STRICTLY to the ONTOLOGY and EXAMPLE format.

# ONTOLOGY
Use the standardized ontology of relationship types and structure your output as follows:

### Hierarchical Relationships
1. `#is_a`: Indicates that the subject is a subtype or instance of the object
2. `#part_of`: Indicates that the subject is a component or subset of the object
3. `#has_part`: Inverse of `#part_of`, indicates the object is a component of the subject

### Associative Relationships
* `#related_to`: Indicates a general association or connection between the subject and object
* `#similar_to`: Indicates that the subject and object share common characteristics
* `#different_from`: Indicates a distinction or contrast between the subject and object

### Causal Relationships
* `#causes`: Indicates that the subject brings about or triggers the object
* `#caused_by`: Inverse of `#causes`, indicates the object is the cause of the subject
* `#enables`: Indicates that the subject makes the object possible or facilitates it
* `#prevents`: Indicates that the presence of the subject stops the object from happening

### Temporal Relationships
* `#before`: Indicates that the subject precedes the object in time
* `#after`: Indicates that the subject follows the object in time
* `#during`: Indicates that the subject occurs or exists at the same time as the object

### Spatial Relationships
* `#located_in`: Indicates that the subject is situated within the object
* `#contains`: Inverse of `#located_in`, indicates that the object is situated within the subject
* `#adjacent_to`: Indicates that the subject is close to or next to the object

### Contribution Relationships
* `#authored_by`: Indicates that the object created or originated the subject
* `#contributed_to`: Indicates that the object played a role in creating or influencing the subject
* `#derived_from`: Indicates that the subject is based on or adapted from the object

### Functional Relationships
* `#used_for`: Indicates the typical use or purpose of the subject
* `#used_by`: Indicates the user or system that utilizes the subject
* `#requires`: Indicates that the subject depends on or needs the object
* `#produces`: Indicates that the subject creates or generates the object as an output

## Examples
Front Matter will be organized into ONE of 7 different types, and generated following the pattern type.

### Person
---
title: Albert Einstein
description: German-born theoretical physicist, widely regarded as one of the most influential scientists of the 20th century.
type: person
tags: "[Physicist, Scientist, Theorist]"
relationships:
- "#developed [[Theory of Relativity]]"
- "#influenced [[Quantum Mechanics]]"
- "#worked_at [[Princeton University]]"
- "#born_in [[Ulm, Germany]]"
birthdate: 1879-03-14
deathdate: 1955-04-18
---

### Group (Company, Institution, Governmental Body, etc.)
---
title: Microsoft Corporation
description: American multinational technology corporation that develops, licenses, and supports a wide range of software products, services, and devices.
type: group
tags: [Technology, Software, Computing]
relationships:
- "#founded_by [[Bill Gates]], [[Paul Allen]]"
- "#headquartered_in [[Redmond, Washington]]"
- "#acquired [[Skype]], [[LinkedIn]], [[GitHub]]"
- "#competes_with [[Apple Inc.]], [[Google]]"
founded: 1975-04-04
---

### Event
---
title: World War II
description: Global war that lasted from 1939 to 1945, involving most of the world's nations and resulting in significant loss of life and destruction.
tags: [War, Conflict, 20th Century]
type: event
relationships:
- "#caused_by [[Rise of Fascism]], [[Invasion of Poland]]"
- "#involved [[Allied Powers]], [[Axis Powers]]"
- "#resulted_in [[United Nations]], [[Cold War]]"
- "#part_of [[World Wars]]"
start_date: 1939-09-01
end_date: 1945-09-02
---

### Concept
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

### Work (Books, Media)
---
title: 1984
description: Dystopian novel by George Orwell, published in 1949, depicting a totalitarian society and the consequences of mass surveillance and repressive control.
type: work
tags: [Literature, Dystopia, Science Fiction]
relationships:
- "#authored_by [[George Orwell]]"
- "#influenced_by [[Stalinism]], [[Totalitarianism]]"
- "#similar_to [[Brave New World]], [[Fahrenheit 451]]"
- "#adapted_into [[Nineteen Eighty-Four (1984 film)]]"
published_date: 1949-06-08
---

### Place
---
title: New York City
description: Most populous city in the United States, known for its diverse culture, iconic landmarks, and global influence in finance, media, art, fashion, and entertainment.
type: place
tags: [City, Metropolis, United States]
relationships:
- "#located_in [[New York State]], [[United States]]"
- "#consists_of [[Manhattan]], [[Brooklyn]], [[Queens]], [[The Bronx]], [[Staten Island]]"
- "#home_to [[Statue of Liberty]], [[Empire State Building]], [[Central Park]]"
- "#part_of [[Mid-Atlantic Region]], [[Northeast Megalopolis]]"
founded: 1624
population: 8,336,817 (2019)
---

### Conversation
---
title: Conversation with ChatGPT about Artificial Intelligence
description: A dialogue between a human and ChatGPT, an AI language model, discussing the implications and future of artificial intelligence.
type: conversation
tags: [Artificial Intelligence, ChatGPT, Language Models]
relationships:
- "#has_participant [[Human]]"
- "#has_participant [[ChatGPT]]"
- "#part_of [[OpenAI Conversations]]"
- "#discusses [[Artificial Intelligence]], [[Machine Learning]], [[Natural Language Processing]]"
- "#related_to [[Turing Test]], [[AI Ethics]]"
participants:
  - "Human"
  - "ChatGPT"
date: 2023-06-10
---

# RULES
- You can add additional properties as make sense, and shown in the examples based on the context, but ALL YAML must include the title, description, type tags, and relationships properties.
- ensure that all relationships are organized following the pattern of -"#predicate [[object]]"
- All dates must be formatted as YYYY-MM-DD

Here is the content to generate the YAML front matter for:

{note_content}
"""

def generate_front_matter(note_content):
    url = "http://localhost:1234/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": "bartowski/Phi-3-medium-128k-instruct-GGUF",
        "messages": [
            {"role": "system", "content": "You are an expert in YAML, specializing in Obsidian's front matter."},
            {"role": "user", "content": front_matter_prompt.format(note_content=note_content)}
        ],
        "temperature": 0.1
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    front_matter = response_data["choices"][0]["message"]["content"].strip()
    return front_matter

processed_notes_file = "processed_notes.txt"

def load_processed_notes():
    if os.path.exists(processed_notes_file):
        with open(processed_notes_file, "r", encoding="utf-8") as f:
            processed_notes = set(f.read().splitlines())
    else:
        processed_notes = set()
    return processed_notes

def save_processed_notes(processed_notes):
    with open(processed_notes_file, "w", encoding="utf-8") as f:
        f.write("\n".join(processed_notes))

def format_front_matter(front_matter):
    # Remove ```yaml delimiters if present
    front_matter = re.sub(r'```yaml\n?', '', front_matter)
    front_matter = re.sub(r'\n?```', '', front_matter)

    # Remove leading and trailing `---` if present
    front_matter = re.sub(r'^---\n', '', front_matter)
    front_matter = re.sub(r'\n---$', '', front_matter)

    # Remove problematic characters or formatting
    front_matter = re.sub(r'[^\x00-\x7F]+', '', front_matter)  # Remove non-ASCII characters
    front_matter = re.sub(r':\s+', ': ', front_matter)  # Remove extra spaces after colons
    front_matter = re.sub(r'\s+-\s+', '\n-', front_matter)  # Add newline before new list item

    # Ensure relationships are properly formatted as a list
    front_matter = re.sub(r'relationships:\s*\n(?!\s*-)', 'relationships:\n', front_matter)
    front_matter = re.sub(r'(\s+)-\s*"', r'\1- "', front_matter)

    # Ensure relationships are formatted as #predicate [[wikilink]]
    front_matter = re.sub(r'- "#(\w+)\s+\[*(.+?)\]*"', r'- "#\1 [[\2]]"', front_matter)

    # Remove colons from property values
    front_matter = re.sub(r':\s*([^"\n]+)(?=\n|$)', r': "\1"', front_matter)

    return front_matter

def process_notes():
    processed_notes = load_processed_notes()
    
    for root, dirs, files in os.walk(notes_directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                
                if file_path in processed_notes:
                    print(f"Skipping {file_path} - Already processed")
                    continue
                
                with open(file_path, "r", encoding="utf-8") as f:
                    note_content = f.read()
                
                print(f"Processing {file_path}")
                
                # Generate front matter using the prompt
                generated_front_matter = generate_front_matter(note_content)
                
                # Format the generated front matter
                formatted_front_matter = format_front_matter(generated_front_matter)

                # Modify the title to remove color and follow the desired format
                formatted_front_matter = re.sub(r'title: (.+)', lambda match: f"title: {re.sub(r'[🎨🖌️🎭]', '', match.group(1)).replace(':', ' - ')}", formatted_front_matter)

                # Remove existing front matter (if any)
                note_content = re.sub(r'^---\n.*?\n---\n', '', note_content, flags=re.DOTALL)

                # Add the formatted front matter to the note
                updated_note_content = f"---\n{formatted_front_matter}\n---\n\n{note_content.strip()}"

                # Write the updated note content back to the file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(updated_note_content)

                print(f"Updated front matter in {file_path}")
                processed_notes.add(file_path)
                save_processed_notes(processed_notes)


# Run the note processing function
process_notes()