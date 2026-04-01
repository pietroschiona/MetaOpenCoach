# -*- coding: utf-8 -*-

"""
SCRIPT FOR AUTOMATIC GENERATION OF CONFIGURATION FILES FOR AI COACH
FINAL VERSION: Generates complete .py files compatible with ga7.py script,
handling assembly of all necessary variables, including package.json.
"""

import fitz  # PyMuPDF
import os
import re
import sys
import time
import json
import requests
import traceback

# --- FIX ENCODING ON WINDOWS --- (Necessary for emojis in console)
try:
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from google.generativeai.types import HarmCategory, HarmBlockThreshold
# --- MAIN CONFIGURATION ---

# 1. GOOGLE GEMINI API KEY (From environment)
GOOGLE_API_KEY = os.getenv("AI_API_KEY", "")

# 2. LIST OF SPORTS TO GENERATE
sport_from_env = os.getenv("SPORT_NAME")
SPORTS_TO_GENERATE = [sport_from_env] if sport_from_env else ["Calisthenics"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTRUCTION_FILE_NAME = os.getenv(
    "INSTRUCTION_FILE", "Dati_necessari_per_personalizzare.pdf"
)
BASE_DOC_PATH = os.path.join(BASE_DIR, "data_input", INSTRUCTION_FILE_NAME)
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_output")

PROMPT_FILES_IN_ORDER = [
    "prompt_for_SYSTEM_PROMPT.md",
    "prompt_for_PROFILE_QUESTIONS.md",
    "prompt_for_CLIENTS_PROFILE_QUESTIONS.md",
    "prompt_for_PERSONALIZED_CONTEXT.md",
    "prompt_for_BUTTON_LOGIC.md",
    "prompt_for_VARIABLES.md",
]

# Mappa: frammento del nome file → chiave env var per override manuale
MODULE_ENV_MAP = {
    "SYSTEM_PROMPT": "MANUAL_SYSTEM_PROMPT",
    "PROFILE_QUESTIONS": "MANUAL_PROFILE_QUESTIONS",
    "CLIENTS_PROFILE_QUESTIONS": "MANUAL_CLIENTS_PROFILE_QUESTIONS",
    "PERSONALIZED_CONTEXT": "MANUAL_PERSONALIZED_CONTEXT",
    "BUTTON_LOGIC": "MANUAL_BUTTON_LOGIC",
    "VARIABLES": "MANUAL_VARIABLES",
}

# Safe fallbacks (already compile()-valid) for each module — used only in extremis
_SAFE_FALLBACKS = {
    "CLIENTS_PROFILE_QUESTIONS": """CLIENTS_PROFILE_QUESTIONS = [
    {"key": "obiettivi", "section": "Obiettivi", "title": "Obiettivi Principali", "question": "Quali sono i tuoi obiettivi principali?", "type": "textarea"},
    {"key": "esperienze", "section": "Storia", "title": "Esperienza Precedente", "question": "Hai avuto esperienze precedenti in questo sport?", "type": "textarea"},
    {"key": "infortuni", "section": "Salute", "title": "Infortuni o Limitazioni", "question": "Hai infortuni attuali o passati da segnalare?", "type": "textarea"}
]""",
    "PROFILE_QUESTIONS": '''PROFILE_QUESTIONS = """
[
    {"key": "nome_atleta", "section": "Anagrafica", "title": "Nome Completo", "question": "Qual è il nome completo dell'atleta?", "type": "text"},
    {"key": "livello_partenza", "section": "Valutazione", "title": "Livello di Partenza", "question": "Qual è il livello attuale dell'atleta (Principiante/Intermedio/Avanzato)?", "type": "select", "options": ["Principiante", "Intermedio", "Avanzato"]}
]
"""''',
    "SYSTEM_PROMPT": '''APP_NAME = "[NOME_DELLO_SPORT] AI"
SYSTEM_PROMPT = """
## ROLE AND IDENTITY
You are {APP_NAME}, an elite AI Personal Trainer specialized in [NOME_DELLO_SPORT]. 
Your goal is to create holistic and hyper-personalized plans that integrate specific athletic preparation and optimization of physical and mental performance.

## FUNDAMENTAL PRINCIPLES
1. Technical and Load Progressivity: Adapted to [NOME_DELLO_SPORT] metrics.
2. Focus on Technique and Execution: To maximize efficiency and prevent injuries.
3. Goal Integration: Balance between strength, endurance, technique, and tactics.
4. Sustainability and Adherence: Adaptation to the athlete's life context.
5. Safety and Longevity: Absolute priority to the health of joints and muscle groups most stressed.

## INTENSITY SYSTEM
Use RPE (Rate of Perceived Exertion) on a scale of 1-10 to monitor intensity and autoregulate the load based on daily form.

## FINAL OUTPUT FORMAT
1. EXECUTIVE SUMMARY
2. NUTRITIONAL STRATEGY
3. LONG-TERM PROGRAMMING
4. WEEKLY TRAINING PLAN
5. SAFETY PROTOCOLS
6. AUTOREGULATION SYSTEM
7. MOTIVATIONAL MESSAGE: Finalized with "- {APP_NAME}".
"""''',
    "PERSONALIZED_CONTEXT": 'PERSONALIZED_CONTEXT = """Contesto d\'élite non disponibile per [NOME_DELLO_SPORT]. Verranno seguite le linee guida generali di alta performance."""',
    "BUTTON_LOGIC": 'PROMPT_BUTTONS_LOGIC = """// Logica di fallback sicura\nconsole.log("MetaOpenCoach: Modalità provvisoria attiva.");"""',
    "VARIABLES": 'VARIABLES_TO_EXTRACT = """[]"""',
}

MODEL_NAME = os.getenv("AI_MODEL", "gemini-2.5-pro")
API_CALL_DELAY_SECONDS = 15  # Safe delay between API calls

# --- HELPER FUNCTIONS ---


def safe_py_string(text):
    """
    Sanitizza una stringa proveniente dall'LLM per renderla sicura all'interno di un file .py.
    Gestisce backslash finali, triple virgolette e residui di markdown.
    """
    if not text:
        return ""

    # 1. Rimuove eventuali blocchi di codice markdown all'inizio o alla fine
    text = re.sub(r"^```(?:python|json|text)?\n", "", text, flags=re.MULTILINE)
    text = re.sub(r"```$", "", text, flags=re.MULTILINE).strip()

    # 2. Raddoppia i backslash per evitare che l'ultimo carattere scappi le virgolette di chiusura
    # o che \n, \t etc vengano interpretati letteralmente se non voluto
    text = text.replace("\\", "\\\\")

    # 3. Gestisce le triple virgolette interne (le sostituisce con escape)
    text = text.replace('"""', '\\"\\"\\"')

    # 4. Sostituisce em-dash con dash normale per portabilità console/Windows
    text = text.replace('—', '-')

    return text


def sanitize_and_validate_block(
    code_str: str, var_name: str, sport_name: str = "MMA"
) -> str:
    """
    Pipeline a 3 stadi per validare e auto-correggere un blocco di codice Python
    generato da LLM che potrebbe contenere parentesi sbilanciate.

    Stage 1: Compiles as-is. If passes → returns immediately (normal case).
    Stage 2: Regex heuristics to balance brackets/braces,
              then recompiles. If passes → returns corrected version.
    Stage 3: Fallback for variable → safe and empty block,
              so final assembly never crashes.

    Security: never executes code (uses only compile()/ast.parse),
    so there is no risk of Remote Code Execution from LLM output.
    """
    # --- Stadi 1 e 2: Validazione e Correzione (solo se presente) ---
    if code_str:
        # Sostituiamo sistematicamente il placeholder se presente nel codice generato (spesso nei fallback auto-generati)
        code_str = code_str.replace("[NOME_DELLO_SPORT]", sport_name)

        # --- Stadio 1: Validazione AST iniziale ---
        try:
            compile(code_str, "<llm_output>", "exec")
            return code_str  # Tutto ok, nessuna modifica
        except SyntaxError:
            pass

        # --- Stadio 2: Auto-correzione heuristica ---
        print(
            f"    ⚠️ [{var_name}] SyntaxError detected. Attempting auto-correction...")
        fixed = code_str

        # Bilancia coppie di parentesi (ordine: prima le interne per non sbilanciarle)
        for open_c, close_c in [("(", ")"), ("[", "]"), ("{", "}")]:
            diff = fixed.count(open_c) - fixed.count(close_c)
            if diff > 0:
                # Mancano chiusure: le aggiunge in coda
                fixed += close_c * diff
            elif diff < 0:
                # Chiusure in eccesso: rimuove le ultime occorrenze
                for _ in range(abs(diff)):
                    idx = fixed.rfind(close_c)
                    if idx != -1:
                        fixed = fixed[:idx] + fixed[idx + 1:]

        try:
            compile(fixed, "<llm_output_fixed>", "exec")
            print(f"    ✅ [{var_name}] Auto-correction of brackets succeeded.")
            return fixed
        except SyntaxError as e2:
            print(
                f"    ⚠️ [{var_name}] Auto-correction failed: {e2}. Applying safe fallback."
            )
    else:
        print(
            f"    ⚠️ [{var_name}] No code provided for validation. Skipping to fallback."
        )

    # --- Stadio 3: Fallback sicuro per variabile ---
    for key_fragment, fallback_code in _SAFE_FALLBACKS.items():
        # More precise matching to avoid collisions (e.g. PROFILE vs CLIENTS_PROFILE)
        if key_fragment in var_name:
            print(
                f"    🔄 [{var_name}] Injecting security fallback block (match: {key_fragment})."
            )
            # Sostituiamo il placeholder del nome dello sport nel fallback
            return fallback_code.replace("[NOME_DELLO_SPORT]", sport_name)

    # Fallback generico (non dovrebbe mai arrivarci se i moduli sono mappati)
    print(f"    🔄 [{var_name}] Generic fallback (unknown module).")
    return f"# BLOCK {var_name} - INVALID SYNTAX"


def read_text_file(file_path):
    """Legge un file di testo e restituisce il suo contenuto."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(
            f"    ERRORE: Impossibile leggere il file {file_path}. Dettagli: {e}")
        return None


# Soglia minima di testo utile estratto (in caratteri).
# Un valore inferiore indica PDF protetto da password, corrotto o vuoto.
MIN_EXTRACTED_CHARS = 100


def read_document_text(file_path):
    """Extracts text from PDF, DOCX, Markdown or TXT with content validation."""
    if not os.path.exists(file_path):
        print(f"    ERROR: Document file not found: {file_path}")
        return None

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        try:
            doc = fitz.open(file_path)
            # Controllo esplicito per PDF protetti da password
            if doc.is_encrypted:  # pylint: disable=no-member
                print(
                    f"    ERROR: PDF file '{os.path.basename(file_path)}' is password protected. Cannot extract text."
                )
                return None
            text = "".join(page.get_text() for page in doc)
            # Validazione: il testo estratto deve avere una lunghezza minima significativa
            if len(text.strip()) < MIN_EXTRACTED_CHARS:
                print(
                    f"    ERROR: Extracted PDF text too short ({len(text.strip())} chars). File may be corrupted, scanned (image) or empty."
                )
                return None
            print(
                f"    ✅ PDF file '{os.path.basename(file_path)}' read successfully ({len(text)} chars)."
            )
            return text
        except Exception as e:
            print(
                f"    ERROR: Unable to read PDF file {file_path}. Details: {e}")
            return None

    elif ext == ".docx":
        try:
            import zipfile
            import xml.etree.ElementTree as ET

            text_lines = []
            with zipfile.ZipFile(file_path) as docx:
                xml_content = docx.read("word/document.xml")
                tree = ET.XML(xml_content)
                NAMESPACE = (
                    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
                )
                for paragraph in tree.iter(NAMESPACE + "p"):
                    texts = [
                        node.text
                        for node in paragraph.iter(NAMESPACE + "t")
                        if node.text
                    ]
                    if texts:
                        text_lines.append("".join(texts))
            content = "\n".join(text_lines)
            # Validazione contenuto minimo
            if len(content.strip()) < MIN_EXTRACTED_CHARS:
                print(
                    f"    ERROR: Extracted DOCX text too short ({len(content.strip())} chars). File may be corrupted or empty."
                )
                return None
            print(
                f"    ✅ DOCX file '{os.path.basename(file_path)}' read successfully ({len(content)} chars)."
            )
            return content
        except Exception as e:
            print(
                f"    ERROR: Unable to read DOCX file {file_path}. Details: {e}")
            return None

    else:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if len(content.strip()) < MIN_EXTRACTED_CHARS:
                print(
                    f"    ERROR: Text file too short ({len(content.strip())} chars). Verify file content."
                )
                return None
            print(
                f"    ✅ Text file '{os.path.basename(file_path)}' read successfully ({len(content)} chars)."
            )
            return content
        except Exception as e:
            print(
                f"    ERROR: Unable to read text file {file_path}. Details: {e}")
            return None


def find_next_config_filename(directory, sport_name):
    """Finds the next available filename (e.g. config_powerlifting_1.py)."""
    if not os.path.exists(directory):
        os.makedirs(directory)

    safe_sport_name = re.sub(r"\W+", "_", sport_name).lower()
    pattern = re.compile(rf"config_{safe_sport_name}_(\d+)\.py")
    max_num = 0
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            max_num = max(max_num, int(match.group(1)))

    return os.path.join(directory, f"config_{safe_sport_name}_{max_num + 1}.py")


# --- ROUTER UNIVERSALE E SCUDO DI SICUREZZA ---
SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}


def genera_contenuto_sicuro(model_google_obj, prompt_completo, max_tentativi=3):
    """
    Router Agnostico: Instrada la chiamata a Gemini (tramite SDK) oppure a OpenAI/Local/Anthropic (tramite REST API)
    basandosi sulle variabili d'ambiente.
    """
    model_name = os.getenv("AI_MODEL", "gemini-2.5-pro").lower()
    base_url = os.getenv("AI_BASE_URL", "").rstrip("/")
    api_key = os.getenv("AI_API_KEY", "")

    is_local = "localhost" in base_url or "127.0.0.1" in base_url

    for tentativo in range(max_tentativi):
        try:
            if "gemini" in model_name:
                risposta = model_google_obj.generate_content(
                    prompt_completo, safety_settings=SAFETY_SETTINGS
                )
                if not is_local:
                    time.sleep(12)
                return risposta

            elif "claude" in model_name:
                headers = {
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                }
                payload = {
                    "model": model_name,
                    "max_tokens": 4096,
                    "messages": [{"role": "user", "content": prompt_completo}],
                }
                url = base_url if base_url else "https://api.anthropic.com/v1/messages"
                res = requests.post(url, headers=headers, json=payload)
                res.raise_for_status()
                return type(
                    "obj", (object,), {"text": res.json()
                                       ["content"][0]["text"]}
                )

            else:
                headers = {
                    "Authorization": f"Bearer {api_key if api_key else 'lm-studio-local'}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "model": model_name,
                    "messages": [{"role": "user", "content": prompt_completo}],
                    "temperature": float(os.getenv("AI_TEMPERATURE", "0.7")),
                    "max_tokens": int(os.getenv("AI_MAX_TOKENS", "8192")),
                }

                if base_url:
                    base_url_clean = base_url.rstrip("/")
                    if (
                        "localhost" in base_url_clean or "127.0.0.1" in base_url_clean
                    ) and not base_url_clean.endswith("/v1"):
                        base_url_clean += "/v1"
                    url = f"{base_url_clean}/chat/completions"
                else:
                    url = "https://api.openai.com/v1/chat/completions"

                print(f"\n---> [DEBUG NETWORK] Contacting: {url}")
                print(f"---> [DEBUG NETWORK] Requested model: {model_name}")

                res = requests.post(url, headers=headers, json=payload)
                print(f"---> [DEBUG NETWORK] Status Code: {res.status_code}")
                res.raise_for_status()

                data = res.json()
                if "choices" not in data:
                    raise KeyError(
                        f"Server response does not contain 'choices'. RAW: {res.text}"
                    )

                estratto = data["choices"][0]["message"]["content"]
                return type("obj", (object,), {"text": estratto})

        except Exception as e:
            errore_str = str(e)
            if "ConnectionRefusedError" in errore_str or "ECONNREFUSED" in errore_str:
                print(
                    f"\n[!] CONNECTION ERROR: Unable to contact AI server at {base_url}. "
                    f"Make sure LM Studio or Ollama are running and listening."
                )
            print(
                f"\n[!] API Error detected ({model_name} - Attempt {tentativo + 1}/{max_tentativi}): {errore_str}"
            )
            if is_local:
                time.sleep(2)
            elif (
                "429" in errore_str
                or "Quota" in errore_str
                or tentativo < max_tentativi - 1
            ):
                time.sleep(65)
            else:
                raise e


def call_generative_ai(prompt, max_retries=3):
    """Invia un prompt al modello generativo e restituisce la risposta pulita."""
    ai_base_url = (
        os.getenv("AI_BASE_URL", "https://api.openai.com/v1").strip().rstrip("/")
    )
    ai_api_key = os.getenv("AI_API_KEY", "").strip()
    ai_model = os.getenv("AI_MODEL", "gpt-4o-mini").strip()

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        if "gemini" in ai_model.lower():
            try:
                import google.generativeai as genai

                genai.configure(api_key=ai_api_key)
                model = genai.GenerativeModel(ai_model)
                response = genera_contenuto_sicuro(model, prompt)
                cleaned_code = re.sub(
                    r"^```(python|json)?\n|```$", "", response.text, flags=re.MULTILINE
                ).strip()
                return cleaned_code
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "quota" in error_str.lower():
                    time.sleep(60)
                    continue
                print(f"      ❌ Gemini API ERROR: {e}")
                return None
        else:
            try:
                import json
                import urllib.request

                endpoint = f"{ai_base_url}/chat/completions"
                headers = {"Content-Type": "application/json"}
                if ai_api_key:
                    headers["Authorization"] = f"Bearer {ai_api_key}"
                data = {
                    "model": ai_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": float(os.getenv("AI_TEMPERATURE", "0.7")),
                    "max_tokens": int(os.getenv("AI_MAX_TOKENS", "8192")),
                }
                req = urllib.request.Request(
                    endpoint, data=json.dumps(data).encode("utf-8"), headers=headers
                )
                with urllib.request.urlopen(req) as resp:
                    result = json.loads(resp.read().decode("utf-8"))
                    content = result["choices"][0]["message"]["content"]
                    cleaned_code = re.sub(
                        r"^```(python|json)?\n|```$", "", content, flags=re.MULTILINE
                    ).strip()
                    return cleaned_code
            except Exception as e:
                print(f"      ❌ REST Compatible call ERROR: {e}")
                if "ECONNREFUSED" in str(e) or "10061" in str(e):
                    print(
                        f"      [!] HINT: It seems the local server ({ai_base_url}) is not responding."
                    )
                if "429" in str(e):
                    time.sleep(60)
                    continue
                return None
    return None


def sanitize_sport_name(name):
    """
    Removes dangerous characters from the sport name before using in AI prompts.
    Prevents Prompt Injection attacks via malicious input in the sport field.
    """
    # Remove newline, tab and backslash that could break the prompt context
    sanitized = re.sub(r"[\n\r\t\\]", " ", name)
    # Limit length to 60 characters to avoid prompt padding
    sanitized = sanitized.strip()[:60]
    if sanitized != name.strip():
        print(
            f"    ⚠️ Sport name sanitized from '{name.strip()[:80]}' to '{sanitized}' (dangerous characters removed)."
        )
    return sanitized


def _get_manual_override(prompt_filename: str) -> str | None:
    """
    Checks if manual override exists for the module corresponding to the prompt file.

    Security: reads only env vars with MANUAL_ prefix, max 64KB length to
    prevent payload inflation attacks. Content is never executed
    (only written to file and later compiled with compile()/ast only).

    Returns manual content (string) or None if module is in AI mode.
    """
    MAX_MANUAL_CONTENT_BYTES = 65_536  # 64 KB — limite ragionevole per sicurezza

    for key_fragment, env_var in MODULE_ENV_MAP.items():
        if key_fragment in prompt_filename:
            raw = os.environ.get(env_var, "").strip()
            if raw:
                # Sicurezza: tronca se troppo grande (previene payload inflation)
                if len(raw.encode("utf-8")) > MAX_MANUAL_CONTENT_BYTES:
                    print(
                        f"    ⚠️ [{env_var}] Contenuto manuale troncato a 64KB per sicurezza."
                    )
                    raw = raw.encode("utf-8")[:MAX_MANUAL_CONTENT_BYTES].decode(
                        "utf-8", errors="ignore"
                    )
                return raw
    return None


def generate_config_for_sport(target_sport, base_framework_text):
    """Orchestrates the configuration generation process for a single sport."""
    # Sanitize sport name BEFORE using in any AI prompt
    target_sport = sanitize_sport_name(target_sport)
    print(f"\n--- START GENERATION PROCESS FOR SPORT: '{target_sport}' ---")

    final_code_pieces = []
    total_prompts = len(PROMPT_FILES_IN_ORDER)

    for i, prompt_filename in enumerate(PROMPT_FILES_IN_ORDER):
        print(
            f"\n  ({i + 1}/{total_prompts}) Processing prompt: '{prompt_filename}'..."
        )

        # ── BYPASS MANUALE ────────────────────────────────────────────────────
        # Se l'utente ha fornito il contenuto manuale dalla UI, lo usa direttamente
        # senza consumare token AI e senza rischi di SyntaxError LLM.
        manual_content = _get_manual_override(prompt_filename)
        if manual_content is not None:
            print(
                f"    ✋ AI Bypass active: user manual injection for '{prompt_filename}'."
            )
            final_code_pieces.append(manual_content)
            continue
        # ─────────────────────────────────────────────────────────────────────

        prompt_path = os.path.join(PROMPTS_DIR, prompt_filename)
        meta_prompt_template = read_text_file(prompt_path)
        if not meta_prompt_template:
            continue

        final_prompt_instructions = meta_prompt_template.replace(
            "[NOME_DELLO_SPORT]", target_sport
        ).replace(
            "[SPORT_NAME]", target_sport
        )

        app_language = os.environ.get("APP_LANGUAGE", "Italiano")
        final_prompt_instructions = final_prompt_instructions.replace(
            "[APP_LANGUAGE]", app_language
        )

        full_prompt_for_ai = (
            f"{final_prompt_instructions}\n\n"
            "--- TESTO DI RIFERIMENTO DA ANALIZZARE E ADATTARE ---\n\n"
            f"{base_framework_text}\n\n"
            f"Devi generare il codice e i testi di risposta TASSATIVAMENTE nella seguente lingua: {app_language}."
        )

        print("    -> Sending request to AI...")
        generated_code = call_generative_ai(full_prompt_for_ai)

        if generated_code:
            # 1. Pulizia markdown residua e variabili pre-esistenti
            clean_raw = re.sub(
                r"^```(?:python|json|text)?\n|```$",
                "",
                generated_code,
                flags=re.MULTILINE,
            ).strip()

            # --- SYSTEM GUARD: Conversational Stripper 2.0 ---
            # Remove common AI "side-talk" that small models leak into code output
            side_talk_patterns = [
                r"^Certainly!.*?\n",
                r"^Ecco il codice.*?\n",
                r"^Certamente!.*?\n",
                r"^Spero che questo.*?\n",
                r"^Here is the.*?\n",
                r"^Sure, .*?\n",
                r"^Absolutely!.*?\n",
                r"^D'accordo, .*?\n",
                r"^OK, .*?\n"
            ]
            for pattern in side_talk_patterns:
                clean_raw = re.sub(pattern, "", clean_raw, flags=re.IGNORECASE | re.MULTILINE)
            
            clean_raw = clean_raw.strip()

            reformatted_code = None

            if "SYSTEM_PROMPT" in prompt_filename:
                # --- MANUALLY ENFORCED APP NAME ---
                # We use the literal name from the UI (SPORT_NAME env var)
                app_name = target_sport

                # Extract SYSTEM_PROMPT (We look for what seems to be the main text block)
                # Enhanced Regex: handles different quote styles and variable assignments more flexibly
                # Tenta di catturare il blocco anche se manca la chiusura finale (output troncato)
                sys_match = re.search(
                    r"SYSTEM_PROMPT\s*=\s*(?P<q>[\'\"]{3}|[\'\"]{1})(.*?)(?:(?P=q)|\Z)",
                    clean_raw,
                    re.DOTALL | re.IGNORECASE,
                )
                if sys_match:
                    sys_prompt = sys_match.group(2).strip("'\"")
                else:
                    # Fallback capture: try to grab everything after the variable name if assignment present
                    second_match = re.search(r"SYSTEM_PROMPT\s*=\s*(.*)", clean_raw, re.DOTALL | re.IGNORECASE)
                    if second_match:
                         sys_prompt = second_match.group(1).strip().strip("'\"")
                    else:
                        # TRUNCATION SAFETY: If AI output was cut off, take everything that remains
                        sys_prompt = clean_raw.strip()

                sys_prompt = safe_py_string(sys_prompt)
                reformatted_code = (
                    f'APP_NAME = "{app_name}"\nSYSTEM_PROMPT = """\n{sys_prompt}\n"""'
                )

            elif (
                "PROFILE_QUESTIONS" in prompt_filename
                and "CLIENTS" not in prompt_filename
            ):
                # Greedy match: everything that starts with [ and ends with ]
                json_match = re.search(
                    r"\[\s*\{.*\}\s*\]", clean_raw, re.DOTALL)
                json_content = json_match.group(0) if json_match else clean_raw
                # Fix null/bool per Python
                json_content = re.sub(r"\bnull\b", "None", json_content)
                json_content = re.sub(
                    r"\btrue\b", "True", json_content, flags=re.I)
                json_content = re.sub(
                    r"\bfalse\b", "False", json_content, flags=re.I)

                reformatted_code = f'PROFILE_QUESTIONS = """\n{safe_py_string(json_content)}\n"""'

            elif "CLIENTS_PROFILE_QUESTIONS" in prompt_filename:
                # Greedy match: everything that starts with [ and ends with ]
                list_match = re.search(
                    r"\[\s*\{.*\}\s*\]", clean_raw, re.DOTALL)
                list_content = list_match.group(0) if list_match else clean_raw
                list_content = re.sub(r"\bnull\b", "None", list_content)
                list_content = re.sub(
                    r"\btrue\b", "True", list_content, flags=re.I)
                list_content = re.sub(
                    r"\bfalse\b", "False", list_content, flags=re.I)
                reformatted_code = f"CLIENTS_PROFILE_QUESTIONS = {list_content}"

            elif "PERSONALIZED_CONTEXT" in prompt_filename:
                # Prende tutto il contenuto come stringa sicura
                context_content = (
                    clean_raw.replace("PERSONALIZED_CONTEXT =",
                                      "").strip().strip("'\"")
                )
                context_content = safe_py_string(context_content)
                reformatted_code = f'PERSONALIZED_CONTEXT = """\n{context_content}\n"""'

            elif "BUTTON_LOGIC" in prompt_filename:
                # Prende tutto il contenuto come stringa sicura
                logic_content = (
                    clean_raw.replace("PROMPT_BUTTONS_LOGIC =",
                                      "").strip().strip("'\"")
                )
                logic_content = safe_py_string(logic_content)
                reformatted_code = f'PROMPT_BUTTONS_LOGIC = """\n{logic_content}\n"""'

            elif "VARIABLES" in prompt_filename:
                # Greedy match for variable list
                var_match = re.search(
                    r"\[\s*\{.*\}\s*\]", clean_raw, re.DOTALL)
                var_content = var_match.group(0) if var_match else clean_raw
                var_content = safe_py_string(var_content)
                reformatted_code = f'VARIABLES_TO_EXTRACT = """\n{var_content}\n"""'

            if reformatted_code:
                # ── VALIDAZIONE AST BLOCCO-PER-BLOCCO ────────────────────────
                safe_block = sanitize_and_validate_block(
                    reformatted_code, prompt_filename, target_sport
                )
                final_code_pieces.append(safe_block)
                print(f"    ✅ Completed: '{prompt_filename}'.")
            else:
                print(
                    f"    ⚠️ Regex failed for '{prompt_filename}'. Applying fallback.")
                final_code_pieces.append(
                    sanitize_and_validate_block(
                        None, prompt_filename, target_sport)
                )
        else:
            print(
                f"    ⚠️ No code generated for '{prompt_filename}'. Applying fallback."
            )
            final_code_pieces.append(
                sanitize_and_validate_block(
                    None, prompt_filename, target_sport)
            )

        if i < total_prompts - 1:
            time.sleep(API_CALL_DELAY_SECONDS)

    # ── COMPLETENESS CHECK (non-fatal) ────────────────────────────────────
    if len(final_code_pieces) != len(PROMPT_FILES_IN_ORDER):
        print(
            f"\n⚠️ WARNING: Partial generation ({len(final_code_pieces)}/{len(PROMPT_FILES_IN_ORDER)} modules). "
            "Continuing with available modules to not lose work already done."
        )
        # No longer exits with sys.exit(1) — continues to save partial
        if not final_code_pieces:
            print("\n[!] No module generated. Cannot proceed with this sport.")
            return  # Returns, but doesn't crash the entire batch process

    print("\n  ASSEMBLING FINAL CONFIGURATION FILE...")
    final_output_code = "\n\n".join(final_code_pieces)

    # ── VALIDAZIONE FINALE DELL'ASSEMBLATO ───────────────────────────────────
    # Double-check sull'intero file assemblato. Questa volta, invece di
    # sys.exit(1), tenta una correzione di emergenza e scrive comunque su disco.
    try:
        compile(final_output_code, "<generated_config>", "exec")
        print("  ✅ Final syntax validation PASSED.")
    except SyntaxError as e:
        print(f"\n[!] SYNTAX ERROR in assembled file: {e}")
        print("    Attempting emergency correction on entire file...")
        final_output_code = sanitize_and_validate_block(
            final_output_code, "ASSEMBLED_CONFIG", target_sport
        )
        try:
            compile(final_output_code, "<generated_config_fixed>", "exec")
            print("  ✅ Emergency correction SUCCEEDED.")
        except SyntaxError as e_final:
            # Worst case: writes file with error comment at top, but doesn't crash.
            print(
                f"  ⛔ Correction impossible: {e_final}. File will be written with warning at top."
            )
            final_output_code = (
                f"# [!] WARNING: File generated with syntax errors. Review manually.\n# Error: {e_final}\n\n"
                + final_output_code
            )

    output_filename = find_next_config_filename(OUTPUT_DIR, target_sport)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(final_output_code)
    print(f"\n🎉 SUCCESS! Saved to: '{output_filename}'")


def main():
    """Configures the environment and starts the generation process."""
    print("--- STARTING CONFIGURATION GENERATION SCRIPT ---")
    ai_model = os.getenv("AI_MODEL", "gpt-4o-mini").strip()
    print(f"✅ Using model: '{ai_model}'")

    # --- DOCUMENT RETRIEVAL LOGIC (Improved) ---
    doc_text = None
    if os.path.exists(BASE_DOC_PATH):
        doc_text = read_document_text(BASE_DOC_PATH)
    else:
        print(f"    ⚠️ Default document not found: {BASE_DOC_PATH}")
        print(
            "    Attempting automatic search for an alternative document in data_input..."
        )

        data_input_dir = os.path.dirname(BASE_DOC_PATH)
        if os.path.exists(data_input_dir):
            for sport in SPORTS_TO_GENERATE:
                # Search for files containing the sport name (case insensitive)
                candidates = [
                    f
                    for f in os.listdir(data_input_dir)
                    if sport.lower() in f.lower()
                    and f.lower().endswith((".pdf", ".docx", ".txt", ".md"))
                ]
                if candidates:
                    chosen_file = os.path.join(data_input_dir, candidates[0])
                    print(f"    🔍 Found related document: {chosen_file}")
                    doc_text = read_document_text(chosen_file)
                    if doc_text:
                        break

        if not doc_text:
            # Extreme fallback: search for first useful file (not .gitkeep)
            print(
                "    ⚠️ No specific document found. Searching for first available file..."
            )
            all_files = [
                f
                for f in os.listdir(data_input_dir)
                if not f.startswith(".")
                and f.lower().endswith((".pdf", ".docx", ".txt", ".md"))
            ]
            if all_files:
                chosen_file = os.path.join(data_input_dir, all_files[0])
                print(f"    🔍 Using generic file: {chosen_file}")
                doc_text = read_document_text(chosen_file)

    if not doc_text:
        print(
            "❌ Error: No reference document found or readable. Cannot proceed."
        )
        sys.exit(1)

    for sport in SPORTS_TO_GENERATE:
        generate_config_for_sport(sport, doc_text)
    print("\n--- ALL PROCESSES COMPLETED ---")


if __name__ == "__main__":
    main()
