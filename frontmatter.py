import os
import requests
import json

# Specify the directory containing the notes
notes_directory = "path/to/your/notes/directory"

# Prompt for generating front matter
front_matter_prompt = """
# MISSION
Act as an expert in YAML, specializing in Obsidian's front matter by inferring relationships from the note content. 
# INSTRUCTIONS
1. Review the provided content by the user.
2. Review the ONTOLOGY and EXAMPLES
3. Output ONLY the YAML front matter, nothing before or after.
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
Here's an example of how to define the "relationships" property in the YAML front matter, with the predicate tags enclosed in quotes:
```yaml
---
title: San Francisco
description: A major city in California known for its cultural landmarks and tech industry.
tags: [City, California, Landmark]
relationships:
  - "#located_in [[California]]"
  - "#part_of [[Bay Area]]"
  - "#has_part [[Golden Gate Bridge]]"
  - "#adjacent_to [[Pacific Ocean]]"
  - "#similar_to [[Seattle]]"
  - "#contains [[Alcatraz Island]]"
population: 873,965
founded: 1776
---
```
When processing a note, the subject is the note itself. The relationships are inferred from the content of the note, formatted as a list under the "relationships" property with each relationship formatted as `- "#predicate [[object]]"`.
```yaml
---
title: To Kill a Mockingbird
description: A novel by Harper Lee published in 1960, widely regarded as a classic of modern American literature.
tags: [Book, Literature, Classic]
relationships:
  - "#authored_by [[Harper Lee]]"
  - "#set_in [[Great Depression]]"
  - "#has_character [[Scout Finch]]"
  - "#has_character [[Atticus Finch]]"
  - "#part_of [[American Literature]]"
  - "#similar_to [[The Adventures of Huckleberry Finn]]"
published_in: 1960
genres: [Classic, Historical Fiction]
---
```
You can add additional properties as make sense, and shown in the examples based on the context, but ALL YAML must include the title, description, tags, and relationships properties.

Here is the content to generate the YAML front matter for:

{note_content}
"""

def generate_front_matter(note_content):
    url = "http://localhost:1234/v1/completions"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": front_matter_prompt.format(note_content=note_content),
        "max_tokens": 300,
        "temperature": 0.7,
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    front_matter = response_data["choices"][0]["text"].strip()
    return front_matter

def process_notes():
    for root, dirs, files in os.walk(notes_directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    note_content = f.read()
                
                # Check if the note has front matter
                if not note_content.startswith("---"):
                    # Generate front matter using the prompt
                    generated_front_matter = generate_front_matter(note_content)
                    
                    # Add the generated front matter to the note
                    updated_note_content = f"---\n{generated_front_matter}\n---\n\n{note_content}"
                    
                    # Write the updated note content back to the file
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(updated_note_content)
                    
                    print(f"Added front matter to {file_path}")

# Run the note processing function
process_notes()
