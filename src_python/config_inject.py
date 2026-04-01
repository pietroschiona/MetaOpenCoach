import os
import re
import json
import shutil
import importlib
import sys
import traceback

# =================== CORE SCRIPT (DO NOT MODIFY) =============================
# ==============================================================================


def replace_js_variable(js_code, var_name, new_value):
    """
    Sostituisce il valore di una variabile cost/let/var nel codice JavaScript.
    Supporta: const VAR = ...; let VAR = ...; var VAR = ...;
    Utilizza un sistema a due fasi:
    1. Se esiste un segnaposto __VAR_NAME_PLACEHOLDER__, lo sostituisce direttamente.
    2. Altrimenti usa un parser bilanciato per trovare il valore tra parentesi quadre o virgolette.
    """
    # 1. Se il segnaposto esplicito esiste, usalo (Priorità)
    placeholder = f"__{var_name}_PLACEHOLDER__"
    if placeholder in js_code:
        return js_code.replace(placeholder, str(new_value))

    # 2. Parser bilanciato per iniezione dinamica in assenza di placeholder
    pattern = re.compile(
        r"((?:const|let|var)\s+" + re.escape(var_name) + r"\s*=\s*)", re.DOTALL
    )
    match = pattern.search(js_code)
    if not match:
        # Fallback finale: regex semplice se non c'è corrispondenza complessa
        simple_pattern = rf"(\b(?:const|let|var)\s+{re.escape(var_name)}\s*=\s*)([^;]+)(;)"
        return re.sub(simple_pattern, rf"\1{new_value}\3", js_code, flags=re.MULTILINE)

    start_pos = match.end()
    # Pulisce spazi iniziali prima del valore
    while start_pos < len(js_code) and js_code[start_pos].isspace():
        start_pos += 1

    if start_pos >= len(js_code):
        return js_code

    first_char = js_code[start_pos]
    end_pos = -1

    if first_char == "[":
        # Trova la parentesi quadra di chiusura bilanciata
        balance = 0
        for i in range(start_pos, len(js_code)):
            if js_code[i] == "[":
                balance += 1
            elif js_code[i] == "]":
                balance -= 1
            if balance == 0:
                end_pos = i + 1
                break
    elif first_char in ("`", "'", '"'):
        # Trova il delimitatore di chiusura (non preceduto da escape)
        for i in range(start_pos + 1, len(js_code)):
            if js_code[i] == first_char and js_code[i - 1] != "\\":
                end_pos = i + 1
                break
    else:
        # Per altri valori (numeri, booleani, etc.) cerchiamo il punto e virgola
        semi_pos = js_code.find(";", start_pos)
        if semi_pos != -1:
            end_pos = semi_pos

    if end_pos != -1:
        print(
            f"  -> Sostituzione variabile JS '{var_name}' riuscita (parser bilanciato).")
        return js_code[:start_pos] + str(new_value) + js_code[end_pos:]
    else:
        # Fallback finale se il parser non trova la fine del blocco
        return js_code


def _unwrap_anomalous_data(data):
    """
    Helper to unwrap anomalous list-of-dicts with 'name'/'key' and 'value'.
    """
    unwrapped = []
    for item in data:
        if not isinstance(item, dict):
            continue
        raw_val = item.get("value")
        # item_name is the identifier
        item_name = item.get("name", item.get("key", f"q_{len(unwrapped)}"))

        # Sub-case A: item is the main "container" with value=list
        if isinstance(raw_val, list):
            for inner in raw_val:
                if not isinstance(inner, dict):
                    continue
                inner_key = inner.get("key", f"q_{len(unwrapped)}")
                inner_val = inner.get("value", {})
                q_text = (
                    inner_val.get("question", inner_key.replace("_", " ").title())
                    if isinstance(inner_val, dict)
                    else str(inner_val)
                    if inner_val
                    else inner_key.replace("_", " ").title()
                )
                unwrapped.append(
                    {
                        "key": inner_key,
                        "section": "Generale",
                        "title": inner_key.replace("_", " ").title(),
                        "question": q_text,
                        "type": "textarea",
                    }
                )

        # Sub-case B: item has value=dict {"question": "..."}
        elif isinstance(raw_val, dict):
            q_text = raw_val.get("question", item_name.replace("_", " ").title())
            unwrapped.append(
                {
                    "key": item_name,
                    "section": "Generale",
                    "title": item_name.replace("_", " ").title(),
                    "question": q_text,
                    "type": "textarea",
                }
            )

        # Sub-case C: item has direct key+value (mixed format)
        elif "key" in item:
            inner_val = item.get("value", {})
            q_text = (
                inner_val.get("question", item["key"].replace("_", " ").title())
                if isinstance(inner_val, dict)
                else str(inner_val)
                if inner_val
                else item["key"].replace("_", " ").title()
            )
            unwrapped.append(
                {
                    "key": item["key"],
                    "section": "Generale",
                    "title": item["key"].replace("_", " ").title(),
                    "question": q_text,
                    "type": "textarea",
                }
            )

        # Sub-case D: value is a primitive (number/string)
        elif isinstance(raw_val, (int, float, str)) and item_name:
            unwrapped.append(
                {
                    "key": item_name,
                    "section": "Generale",
                    "title": item_name.replace("_", " ").title(),
                    "question": str(raw_val),
                    "type": "number" if isinstance(raw_val, (int, float)) else "textarea",
                }
            )

        # Sub-case E: value is null or missing → use name as label
        elif raw_val is None and item_name:
            unwrapped.append(
                {
                    "key": item_name,
                    "section": "Generale",
                    "title": item_name.replace("_", " ").title(),
                    "question": item_name.replace("_", " ").title(),
                    "type": "textarea",
                }
            )
    return unwrapped


