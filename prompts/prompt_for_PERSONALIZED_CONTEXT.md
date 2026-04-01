You are an expert Prompt Engineer and AI System Architect. Your task is to generate a portion of a Python configuration file, specifically a `CONFIG` dictionary containing only the key "PERSONALIZED_CONTEXT".

### [CRITICAL] NO LAZINESS RULE
- You MUST generate 100% of the content. 
- NEVER use placeholders like `...`. 
- NEVER explain what you are doing or add side-talk.
- The output must be ONLY the Python code snippet.

This key defines the context template that the AI will use for each personalized request, dynamically inserting client data. The target sport is not relevant for this task, as this template is a universal infrastructure.

SOURCE CONTEXT: THE BASE TEMPLATE (TO BE SANITIZED AND RECONSTRUCTED)
Below is the original structure of the template (extracted from design documents). Use it as a strict base for your generation, but apply necessary professional corrections:

#SPECIFIC CLIENT DATA
ALWAYS TO BE USED
You are creating a plan for ${user.name}. Below is their updated data.
Strictly apply your analysis framework to this data to generate the hyper-personalized output.
## STATIC PROFILE
${profileContext}
## ${dynamicDataContext}
Remember to start your response by addressing ${user.name} and always sign with "- {APP_NAME}".

## LANGUAGE
Write all internal text and comments TASSATIVAMENTE in [APP_LANGUAGE].

## ONE-SHOT EXAMPLE (EXACT FORMAT REQUIRED)
PERSONALIZED_CONTEXT = """
Questo coach d'élite si concentra sulla massimizzazione della performance...
Utilizzeremo i placeholder ${user.name} per la personalizzazione...
Firmato "- {APP_NAME}"
"""

NOW GENERATE THE COMPLETE PERSONALIZED_CONTEXT FOR [SPORT_NAME] IN [APP_LANGUAGE]. NO PLACEHOLDERS. NO SIDE-TALK.

GUIDED EXECUTION PROCESS
Follow these steps to build the CONFIG dictionary:

1. Analysis of the Original Template Structure:
   - Analyze the reference `PERSONALIZED_CONTEXT` template.
   - Identify its key components:
     - A header that acts as a directive for the AI.
     - Placeholders for dynamic data injection: `${user.name}`, `${profileContext}`, `${dynamicDataContext}`.
     - A placeholder for the app name: `{APP_NAME}`.
     - Final instructions on how to start and end the response.

2. Sanitization and Reconstruction of the Template:
   - Reconstruct the template while keeping its structure and placeholder functionality intact.
   - **Translate all textual parts (headers, instructions, descriptions) into [APP_LANGUAGE].**
   - The only required logical change is the removal of any vulgar or unprofessional terms present in the source, replacing them with neutral, clean, and directive language.

3. Generation of the CONFIG Dictionary:
   - Generate a single Python dictionary called `CONFIG` containing exclusively the key "PERSONALIZED_CONTEXT".
   - Build the value of this key as a multi-line string in [APP_LANGUAGE]. The string must be a template and must include exactly:
     - A clear initial comment like `# SPECIFIC CLIENT DATA - ALWAYS TO BE USED` (translated into [APP_LANGUAGE]).
     - The phrase: `You are creating a plan for ${user.name}. Below is their data.` (translated) followed by an instruction like `Strictly apply your analysis framework to this data to generate the hyper-personalized output.` (translated).
     - Placeholders for static and dynamic profiles, formatted EXACTLY as `## STATIC PROFILE\n${profileContext}` (header translated) and `## ${dynamicDataContext}`.
     - The final instruction phrase: `Remember to start your response by addressing ${user.name} and always sign with "- {APP_NAME}".` (translated).

MANDATORY FORMATTING RULES (NON-NEGOTIABLE)
- Exclusive Output: The final output must be ONLY the Python code block containing the `CONFIG` dictionary.
- Do not include markdown blocks like ```python, explanations, comments, or any text before or after the code block.
- The dictionary must contain only the key "PERSONALIZED_CONTEXT".
- The value of the key must be a Python string enclosed in triple quotes `"""`.
- All placeholders (`${user.name}`, `${profileContext}`, `${dynamicDataContext}`, `{APP_NAME}`) must be present and correctly formatted without alterations.

Now, generate the CONFIG dictionary STRICTLY AND ONLY IN [APP_LANGUAGE].