def _normalize_huge_dict_entry(huge_dict, primary_goal="weight"):
    """
    Helper to normalize a single dictionary where keys are the questions.
    """
    normalized = []
    for k, v in huge_dict.items():
        if isinstance(v, dict):
            question_text = v.get("question", str(k).replace("_", " ").title())
            raw_options = v.get("options", None)
        else:
            question_text = str(v)
            raw_options = None

        obj = {
            "key": str(k),
            "section": "Generale",
            "title": str(k).replace("_", " ").title(),
            "question": question_text,
            "type": "text",
        }

        if isinstance(raw_options, list) and len(raw_options) > 0:
            obj["type"] = "select"
            obj["options"] = [str(o) for o in raw_options]
        elif any(
            x in str(k).lower() for x in [primary_goal, "peso", "weight", "numerico"]
        ):
            obj["type"] = "number"

        normalized.append(obj)
    return normalized


def _apply_env_placeholders(items, is_variables=False):
    """
    Replaces placeholders ONLY in non-technical fields (title, question, label).
    Technical fields like 'key' or 'id' are preserved to avoid breaking UI links.
    Also formats the replacement value for a 'pretty' look.
    """
    # Get and format the goal key for 'pretty' labels
    raw_goal = os.environ.get("PRIMARY_GOAL_KEY", "weight")
    pretty_goal = raw_goal.replace("_", " ").title()

    env_placeholders = {
        r"\[PRIMARY_GOAL_KEY\]": pretty_goal,
        r"_\[PRIMARY_GOAL_KEY\]_": f" {pretty_goal} ",
        r"\[NOME_DELLO_SPORT\]": os.getenv("NOME_DELLO_SPORT", "OpenCoach"),
        r"\[APP_LANGUAGE\]": os.getenv("APP_LANGUAGE", "it"),
    }

    raw_placeholders = {
        r"\[PRIMARY_GOAL_KEY_RAW\]": raw_goal
    }

    for item in items:
        if not isinstance(item, dict):
            continue
        
        # Fields where we allow 'pretty' replacement
        target_fields = ["title", "question", "label", "section"]
        for field in target_fields:
            if field in item and isinstance(item[field], str):
                for pattern, val in env_placeholders.items():
                    item[field] = re.sub(pattern, str(val), item[field])
                for pattern, val in raw_placeholders.items():
                    item[field] = re.sub(pattern, str(val), item[field])
    return items
        
        # We EXPLICITLY do NOT replace [PRIMARY_GOAL_KEY] in 'key' or 'id' 
        # to maintain functional links with the template (clients.html / dashboard.html)
    return items


def normalize_questions(data, primary_goal="weight"):
    """
    Normalizes different data structures into a list of dictionaries.
    Decomposed to solve Pylint complexity.
    """
    if not data:
        return []

    if isinstance(data, str):
        try:
            # Handle possible python-style dicts in strings
            cleaned_str = data.replace("None", "null").replace("True", "true").replace("False", "false")
            data = json.loads(cleaned_str)
        except (json.JSONDecodeError, TypeError):
            return []

    if isinstance(data, dict):
        # Case 1 (Direct Huge Dict)
        if len(data) > 3 and "key" not in data:
            return _normalize_huge_dict_entry(data, primary_goal)
        data = [data]

    # Pre-check for Anomalous Wrapping (Case 0)
    if all(isinstance(x, dict) and ("name" in x or "value" in x) for x in data if isinstance(x, dict)):
        data = _unwrap_anomalous_data(data)

    final_list = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            # Case 2: Simple string list (fallback)
            if isinstance(item, str):
                final_list.append({
                    "key": f"q_{i}",
                    "section": "Generale",
                    "title": f"Question {i+1}",
                    "question": item,
                    "type": "textarea"
                })
            continue

        # Check for Nested Huge Dict inside the list
        if len(item) > 3 and "key" not in item:
            final_list.extend(_normalize_huge_dict_entry(item, primary_goal))
            continue

        # Normal Structured Item
        if "key" in item:
            item.setdefault("section", "Generale")
            item.setdefault("title", item["key"].replace("_", " ").title())
            item.setdefault("question", item["title"])
            item.setdefault("type", "textarea")
            final_list.append(item)
        else:
            # Fallback for dictionary entry without key
            k = list(item.keys())[0] if item else f"q_{i}"
            v = item[k] if item else "No text provided"
            final_list.append({
                "key": str(k),
                "section": "Generale",
                "title": str(k).replace("_", " ").title(),
                "question": str(v),
                "type": "textarea"
            })

    # Placeholder replacement (Surgical Fix v7)
    return _apply_env_placeholders(final_list)


def safe_js_dump(data):
    """
    Serializes data to JSON and cleans quotes from keys only if they are valid identifiers.
    Example: "key": -> key: (valid) | "1_key": -> "1_key" (remains quoted for JS)
    """
    if data is None:
        return "null"
    if isinstance(data, str) and (data.startswith("[") or data.startswith("{")):
        # If it's already a JSON-like string, try to load it to normalize
        try:
            data = json.loads(data)
        except Exception:
            pass

    js_str = json.dumps(data, indent=4, ensure_ascii=False)

    # Regex to remove quotes only from keys that are valid JS identifiers
    # A valid JS identifier CANNOT start with a number.
    # Must start with [a-zA-Z_$] followed by [a-zA-Z0-9_$]*
    js_str = re.sub(r'"([a-zA-Z_$][a-zA-Z0-9_$]*)"\s*:', r"\1:", js_str)

    # Residual cleanup for booleans or null if injected as strings in mixed contexts
    # (Shouldn't be needed with json.dumps but better for security)
    return js_str


def safe_js_inject(text):
    """
    Escapes characters that could break a JavaScript backtick string
    or trigger unwanted interpolation (like ${var}).
    """
    if not text:
        return ""
    # Escape dollar signs to prevent ${} interpolation in JS backticks
    return text.replace("$", "\\$")


def replace_between_markers(content, marker_name, new_value):
    """
    Replaces text between two marker comments using find and slice.
    Robust against regex special characters in markers.
    """
    start_tag = f"// --- {marker_name}_START ---"
    end_tag = f"// --- {marker_name}_END ---"
    
    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag)
    
    if start_idx == -1 or end_idx == -1:
        print(f"  -> WARNING: Markers for '{marker_name}' NOT found.")
        return content
        
    actual_start = start_idx + len(start_tag)
    print(f"  -> Block '{marker_name}' updated successfully.")
    return content[:actual_start] + "\n" + new_value + "\n" + content[end_idx:]


def sanitize_app_name_for_path(app_name, base_output_dir):
    """
    Sanitizes APP_NAME for SAFE use as a folder name in the filesystem.
    Returns the sanitized name string.
    """
    # 1. Remove all dangerous characters: only keep alphanumeric, spaces, hyphens and underscores
    safe_name = re.sub(r"[^\w\s\-]", "", app_name).strip()
    # 2. Replace spaces with underscores for filesystem compatibility
    safe_name = safe_name.replace(" ", "_")
    # 3. Collapse multiple underscore sequences
    safe_name = re.sub(r"_+", "_", safe_name).strip("_")
    # 4. Fallback if name is completely empty after sanitization
    if not safe_name:
        safe_name = "generated_app"
    return safe_name

def resolve_unique_output_dir(base_output_dir, sanitized_name):
    """
    Finds a unique folder path by appending numeric suffixes if necessary.
    Also ensures path confinement (security).
    """
    candidate_folder = sanitized_name
    candidate_path = os.path.realpath(os.path.join(base_output_dir, candidate_folder))
    base_real = os.path.realpath(base_output_dir)

    counter = 1
    while os.path.exists(candidate_path):
        candidate_folder = f"{sanitized_name}_{counter}"
        candidate_path = os.path.realpath(os.path.join(base_output_dir, candidate_folder))
        counter += 1

    # Security check: verify that the resulting path is a CHILD of base_output_dir
    if not candidate_path.startswith(base_real + os.sep) and candidate_path != base_real:
        raise ValueError(
            f"[SECURITY] Path Traversal detected! Sanitized name '{sanitized_name}' "
            f"produces an unsafe path: '{candidate_path}'"
        )
    
    return candidate_path


def process_files(config):
    """
    Main function that creates the app folder, copies base files,
    applies modifications and writes new customized files using the provided config.
    """
    # --- 1. EXTRACT AND PREPARE VARIABLES FROM CONFIG ---
    APP_NAME = config.APP_NAME
    SPORT_NAME = getattr(config, "SPORT_NAME", APP_NAME)
    
    # SYSTEM_PROMPT
    SYSTEM_PROMPT = config.SYSTEM_PROMPT.format(APP_NAME=APP_NAME)
    primary_goal_key = os.environ.get("PRIMARY_GOAL_KEY", "weight")
    
    # PROFILE_QUESTIONS -> PROF_QUESTIONS (JSON)
    raw_profile = getattr(config, "CLIENTS_PROFILE_QUESTIONS", config.PROFILE_QUESTIONS)
    # Cleanup possible comments in strings if it comes from a dirty source
    if isinstance(raw_profile, str):
        raw_profile = re.sub(r"#.*$", "", raw_profile, flags=re.MULTILINE)
    
    PROF_QUESTIONS_LIST = normalize_questions(raw_profile)
    PROF_QUESTIONS = json.dumps(
        PROF_QUESTIONS_LIST,
        indent=4,
        ensure_ascii=False,
    )

    # VARIABLES_TO_EXTRACT -> VARS_EXTRACT (JSON)
    raw_vars = getattr(config, "VARIABLES_TO_EXTRACT", "[]")
    if not isinstance(raw_vars, str):
        VARS_EXTRACT_LIST = raw_vars
    else:
        # Clean possible markdown
        v_clean = re.sub(r"^```(?:json)?\n", "", raw_vars, flags=re.MULTILINE)
        v_clean = re.sub(r"```$", "", v_clean, flags=re.MULTILINE).strip()
        if not v_clean.startswith("["):
            match = re.search(r"\[.*\]", v_clean, re.DOTALL)
            v_clean = match.group(0) if match else "[]"
        try:
            VARS_EXTRACT_LIST = json.loads(v_clean)
        except Exception:
            VARS_EXTRACT_LIST = []

    # Normalize VARIABLES_TO_EXTRACT (id -> key) + Placeholders
    if isinstance(VARS_EXTRACT_LIST, list):
        for v in VARS_EXTRACT_LIST:
            if isinstance(v, dict):
                if "id" in v and "key" not in v:
                    v["key"] = v["id"]
        VARS_EXTRACT_LIST = _apply_env_placeholders(VARS_EXTRACT_LIST, is_variables=True)
    
    VARS_EXTRACT = json.dumps(VARS_EXTRACT_LIST, indent=4, ensure_ascii=False)

    # PERSONALIZED_CONTEXT -> PERS_CONTEXT (String)
    PERS_CONTEXT = str(getattr(config, "PERSONALIZED_CONTEXT", ""))
    
    # Robust Cleaning of LLM hallucinations
    # Pattern 1: CONFIG = { "PERSONALIZED_CONTEXT": """ ... """ }
    match_wrapper = re.search(r'PERSONALIZED_CONTEXT":\s*["\']{3}(.*?)["\']{3}', PERS_CONTEXT, re.DOTALL)
    if match_wrapper:
        PERS_CONTEXT = match_wrapper.group(1).strip()
    else:
        # Pattern 2: CONFIG = { ... } strip wrapper lines
        PERS_CONTEXT = re.sub(r'^CONFIG\s*=\s*\{\s*"PERSONALIZED_CONTEXT":\s*["\']{3}', '', PERS_CONTEXT.strip(), flags=re.MULTILINE)
        PERS_CONTEXT = re.sub(r'["\']{3}\s*\}\s*$', '', PERS_CONTEXT.strip(), flags=re.MULTILINE)
    
    PERS_CONTEXT = PERS_CONTEXT.strip().strip("'\"").strip()

    # PROMPT_BUTTONS_LOGIC
    PROMPT_BUTTONS_LOGIC = getattr(config, "PROMPT_BUTTONS_LOGIC", "None")
    if isinstance(PROMPT_BUTTONS_LOGIC, str):
        PROMPT_BUTTONS_LOGIC = PROMPT_BUTTONS_LOGIC.replace("None", "null").replace("True", "true").replace("False", "false")

    # --- PERCORSI DI BASE (CORRETTI) ---
    # CORRECTION: Removed extra quotes that were causing [WinError 123]
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_dir_full_app = os.path.join(
        BASE_DIR, "template_core", "metaopencoach_base")
    base_output_dir = os.path.join(BASE_DIR, "generated_output")

    # --- PERCORSO DI DESTINAZIONE DINAMICO ---
    # FIX VUL-001 & V11: Resolve unique folder name to prevent overwriting
    sanitized_folder_name = sanitize_app_name_for_path(APP_NAME, base_output_dir)
    output_dir = resolve_unique_output_dir(base_output_dir, sanitized_folder_name)
    
    # We update APP_NAME to reflect the actual folder name if it's different
    FINAL_APP_NAME = os.path.basename(output_dir)
    print(f"  -> Final Folder Name: '{FINAL_APP_NAME}'")
    print(f"  Files are located in folder: '{output_dir}'")

    old_app_name = "MetaOpenCoach"

    print(f"\n--- Starting app generation: '{APP_NAME}' ---")
    print(f"DEBUG: BASE_DIR = {BASE_DIR}")
    print(f"DEBUG: Source Dir = {source_dir_full_app}")
    print(f"DEBUG: Output Dir = {output_dir}")

    # --- 1. Create destination folder and copy base files ---
    print(f"\n[1/5] Preparing destination folder for '{APP_NAME}'...")
    try:
        # BUG FIX: rmtree disabilitato per preservare file personalizzati in generated_output/
        # if os.path.exists(output_dir):
        #     def _force_remove(func, path, exc):
        #         """Rimuove i file read-only (fix WinError 5 su node_modules)."""
        #         import stat
        #         os.chmod(path, stat.S_IWRITE)
        #         func(path)
        #     shutil.rmtree(output_dir, onexc=_force_remove)
        #     print(
        #         f"  -> Cartella di destinazione esistente rimossa: '{output_dir}'")

        shutil.copytree(
            source_dir_full_app,
            output_dir,
            ignore=shutil.ignore_patterns("node_modules", ".git"),
            dirs_exist_ok=True,
        )
        print(
            f"  -> Copied '{os.path.basename(source_dir_full_app)}' to '{output_dir}' (node_modules excluded)."
        )
    except Exception as e:
        print(f" -> CRITICAL ERROR during file copy: {e}")
        return

    # --- 2. Create package.json (Deterministic Algorithmic Generation) ---
    print(f"\n[2/5] Creating agnostic 'package.json' file...")
    try:
        # Pulisce l'APP_NAME generato dall'AI per renderlo compatibile con NPM e Windows
        safe_name = re.sub(r"[^a-zA-Z0-9 ]", "", APP_NAME)
        kebab_name = safe_name.lower().replace(" ", "-")
        pascal_name = "".join(word.capitalize() for word in safe_name.split())

        # Carica il package.json del template per sincronizzare le dipendenze originali
        template_pkg_path = os.path.join(source_dir_full_app, "package.json")
        template_deps = {}
        template_dev_deps = {}
        if os.path.exists(template_pkg_path):
            with open(template_pkg_path, "r", encoding="utf-8") as tf:
                t_data = json.load(tf)
                template_deps = t_data.get("dependencies", {})
                template_dev_deps = t_data.get("devDependencies", {})

        # Dizionario Python puro, impossibile da corrompere, 100% Agnostico
        pkg_data = {
            "name": kebab_name,
            "version": "1.0.0",
            "description": f"AI Coaching Software per {APP_NAME}",
            "main": "server.js",
            "bin": "server.js",
            "scripts": {
                "start": "node server.js",
                "test": "npx playwright test",
                "build": f"pkg . --targets node18-win-x64 --no-bytecode --public --output dist/{pascal_name}.exe",
            },
            "pkg": {"assets": ["public/**/*", ".env"]},
            "dependencies": {
                **template_deps,
                "express": "^4.18.2",
                "ws": "^8.16.0",
                "helmet": "^7.1.0",
                "cors": "^2.8.5",
                "redact-pii": "^3.4.0",
                "dotenv": "^16.4.5",
            },
            "devDependencies": {
                **template_dev_deps,
                "pkg": "^5.8.1",
                "@playwright/test": "^1.40.0",
            },
        }

        output_path_package_json = os.path.join(output_dir, "package.json")
        with open(output_path_package_json, "w", encoding="utf-8") as f:
            json.dump(pkg_data, f, indent=4)

        print(
            f" -> File 'package.json' generato algoritmicamente con successo in '{output_path_package_json}'."
        )
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f" -> Unexpected error creating package.json: {e}")
        sys.exit(1)

    # --- 2.1 Crea file .env ---
    print(f"\n[2.1] Creating '.env' file...")
    try:
        env_content = (
            f"AI_BASE_URL={os.getenv('AI_BASE_URL', 'https://api.openai.com/v1')}\n"
            f"AI_API_KEY={os.getenv('AI_API_KEY', '')}\n"
            f"AI_MODEL={os.getenv('AI_MODEL', 'gpt-4o-mini')}\n"
            f"AI_PROVIDER={os.getenv('AI_PROVIDER', 'openai')}\n"
        )
        output_path_env = os.path.join(output_dir, ".env")
        with open(output_path_env, "w", encoding="utf-8") as f:
            f.write(env_content)
        print(f" -> '.env' file created successfully at '{output_path_env}'.")
    except Exception as e:
        print(f" -> Unexpected error creating .env: {e}")

    # --- Definizione dei percorsi dei file da modificare ---
    output_path_server_js = os.path.join(output_dir, "server.js")
    output_path_clients_html = os.path.join(
        output_dir, "public", "clients.html")
    output_path_index_html = os.path.join(output_dir, "public", "index.html")

    # --- 3. Processa server.js ---
    print(
        f"\n[3/5] Processando e sostituendo '{os.path.basename(output_path_server_js)}'..."
    )
    try:
        with open(output_path_server_js, "r", encoding="utf-8") as f:
            content = f.read()

        # Sostituzione del segnaposto per il SYSTEM_PROMPT
        escaped_system_prompt = SYSTEM_PROMPT.replace("`", r"\`")
        content = content.replace(
            "__SYSTEM_PROMPT_PLACEHOLDER__", escaped_system_prompt
        )
        print(
            "  -> Segnaposto '__SYSTEM_PROMPT_PLACEHOLDER__' sostituito con successo."
        )

        # Iniezione di variabili complesse tramite replace_js_variable
        content = replace_js_variable(content, "PROFILE_QUESTIONS", PROF_QUESTIONS)
        content = replace_js_variable(content, "VARIABLES_TO_EXTRACT", VARS_EXTRACT)

        # Branding e placeholder rimanenti
        content = content.replace("calicoach", FINAL_APP_NAME.lower())
        content = content.replace("[APP_NAME]", FINAL_APP_NAME)
        content = content.replace("[NOME_DELLO_SPORT]", SPORT_NAME)
        content = content.replace("__PERSONALIZED_CONTEXT_PLACEHOLDER__", safe_js_inject(PERS_CONTEXT))
        content = content.replace("__VARIABLES_TO_EXTRACT_PLACEHOLDER__", safe_js_inject(VARS_EXTRACT))
        content = content.replace("__PROFILE_QUESTIONS_PLACEHOLDER__", PROF_QUESTIONS)

        with open(output_path_server_js, "w", encoding="utf-8") as f:
            f.write(content)
        print(f" -> File '{os.path.basename(output_path_server_js)}' aggiornato correttamente.")

    except Exception as e:
        print(f" -> Errore durante il processing di server.js: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # --- 4. Processa index.html ---
    print(
        f"\n[4/5] Processando e sostituendo '{os.path.basename(output_path_index_html)}'..."
    )
    try:
        with open(output_path_index_html, "r", encoding="utf-8") as f:
            content = f.read()

        count_before = content.count(old_app_name)
        content = content.replace(old_app_name, FINAL_APP_NAME)
        print(
            f"  -> Nome app '{old_app_name}' sostituito con '{FINAL_APP_NAME}' ({count_before} occorrenze)."
        )

        # Replace environment placeholders in HTML
        sport_name = getattr(config, "SPORT_NAME", APP_NAME)
        content = content.replace("[NOME_DELLO_SPORT]", sport_name)
        content = content.replace("[SPORT_NAME]", sport_name)
        content = content.replace("[APP_NAME]", FINAL_APP_NAME)
        # Surgical fix: avoid global [PRIMARY_GOAL_KEY] replacement here

        # Converte le chiamate promptBtnXXX nell'accesso DOM corretto per index.html
        logic_str = str(PROMPT_BUTTONS_LOGIC)
        logic_str = re.sub(
            r"promptBtn([a-zA-Z]+)\.onclick",
            lambda m: (
                f"document.getElementById('prompt-btn-{re.sub(r'(?<!^)(?=[A-Z])', '-', m.group(1)).lower()}'"
                f").onclick"
            ),
            logic_str,
        )

        # Iniezione dei bottoni tramite marcatori ROBBUSTI (Sostituisce il vecchio metodo Regex fragile)
        content = replace_between_markers(content, "QUICK_COMMANDS", logic_str)

        with open(output_path_index_html, "w", encoding="utf-8") as f:
            f.write(content)
        print(
            f" -> File '{os.path.basename(output_path_index_html)}' sovrascritto con successo."
        )

    except FileNotFoundError:
        print(f" -> ERROR: File not found at path '{output_path_index_html}'.")
    except Exception as e:
        print(f" -> Unexpected error processing index.html: {e}")

    # --- 5. Process clients.html ---
    print(
        f"\n[5/5] Processando e sostituendo '{os.path.basename(output_path_clients_html)}'..."
    )
    try:
        with open(output_path_clients_html, "r", encoding="utf-8") as f:
            content = f.read()

        # Usa PROF_QUESTIONS_LIST normalizzate (già calcolate all'inizio)
        js_array_as_string = json.dumps(PROF_QUESTIONS_LIST, indent=4, ensure_ascii=False)

        content = replace_between_markers(
            content,
            "PROFILE_QUESTIONS",
            f"        const profileQuestions = {js_array_as_string};",
        )
        content = content.replace(old_app_name, FINAL_APP_NAME)
        print(
            f"  -> Nome app '{old_app_name}' sostituito con '{FINAL_APP_NAME}' (tutte le occorrenze)."
        )
 
        # Replace environment placeholders in HTML (Only outside injected blocks)
        sport_name = getattr(config, "SPORT_NAME", APP_NAME)
        # Note: We avoid global replacement of [PRIMARY_GOAL_KEY] here 
        # because it's already handled surgically in PROF_QUESTIONS_LIST.
        # However, we still replace it in regular HTML text if needed.
        # But to be safe and avoid breaking 'key: "[PRIMARY_GOAL_KEY]"', 
        # we only replace it in specific patterns or markers.
        # For now, let's keep NOME_DELLO_SPORT and APP_NAME as they are usually titles.
        content = content.replace("[NOME_DELLO_SPORT]", sport_name)
        content = content.replace("[SPORT_NAME]", sport_name)
        content = content.replace("[APP_NAME]", FINAL_APP_NAME)

        # Inject PRIMARY_GOAL_KEY via markers
        content = replace_between_markers(
            content,
            "PRIMARY_GOAL_KEY",
            f"const PRIMARY_GOAL_KEY = '{primary_goal_key}';",
        )

        # --- AGGIORNAMENTO PROGRESS TRACKING ---
        progress_mode = os.environ.get("PROGRESS_MODE", "auto")
        custom_html = os.environ.get("CUSTOM_PROGRESS_HTML", "")

        if progress_mode == "manual" and custom_html:
            print(
                "  -> PROGRESS_MODE=manual: Iniezione HTML dinamico e sostituzione del motore Chart.js in corso..."
            )

            # 1. Sostituzione HTML progress-inputs
            content = re.sub(
                r'<div class="progress-inputs">.*?</div>(?=\s*<button type="button" id="update-progress-btn")',
                f'<div class="progress-inputs">\n{custom_html}\n</div>\n',
                content,
                flags=re.DOTALL,
            )

            # 2. Sostituzione JS updateProgressBtn
            dynamic_btn_js = """updateProgressBtn.addEventListener('click', async () => {
            const id = hiddenIdEl.value;
            if (!id) return;
            const inputs = document.querySelectorAll('.progress-inputs input');
            let weight = null, bodyFat = null, adherence = {};
            inputs.forEach(input => {
                const val = input.value;
                if (!val && val !== '0') return;
                if (input.id === 'current-weight' || input.id.includes('weight')) weight = val;
                else if (input.id === 'body-fat' || input.id.includes('fat')) bodyFat = val;
                else adherence[input.id] = isNaN(val) ? val : parseFloat(val);
            });
            const body = { weight: weight || null, bodyFat: bodyFat || null, adherence };
            try {
                const response = await fetch(`/api/users/${id}/progress`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
                const result = await response.json();
                if (!response.ok) throw new Error(result.error || 'Errore salvataggio progresso.');
                showFeedback(result.message, 'success', progressFeedbackEl);
                await fetchAndRenderUsers();
                await selectUser(id);
                inputs.forEach(input => input.value = '');
            } catch(error) { showFeedback(error.message, 'error', progressFeedbackEl); }
        });"""
            content = re.sub(
                r"updateProgressBtn\.addEventListener\('click', async \(\) => \{.+?(?=// --- BLOCCO SALVATAGGIO FORM CORRETTO)",
                dynamic_btn_js + "\n\n        ",
                content,
                flags=re.DOTALL,
            )

            # 3. Sostituzione JS updateClientDashboard
            dynamic_dash_js = """function updateClientDashboard(user) {
            currentUser = user; 
            clientAnalyticsSection.style.display = 'block';
            Object.values(clientCharts).forEach(chart => { if (chart) chart.destroy(); });

            const weeklyData = [];
            const currentYear = new Date().getFullYear();
            const adherenceMap = new Map((user.progressData?.adherenceHistory || []).map(d => [d.week, d]));
            const weightMap = new Map();
            (user.progressData?.weightHistory || []).forEach(w => {
                const dateObj = new Date(w.date);
                if (isNaN(dateObj.getTime())) return;
                const weekId = `${currentYear}-W${String(dateObj.getWeek()).padStart(2, '0')}`;
                if (!weightMap.has(weekId)) weightMap.set(weekId, w);
            });
            for(let w of adherenceMap.keys()) {
                const weekNum = parseInt(w.split('W')[1] || "0");
                weeklyData.push({ weekLabel: `W${weekNum}`, adherence: adherenceMap.get(w), weight: weightMap.get(w) || {} });
            }
            weeklyData.sort((a,b) => parseInt(a.weekLabel.substring(1)) - parseInt(b.weekLabel.substring(1)));

            const allKeys = new Set();
            weeklyData.forEach(d => { if (d.adherence) { Object.keys(d.adherence).forEach(k => { if(k !== 'week') allKeys.add(k); }); } });
            
            const chartColors = [ '#9F7AEA', '#667EEA', '#f59e0b', '#dc3545', '#28a745', '#17a2b8' ];
            const datasets = [];
            let colorIndex = 0;
            allKeys.forEach(key => {
                datasets.push({ label: key, data: weeklyData.map(d => (d.adherence && d.adherence[key]) ? d.adherence[key] : 0), borderColor: chartColors[colorIndex % chartColors.length], tension: 0.4 });
                colorIndex++;
            });
            
            const perfCtx = document.getElementById('clientCompositeChart').getContext('2d');
            clientCharts.performance = new Chart(perfCtx, { type: 'line', data: { labels: weeklyData.map(d => d.weekLabel), datasets: datasets }, options: { responsive: true, maintainAspectRatio: false } });
            
            const radarCtx = document.getElementById('clientRadarChart').getContext('2d');
            clientCharts.radar = new Chart(radarCtx, { type: 'radar', data: { labels: Array.from(allKeys), datasets: [{ label: 'Media Storica', data: Array.from(allKeys).map(key => { const validData = weeklyData.filter(d => d.adherence && d.adherence[key]); return validData.length === 0 ? 0 : validData.reduce((acc, d) => acc + parseFloat(d.adherence[key]), 0) / validData.length; }), borderColor: '#9F7AEA', backgroundColor: 'rgba(159, 122, 234, 0.1)' }] }, options: { responsive: true, maintainAspectRatio: false } });

            // --- CALCOLO PROGRESSO OBIETTIVO NUMERICO ---
            const goalKey = "${primary_goal_key}"; // Es: weight
            const targetKey = "target_" + goalKey; // Mapping automatico
            const targetVal = parseFloat(user.profile[targetKey]) || parseFloat(user.profile[goalKey]);
            
            let progressPerc = 0;
            if (targetVal && weeklyData.length > 0) {
                const initialVal = parseFloat(user.profile[goalKey]) || (weeklyData[0].weight ? weeklyData[0].weight.weight : null);
                const currentVal = weeklyData[weeklyData.length - 1].weight ? weeklyData[weeklyData.length - 1].weight.weight : null;
                
                if (initialVal !== null && currentVal !== null) {
                    const tolerance = initialVal * 0.02; // 2% soglia mantenimento
                    if (Math.abs(targetVal - initialVal) < tolerance) {
                        // MAINTAIN: progress = how close to target
                        const deviation = Math.abs(currentVal - targetVal);
                        progressPerc = Math.max(0, 100 - (deviation / (tolerance || 1)) * 100);
                    } else if (targetVal > initialVal) {
                        // INCREASE: progresso cresce avvicinandosi al target dall'alto
                        progressPerc = ((currentVal - initialVal) / (targetVal - initialVal)) * 100;
                    } else {
                        // DECREASE: progresso cresce avvicinandosi al target dal basso
                        progressPerc = ((initialVal - currentVal) / (initialVal - targetVal)) * 100;
                    }
                }
            }
            progressPerc = Math.max(0, Math.min(100, progressPerc));

            document.getElementById('metric-adherence').textContent = 'Dinamico';
            document.getElementById('metric-sleep').textContent = '...';
            document.getElementById('metric-stress').textContent = '...';
            document.getElementById('metric-weight-loss').textContent = weightMap.size > 0 ? Array.from(weightMap.values()).pop().weight + ' kg' : 'N/D';
            document.getElementById('metric-goal-progress').textContent =
                `${progressPerc.toFixed(0)} %`;
        }"""

            # Iniezione variabile primaria nel JS iniettato
            dynamic_dash_js = dynamic_dash_js.replace(
                "${primary_goal_key}", primary_goal_key
            )

            content = re.sub(
                r"function updateClientDashboard\(user\) \{.+?(?=function renderClientList\(\) \{)",
                dynamic_dash_js + "\n\n        ",
                content,
                flags=re.DOTALL,
            )
            print(
                "  -> Logica JavaScript dinamica assemblata ed iniettata con successo."
            )

        with open(output_path_clients_html, "w", encoding="utf-8") as f:
            f.write(content)
        print(
            f" -> File '{os.path.basename(output_path_clients_html)}' sovrascritto con successo."
        )

    except FileNotFoundError:
        print(
            f" -> ERROR: File not found at path '{output_path_clients_html}'.")
    except Exception as e:
        print(f" -> Unexpected error processing clients.html: {e}")

    print(f"\n--- Process for '{APP_NAME}' completed! ---")
    print(f"Files are located in folder: '{os.path.abspath(output_dir)}'")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Inject configuration into the web app template.")
    parser.add_argument(
        "--file", help="Specific configuration file to process (e.g. config_mma_1.py)")
    args = parser.parse_args()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir_path = os.path.join(BASE_DIR, "generated_output")

    # Aggiungiamo direttamente la cartella generated_output al path di Python
    if config_dir_path not in sys.path:
        sys.path.insert(0, config_dir_path)

    if args.file:
        # SINGLE FILE MODE
        filename = args.file
        if not filename.endswith(".py"):
            filename += ".py"

        # Se il percorso non è assoluto, assume che sia in generated_output
        if not os.path.isabs(filename):
            full_path = os.path.join(config_dir_path, filename)
        else:
            full_path = filename
            filename = os.path.basename(filename)

        if not os.path.exists(full_path):
            print(f"ERROR: Specified config file not found: {full_path}")
            sys.exit(1)

        config_files = [filename]
        print(f"Targeting specific config file: {filename}")
    else:
        # BATCH MODE (Legacy/Automatic)
        try:
            config_files = [
                f
                for f in os.listdir(config_dir_path)
                if f.endswith(".py") and not f.startswith("__")
            ]
        except FileNotFoundError:
            print(
                f"ERROR: Config folder not found at path '{config_dir_path}'.")
            config_files = []

    if not config_files:
        print(f"No .py config files found. Processing aborted.")
    else:
        total_files = len(config_files)
        if not args.file:
            print(
                f"Found {total_files} config files. Starting batch processing...")

        for i, filename in enumerate(config_files):
            module_name = filename[:-3]
            print(f"\n{'=' * 70}")
            print(
                f"ATOMIC PROCESS [{i + 1}/{total_files}]: Loading module '{module_name}'"
            )
            print(f"{'=' * 70}")
            try:
                # Importa il modulo dinamicamente
                config_module = importlib.import_module(module_name)
                importlib.reload(config_module)
                process_files(config_module)
            except ImportError as e:
                print(
                    f"CRITICAL ERROR: Unable to import module '{module_name}'. Details: {e}"
                )
                sys.exit(1)
            except AttributeError as e:
                print(
                    f"CRITICAL ERROR: Missing variable in file {filename}. Details: {e}")
                sys.exit(1)
            except Exception as e:
                print(f"CRITICAL ERROR unexpected processing {filename}: {e}")
                traceback.print_exc()
                sys.exit(1)

        print(f"\n{'=' * 70}")
        print("INJECTION COMPLETED.")
        print(f"{'=' * 70}")
