import os
import sys
import shutil
import signal
import threading
import subprocess
import re
import customtkinter as ctk
from tkinter import filedialog, messagebox

# ═══════════════════════════════════════════════════════════════
# LOCALIZATION — UI strings (EN / IT)
# ═══════════════════════════════════════════════════════════════
STRINGS = {
    "EN": {
        "title": "MetaOpenCoach — App Builder",
        "title_bar": "MetaOpenCoach - Backend & App Builder",
        "card_identity": "Sport & Identity",
        "sport_placeholder": "Sport name (e.g. MMA)",
        "load_doc": "Load Reference Document",
        "no_file": "No file selected",
        "card_ai": "AI Engine",
        "advanced": "Advanced Options",
        "ai_temp": "AI Temperature",
        "tooltip_temp": "0-1. Higher = more creative, lower = more deterministic.",
        "card_goal": "Primary Goal",
        "goal_hint": "Key of the numeric goal (e.g. weight or pullups)",
        "goal_placeholder": "e.g. weight",
        "app_name_label": "App Name (Override)",
        "app_name_placeholder": "Manual name (e.g. MyCalisthenicsApp)",
        "app_name_desc": "Application name is mandatory and must be entered by the user.",
        "warn_no_app_name": "Application name is required.",
        "warn_folder_exists": "An app with the name '{}' already exists in generated_output. Please choose a different name.",
        "card_export": "Export",
        "add_queue": "Add to Generation Queue",
        "card_queue": "Work Queue",
        "queue_empty": "Queue is empty.",
        "card_control": "Control Panel",
        "btn_start": "START",
        "btn_stop": "STOP ALL",
        "card_logs": "Logs & Details",
        "show_logs": "Show Technical Logs",
        "log_removed": "Removed: ",
        "log_restored": "Item restored to editor for editing.",
        "warn_no_sport": "Sport name is required.",
        "warn_no_file": "Select a reference document first.",
        "warn_busy": "A batch process is already running.",
        "warn_queue_empty": "Add at least one app to the queue before starting.",
        "batch_started": "BATCH PROCESS STARTED",
        "batch_done": "BATCH COMPLETED. {} OK — {} Errors",
        "batch_cancelled": "BATCH CANCELLED BY USER.",
        "interrupted": "Process for {} forcibly stopped.",
        "app_done": "{} — COMPLETED SUCCESSFULLY!",
        "app_error": "{} — GENERATION FAILED.",
        "stopping": "Stopping...",
        "interrupt_all": "STOP ALL",
        "ai_label": "Generate with AI",
        "manual_label": "Manual Input",
        "bypass_log": "AI bypass active — manual injection for {}",
        "system_prompt_title": "Personality & Traits",
        "system_prompt_desc": "Tone of voice and character of the coach",
        "profile_questions_title": "Onboarding Questions",
        "profile_questions_desc": "What to ask the athlete at first login",
        "clients_profile_questions_title": "Advanced Client Profile",
        "clients_profile_questions_desc": "Specific data for technical monitoring",
        "personalized_context_title": "RAG Context & Knowledge",
        "personalized_context_desc": "Base knowledge from reference documents",
        "button_logic_title": "Button Prompt Logic",
        "button_logic_desc": "Automations for quick-action buttons",
        "variables_title": "Variables to Extract",
        "variables_desc": "Structured metrics for tracking",
        "metrics_title": "Progress Tracking (Metrics)",
        "metrics_desc": "Dynamic data fields for progress charts",
        "primary_goal_title": "Primary Goal (Tracking %)",
        "primary_goal_desc": "Key of the numeric goal (e.g. weight or pullups)",
        "export_title": "Export",
        "batch_in_progress": "A batch process is already running.",
        "queue_empty_title": "Queue empty",
        "generating": "Batch generation in progress...",
        "interrupted_title": "Interrupted",
        "interrupted_msg": "Batch generation stopped. All processes and the queue have been cleared.",
        "completed_title": "Batch Completed",
        "dialog_warning": "Warning",
        "dialog_processing": "Processing",
        "dialog_ok_title": "OK",
    },
    "IT": {
        "title": "MetaOpenCoach — Generatore App",
        "title_bar": "MetaOpenCoach - Backend & App Builder",
        "card_identity": "Sport e Identità",
        "sport_placeholder": "Nome dello Sport (es. MMA)",
        "load_doc": "Carica Documento Base",
        "no_file": "Nessun file selezionato",
        "card_ai": "Cervello Artificiale",
        "advanced": "Opzioni Avanzate",
        "ai_temp": "Temperatura AI",
        "tooltip_temp": "0-1. Più alto = più creativo, più basso = deterministico.",
        "card_goal": "Obiettivo Primario",
        "goal_hint": "Chiave dell'obiettivo numerico (es. weight o pullups)",
        "goal_placeholder": "Es: weight",
        "app_name_label": "Nome App (Override)",
        "app_name_placeholder": "Nome manuale (es. MenteD)",
        "app_name_desc": "Il nome dell'applicazione è obbligatorio e deve essere inserito dall'utente.",
        "warn_no_app_name": "Il nome dell'applicazione è obbligatorio.",
        "warn_folder_exists": "Un'app con il nome '{}' esiste già in generated_output. Scegli un nome diverso.",
        "card_export": "Esportazione",
        "add_queue": "Aggiungi alla Coda di Generazione",
        "card_queue": "Coda di Lavoro",
        "queue_empty": "Coda Vuota.",
        "card_control": "Pannello di Controllo",
        "btn_start": "AVVIA",
        "btn_stop": "INTERROMPI TUTTO",
        "card_logs": "Log e Dettagli",
        "show_logs": "Mostra Log Tecnici",
        "log_removed": "Rimosso: ",
        "log_restored": "Elemento ripristinato nell'editor per la modifica.",
        "warn_no_sport": "Il nome dello sport è obbligatorio.",
        "warn_no_file": "Seleziona un file base da analizzare.",
        "warn_busy": "Un processo batch è già in corso.",
        "warn_queue_empty": "Aggiungi almeno un'app alla coda prima di avviare.",
        "batch_started": "AVVIO PROCESSO BATCH",
        "batch_done": "BATCH TERMINATO. {} OK — {} Errori",
        "batch_cancelled": "ELABORAZIONE BATCH CANCELLATA DALL'UTENTE.",
        "interrupted": "Processo per {} forzatamente interrotto.",
        "app_done": "{} — COMPLETATA CON SUCCESSO!",
        "app_error": "{} — GENERAZIONE FALLITA.",
        "stopping": "Interrompendo...",
        "interrupt_all": "INTERROMPI TUTTO",
        "ai_label": "Genera con AI",
        "manual_label": "Inserisci Manuale",
        "bypass_log": "Bypass AI attivo — iniezione manuale per {}",
        "system_prompt_title": "Personality & Traits",
        "system_prompt_desc": "Tono di voce e carattere del coach (English desc)",
        "profile_questions_title": "Onboarding Questions",
        "profile_questions_desc": "Cosa chiedere all'atleta al primo login (English desc)",
        "clients_profile_questions_title": "Advanced Client Profile",
        "clients_profile_questions_desc": "Dati specifici per il monitoraggio tecnico (English desc)",
        "personalized_context_title": "RAG Context & Knowledge",
        "personalized_context_desc": "Insegnamenti base dai doc di riferimento (English desc)",
        "button_logic_title": "Button Prompt Logic",
        "button_logic_desc": "Automazioni per i bottoni di azione rapida (English desc)",
        "variables_title": "Variables to Extract",
        "variables_desc": "Metriche strutturate per il tracking (English desc)",
        "metrics_title": "Progress Tracking (Metrics)",
        "metrics_desc": "Campi dati dinamici per i grafici di progresso (English desc)",
        "primary_goal_title": "Obiettivo Primario (Tracciamento %)",
        "primary_goal_desc": "Indica la chiave dell'obiettivo numerico (es. weight o pullups)",
        "export_title": "Esportazione",
        "batch_in_progress": "Un processo batch è già in corso.",
        "queue_empty_title": "Coda vuota",
        "generating": "Generazione Batch in corso...",
        "interrupted_title": "Interrotto",
        "interrupted_msg": "Generazione batch interrotta. Tutti i processi e la coda sono stati azzerati.",
        "completed_title": "Batch Completato",
        "dialog_warning": "Attenzione",
        "dialog_processing": "In elaborazione",
        "dialog_ok_title": "OK",
        "personality_title": "Personality & Traits",
        "personality_desc": "Tone of voice and character of the coach",
        "onboarding_title": "Onboarding Questions",
        "onboarding_desc": "What to ask the athlete at first login",
        "advanced_profile_title": "Advanced Client Profile",
        "advanced_profile_desc": "Specific data for technical monitoring",
        "context_title": "RAG Context & Knowledge",
        "context_desc": "Base knowledge from reference documents",
        "logic_title": "Button Prompt Logic",
        "logic_desc": "Automations for quick-action buttons",
        "extraction_title": "Variables to Extract",
        "extraction_desc": "Structured metrics for tracking",
    },
}


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = ctk.CTkLabel(
            tw,
            text=self.text,
            justify="left",
            fg_color=("gray85", "gray25"),
            text_color=("black", "white"),
            corner_radius=6,
            padx=10,
            pady=10,
        )
        label.pack()

    def leave(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class Card(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(
            master, fg_color=("gray85", "gray20"), corner_radius=10, **kwargs
        )
        self.title_label = None
        if title:
            lbl = ctk.CTkLabel(
                self, text=title, font=ctk.CTkFont(size=16, weight="bold")
            )
            lbl.pack(anchor="w", padx=15, pady=(15, 5))
            self.title_label = lbl
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=15, pady=(0, 15))


# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_INPUT_DIR = os.path.join(BASE_DIR, "data_input")
ORCHESTRATORE_PATH = os.path.join(BASE_DIR, "src_python", "orchestrator.py")

# Layout and Theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Map: module_id → env var produced for geco5gemini.py
_MODULE_ENV_MAP = {
    "system_prompt": "MANUAL_SYSTEM_PROMPT",
    "profile_questions": "MANUAL_PROFILE_QUESTIONS",
    "clients_profile_questions": "MANUAL_CLIENTS_PROFILE_QUESTIONS",
    "personalized_context": "MANUAL_PERSONALIZED_CONTEXT",
    "button_logic": "MANUAL_BUTTON_LOGIC",
    "variables": "MANUAL_VARIABLES",
    "metrics": "CUSTOM_PROGRESS_HTML",  # backward compatibility
}

# English default contents for each manual textbox
_DEFAULT_CONTENTS = {
    "system_prompt": (
        'APP_NAME = "IronMaster Pro"\n'
        'SYSTEM_PROMPT = """\n'
        "You are an elite Calisthenics coach. Focus on progressive overload, Front Lever, Planche, and Muscle-up.\n"
        "Goal: perfect form and explosive strength. Every session must include scapular activation and core work.\n"
        "Always sign as - {APP_NAME}.\n"
        '"""'
    ),
    "profile_questions": (
        "[\n"
        '  {"id": "weight", "label": "Body Weight (kg)", "type": "number", "required": true},\n'
        '  {"id": "max_pullups", "label": "Max Pull-ups (Strict)", "type": "number", "required": true},\n'
        '  {"id": "max_dips", "label": "Max Dips (Strict)", "type": "number", "required": true},\n'
        '  {"id": "pl_lean_hold", "label": "Planche Lean Hold (sec)", "type": "number", "required": false}\n'
        "]"
    ),
    "clients_profile_questions": (
        "[\n"
        '  {"id": "target_weight", "label": "Target Weight (kg)", "type": "number", "required": true},\n'
        '  {"id": "target_muscleup", "label": "Target Muscle-up (Reps)", "type": "number", "required": true},\n'
        '  {"id": "target_planche", "label": "Target Planche Hold (sec)", "type": "number", "required": true}\n'
        "]"
    ),
    "personalized_context": (
        "Context for Calisthenics athlete:\n\n"
        "- Focus on wrist and shoulder joint mobility\n"
        "- Injury screening: epicondylitis, rotator cuff\n"
        "- Equipment: high parallettes, bar, rings, loop bands"
    ),
    "button_logic": (
        'PROMPT_BUTTONS_LOGIC = """\n'
        'Button 1: "Skill Progression" → Generate micro-cycle to unlock Planche/Front Lever\n'
        'Button 2: "Max Test" → RPE analysis and suggest new loads/reps\n'
        'Button 3: "Mobility Protocol" → Specific routine for injury prevention\n'
        '"""'
    ),
    "variables": (
        "[\n"
        '  {"name": "current_weight", "description": "Current weight", "type": "number"},\n'
        '  {"name": "pullups_done", "description": "Pull-ups done", "type": "number"}\n'
        "]"
    ),
    "metrics": (
        '    <div class="form-group">\n'
        '        <label for="current-weight">Current Weight (kg)</label>\n'
        '        <input type="number" id="current-weight" class="form-control" step="0.1" placeholder="Ex: 75.5">\n'
        "    </div>\n"
        '    <div class="form-group">\n'
        '        <label for="pullups-max">Current Max Pull-ups</label>\n'
        '        <input type="number" id="pullups-max" class="form-control" step="1" placeholder="Ex: 15">\n'
        '    </div>\n'
        '    <div class="form-group">\n'
        '        <label for="stress-level">Stress Level (1-10)</label>\n'
        '        <input type="number" id="stress-level" class="form-control" min="1" max="10" placeholder="1=min, 10=max">\n'
        "    </div>"
    ),
}


class AppBuilderUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.lang = ctk.StringVar(value="EN")
        self.title(STRINGS["EN"]["title_bar"])
        self.geometry("1200x860")
        self.minsize(1000, 700)
        self.selected_file_path = None
        self.generation_queue = []
        self.is_processing = False
        self.is_cancelled = False
        self.app_name_var = ctk.StringVar()
        self.current_process = None
        self._worker_thread = None
        self._start_lock = threading.Lock()
        self._MANUAL_LABEL = "\u270d\ufe0f Manual Insert"
        self._AI_LABEL = "\U0001f916 Generate with AI"

        # State dictionaries for universal God-Mode
        # module_id → ctk.StringVar  ("auto" | "manual")
        self._module_mode: dict[str, ctk.StringVar] = {}
        # module_id → ctk.CTkTextbox
        self._module_textbox: dict[str, ctk.CTkTextbox] = {}
        # module_id → Card
        self._module_cards: dict[str, Card] = {}
        # module_id → desc label (CTkLabel)
        self._module_card_desc_labels: dict[str, ctk.CTkLabel] = {}

        self._create_widgets()

    # ══════════════════════════════════════════════════════════════════════════
    # FACTORY METHOD — God-Mode Card
    # ══════════════════════════════════════════════════════════════════════════

    def _build_module_card(
        self,
        parent,
        module_id: str,
        title: str,
        description: str,
        default_content: str,
        textbox_height: int = 160,
    ) -> Card:
        """
        Factory that builds a Card with AI/Manual selector and pre-filled textbox.

        Saves references to:
          self._module_mode[module_id]    → StringVar ('auto'/'manual')
          self._module_textbox[module_id] → CTkTextbox
        """
        card = Card(parent, title)

        desc_lbl = ctk.CTkLabel(
            card.content,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"),
        )
        desc_lbl.pack(anchor="w", pady=(0, 8))

        mode_var = ctk.StringVar(value="auto")
        self._module_mode[module_id] = mode_var

        seg = ctk.CTkSegmentedButton(
            card.content,
            values=[self._AI_LABEL, self._MANUAL_LABEL],
            variable=mode_var,
            command=lambda val, mid=module_id: self._on_module_mode_changed(
                mid),
        )
        seg.pack(fill="x", pady=(0, 10))

        tb = ctk.CTkTextbox(
            card.content,
            height=textbox_height,
            font=ctk.CTkFont(family="Consolas", size=11),
        )
        tb.insert("1.0", default_content)
        tb.pack_forget()  # Nascosta di default (modalità AI)
        self._module_textbox[module_id] = tb

        self._module_cards[module_id] = card
        self._module_card_desc_labels[module_id] = desc_lbl

        return card

    def _on_module_mode_changed(self, module_id: str) -> None:
        """Shows/hides the textbox based on the chosen mode."""
        mode = self._module_mode[module_id].get()
        tb = self._module_textbox[module_id]
        if mode == self._MANUAL_LABEL:
            tb.pack(fill="both", expand=True, pady=(0, 10))
        else:
            tb.pack_forget()

    def _is_manual(self, module_id: str) -> bool:
        """Returns True if the module is in Manual mode."""
        return self._module_mode[module_id].get() == self._MANUAL_LABEL

    def _get_module_content(self, module_id: str) -> str:
        """Returns the content of the module's textbox (only if manual)."""
        if self._is_manual(module_id):
            return self._module_textbox[module_id].get("1.0", "end").strip()
        return ""

    def _S(self, key):
        """Short-hand for STRINGS[self.lang.get()][key]."""
        return STRINGS[self.lang.get()][key]

    # ══════════════════════════════════════════════════════════════════════════
    # WIDGET CONSTRUCTION
    # ══════════════════════════════════════════════════════════════════════════

    def _create_widgets(self):
        S = STRINGS[self.lang.get()]

        # --- Language selector (top-right) ---
        lang_frame = ctk.CTkFrame(self, fg_color="transparent")
        lang_frame.pack(anchor="ne", padx=15, pady=5)
        ctk.CTkLabel(lang_frame, text="\U0001f310", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=4
        )
        ctk.CTkOptionMenu(
            lang_frame,
            values=["EN", "IT"],
            variable=self.lang,
            width=70,
            command=lambda _: self.refresh_ui_strings(),
        ).pack(side="left")

        # --- MAIN TWO-COLUMN GRID ---
        self.main_grid = ctk.CTkFrame(self, fg_color="transparent")
        self.main_grid.pack(fill="both", expand=True, padx=20, pady=10)

        self.main_grid.rowconfigure(0, weight=1)
        self.main_grid.columnconfigure(0, weight=45)
        self.main_grid.columnconfigure(1, weight=55)

        # ══════════════════════════════════════════════════════
        # LEFT COLUMN: INPUT AND SETTINGS (45%)
        # ══════════════════════════════════════════════════════
        self.left_col = ctk.CTkScrollableFrame(
            self.main_grid, fg_color="transparent")
        self.left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # ── Header Title (Internal) ───────────
        self.lbl_title = ctk.CTkLabel(
            self.left_col,
            text="App Batch Generator",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.lbl_title.pack(pady=(10, 20))

        # ── Card 1.2: App Settings (PRIORITY) ──────────
        self.c_app_settings = Card(self.left_col, S["app_name_label"])
        self.c_app_settings.pack(fill="x", pady=(0, 15))

        self.entry_app_name = ctk.CTkEntry(
            self.c_app_settings.content,
            placeholder_text=S["app_name_placeholder"],
            textvariable=self.app_name_var
        )
        self.entry_app_name.pack(fill="x", pady=(0, 5))

        self.lbl_app_name_desc = ctk.CTkLabel(
            self.c_app_settings.content,
            text=S["app_name_desc"],
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="left"
        )
        self.lbl_app_name_desc.pack(anchor="w")

        # ── Card 1: Coach Identity ─────────────────────
        self.c_identity = Card(self.left_col, S["card_identity"])
        self.c_identity.pack(fill="x", pady=(0, 15))

        self.entry_sport = ctk.CTkEntry(
            self.c_identity.content, placeholder_text=S["sport_placeholder"]
        )
        self.entry_sport.pack(fill="x", pady=(0, 10))

        self.combo_lang = ctk.CTkComboBox(
            self.c_identity.content,
            values=["Italiano", "English", "Español", "Français", "Deutsch"],
        )
        self.combo_lang.set("Italiano")
        self.combo_lang.pack(fill="x", pady=(0, 10))

        btn_frame = ctk.CTkFrame(
            self.c_identity.content, fg_color="transparent")
        btn_frame.pack(fill="x")
        self.btn_select_file = ctk.CTkButton(
            btn_frame, text="📄 " + S["load_doc"], command=self.select_file, height=35
        )
        self.btn_select_file.pack(side="left")
        self.lbl_selected_file = ctk.CTkLabel(btn_frame, text=S["no_file"])
        self.lbl_selected_file.pack(side="left", padx=10)

        # ── Card 2: Artificial Intelligence (AI) ─────────────
        self.c_ai = Card(self.left_col, S["card_ai"])
        self.c_ai.pack(fill="x", pady=(0, 15))

        self.combo_url = ctk.CTkComboBox(
            self.c_ai.content,
            values=[
                "LM Studio (Locale)",
                "Ollama (Locale sul tuo PC)",
                "OpenAI (Cloud Predefinito)",
                "Groq (Cloud Veloce)",
                "Gemini (Google)",
                "Anthropic (Claude)",
                "Inserimento Manuale...",
            ],
        )
        self.combo_url.set("LM Studio (Locale)")
        self.combo_url.pack(fill="x", pady=(0, 10))

        self.combo_model = ctk.CTkComboBox(
            self.c_ai.content,
            values=[
                "qwen3.5-2b",
                "gemini-2.1-pro",
                "gemini-2.1-flash",
                "gpt-4o",
                "gpt-4o-mini",
                "claude-3-5-sonnet-latest",
                "llama3.1",
                "Mistral",
                "Manual Entry...",
            ],
        )
        self.combo_model.set("qwen3.5-2b")
        self.combo_model.pack(fill="x", pady=(0, 10))

        self.entry_key = ctk.CTkEntry(
            self.c_ai.content,
            show="*",
            placeholder_text="API Key (Opzionale per modelli locali)",
        )
        self.entry_key.pack(fill="x", pady=(0, 10))

        # ── Advanced Options ──
        self.lbl_adv = ctk.CTkLabel(
            self.c_ai.content,
            text=S["advanced"],
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        self.lbl_adv.pack(anchor="w")

        adv_frame = ctk.CTkFrame(self.c_ai.content, fg_color="transparent")
        adv_frame.pack(fill="x", pady=(0, 5))

        self.lbl_temp = ctk.CTkLabel(
            adv_frame, text=S["ai_temp"] + ":", font=ctk.CTkFont(size=11)
        )
        self.lbl_temp.pack(side="left", padx=(0, 5))
        self.entry_temp = ctk.CTkEntry(
            adv_frame, width=60, placeholder_text="0.6")
        self.entry_temp.insert(0, "0.6")
        self.entry_temp.pack(side="left")

        self.tooltip_temp = ToolTip(self.entry_temp, S["tooltip_temp"])

        # ── God-Mode Cards (generative modules) ───────────────
        # Each card uses _build_module_card() — same layout, different default

        self._build_module_card(
            self.left_col,
            module_id="system_prompt",
            title=S["system_prompt_title"],
            description=S["system_prompt_desc"],
            default_content=_DEFAULT_CONTENTS["system_prompt"],
            textbox_height=140,
        ).pack(fill="x", pady=(0, 15))

        self._build_module_card(
            self.left_col,
            module_id="profile_questions",
            title=S["profile_questions_title"],
            description=S["profile_questions_desc"],
            default_content=_DEFAULT_CONTENTS["profile_questions"],
            textbox_height=130,
        ).pack(fill="x", pady=(0, 15))

        self._build_module_card(
            self.left_col,
            module_id="clients_profile_questions",
            title=S["clients_profile_questions_title"],
            description=S["clients_profile_questions_desc"],
            default_content=_DEFAULT_CONTENTS["clients_profile_questions"],
            textbox_height=130,
        ).pack(fill="x", pady=(0, 15))

        self._build_module_card(
            self.left_col,
            module_id="personalized_context",
            title=S["personalized_context_title"],
            description=S["personalized_context_desc"],
            default_content=_DEFAULT_CONTENTS["personalized_context"],
            textbox_height=130,
        ).pack(fill="x", pady=(0, 15))

        self._build_module_card(
            self.left_col,
            module_id="button_logic",
            title=S["button_logic_title"],
            description=S["button_logic_desc"],
            default_content=_DEFAULT_CONTENTS["button_logic"],
            textbox_height=140,
        ).pack(fill="x", pady=(0, 15))

        self._build_module_card(
            self.left_col,
            module_id="variables",
            title=S["variables_title"],
            description=S["variables_desc"],
            default_content=_DEFAULT_CONTENTS["variables"],
            textbox_height=130,
        ).pack(fill="x", pady=(0, 15))

        self._build_module_card(
            self.left_col,
            module_id="metrics",
            title=S["metrics_title"],
            description=S["metrics_desc"],
            default_content=_DEFAULT_CONTENTS["metrics"],
            textbox_height=150,
        ).pack(fill="x", pady=(0, 15))

        # --- PRIMARY GOAL SELECTOR ---
        self.c_goal = Card(self.left_col, S["primary_goal_title"])
        self.c_goal.pack(fill="x", pady=(0, 15))
        self.lbl_goal_hint = ctk.CTkLabel(
            self.c_goal.content,
            text=S["primary_goal_desc"],
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        )
        self.lbl_goal_hint.pack(anchor="w", pady=(0, 5))
        self.entry_primary_goal = ctk.CTkEntry(
            self.c_goal.content, placeholder_text=S["goal_placeholder"]
        )
        self.entry_primary_goal.insert(0, "weight")
        self.entry_primary_goal.pack(fill="x")

        # ── Export Card ─────────────────────────────────
        self.c_export = Card(self.left_col, S["export_title"])
        self.c_export.pack(fill="x", pady=(0, 10))
        self.combo_os = ctk.CTkComboBox(
            self.c_export.content,
            values=[
                "Windows (.exe) - Predefinito",
                "Linux (Binario)",
                "macOS (Binario)",
                "Tutti e 3 (Multi-OS)",
            ],
        )
        self.combo_os.set("Windows (.exe) - Predefinito")
        self.combo_os.pack(fill="x", pady=(0, 15))
        self.btn_add_queue = ctk.CTkButton(
            self.c_export.content,
            text="➕ " + S["add_queue"],
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            fg_color="#2b7b41",
            hover_color="#1e5c30",
            command=self.add_to_queue,
        )
        self.btn_add_queue.pack(fill="x")

        # ══════════════════════════════════════════════════════
        # RIGHT COLUMN: QUEUE AND CONSOLE (55%)
        # ══════════════════════════════════════════════════════
        self.right_col = ctk.CTkScrollableFrame(
            self.main_grid, fg_color="transparent")
        self.right_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.right_col.columnconfigure(0, weight=1)

        # ── Card: Work Queue ──────────────────────────────
        self.c_queue = Card(self.right_col, S["card_queue"])
        self.c_queue.pack(fill="x", pady=(0, 15))
        self.queue_frame = ctk.CTkScrollableFrame(
            self.c_queue.content, height=140, fg_color="transparent"
        )
        self.queue_frame.pack(fill="both", expand=True)

        # ── Card: Control Panel ───────────────────────
        self.c_control = Card(self.right_col, S["card_control"])
        self.c_control.pack(fill="x", pady=(0, 15))
        ctl_frame = ctk.CTkFrame(
            self.c_control.content, fg_color="transparent")
        ctl_frame.pack(fill="x", expand=True)
        ctl_frame.columnconfigure(0, weight=1)
        ctl_frame.columnconfigure(1, weight=1)

        self.btn_generate = ctk.CTkButton(
            ctl_frame,
            text="\U0001f680 " + S["btn_start"],
            height=55,
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.start_generation_loop,
        )
        self.btn_generate.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.btn_cancel = ctk.CTkButton(
            ctl_frame,
            text="\U0001f6d1 " + S["btn_stop"],
            height=55,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#b82121",
            hover_color="#8a1717",
            state="disabled",
            command=self.cancel_generation,
        )
        self.btn_cancel.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # ── Card: Log e Dettagli ──────────────────────────────
        self.c_logs = Card(self.right_col, S["card_logs"])
        self.c_logs.pack(fill="x", pady=(0, 0))

        switch_frame = ctk.CTkFrame(
            self.c_logs.content, fg_color="transparent")
        switch_frame.pack(fill="x", pady=(0, 8))
        self.show_logs_var = ctk.BooleanVar(value=True)
        self.switch_logs = ctk.CTkSwitch(
            switch_frame,
            text=S["show_logs"],
            variable=self.show_logs_var,
            command=self.toggle_logs,
        )
        self.switch_logs.pack(side="left")

        self.console_textbox = ctk.CTkTextbox(
            self.c_logs.content,
            height=400,
            font=ctk.CTkFont(family="Consolas", size=12),
        )
        self.console_textbox.pack(fill="both", expand=True)

        # Apply EN strings on first load
        self.refresh_ui_strings()

    # ══════════════════════════════════════════════════════════════════════════
    # REFRESH UI STRINGS
    # ══════════════════════════════════════════════════════════════════════════

    def refresh_ui_strings(self):
        """Updates all widgets with the strings of the current language."""
        S = STRINGS[self.lang.get()]

        # Window title
        self.title(S["title_bar"])

        # Main title label
        self.lbl_title.configure(text=S["title"])

        # Card title labels
        for card, key in [
            (self.c_identity, "card_identity"),
            (self.c_app_settings, "app_name_label"),
            (self.c_ai, "card_ai"),
            (self.c_goal, "primary_goal_title"),
            (self.c_export, "export_title"),
            (self.c_queue, "card_queue"),
            (self.c_control, "card_control"),
            (self.c_logs, "card_logs"),
        ]:
            if card.title_label:
                card.title_label.configure(text=S[key])

        # Buttons
        self.btn_generate.configure(text="\U0001f680 " + S["btn_start"])
        self.btn_cancel.configure(text="\U0001f6d1 " + S["btn_stop"])
        self.btn_add_queue.configure(text="➕ " + S["add_queue"])
        self.btn_select_file.configure(text="📄 " + S["load_doc"])

        # Switch
        self.switch_logs.configure(text=S["show_logs"])

        # Labels
        self.lbl_adv.configure(text=S["advanced"])
        self.lbl_temp.configure(text=S["ai_temp"] + ":")
        self.lbl_goal_hint.configure(text=S["primary_goal_desc"])
        self.entry_app_name.configure(
            placeholder_text=S["app_name_placeholder"])
        self.lbl_app_name_desc.configure(text=S["app_name_desc"])

        # Segmented buttons in module cards
        for mid, seg in [
            (mid, self._module_cards[mid].content.winfo_children()[1])
            for mid in self._module_cards
        ]:
            if isinstance(seg, ctk.CTkSegmentedButton):
                current_mode = self._module_mode[mid].get()
                seg.configure(values=[self._AI_LABEL, self._MANUAL_LABEL])
                self._module_mode[mid].set(current_mode)

        # Module card title labels
        for mid, card in self._module_cards.items():
            if card.title_label:
                card.title_label.configure(text=S[f"{mid}_title"])
            # Update description if it exists (assuming it's the second child of Card content or similar)
            # Actually, we don't store ref to description label easily, but we can look for it
            for child in card.content.winfo_children():
                if isinstance(child, ctk.CTkLabel) and child != card.title_label:
                    if mid + "_desc" in S:
                        child.configure(text=S[mid + "_desc"])
                        break
                title_key = mid + "_title"
                if title_key in S:
                    card.title_label.configure(text=S[title_key])

        # Module card description labels
        for mid, lbl in self._module_card_desc_labels.items():
            desc_key = mid + "_desc"
            if desc_key in S:
                lbl.configure(text=S[desc_key])

        # Placeholders
        self.entry_sport.configure(placeholder_text=S["sport_placeholder"])
        self.entry_primary_goal.configure(
            placeholder_text=S["goal_placeholder"])

        # Queue empty label (if visible)
        for w in self.queue_frame.winfo_children():
            if isinstance(w, ctk.CTkLabel) and w.cget("text_color") == "gray":
                w.configure(text=S["queue_empty"])

        # Tooltip
        self.tooltip_temp.text = S["tooltip_temp"]

        # Dynamic button texts (if not in default state)
        if self.btn_generate.cget("state") == "disabled" and self.is_processing:
            self.btn_generate.configure(text=S["generating"])
        if self.btn_cancel.cget("text") == S.get("stopping", ""):
            pass  # already localized
        # Catch the old Italian stopping text
        current_cancel = self.btn_cancel.cget("text")
        if current_cancel.endswith("Interrompendo..."):
            self.btn_cancel.configure(text=S["stopping"])

    # ══════════════════════════════════════════════════════════════════════════
    # UI AND EVENT HANDLERS
    # ══════════════════════════════════════════════════════════════════════════

    def toggle_logs(self):
        if self.show_logs_var.get():
            self.console_textbox.pack(fill="both", expand=True)
        else:
            self.console_textbox.pack_forget()

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Base Document (e.g. PDF, DOCX, MD, TXT)",
            filetypes=(
                ("Documents", "*.pdf;*.docx;*.md;*.txt"),
                ("PDF", "*.pdf"),
                ("Word", "*.docx"),
                ("Markdown", "*.md"),
                ("Text", "*.txt"),
                ("All files", "*.*"),
            ),
        )
        if file_path:
            self.selected_file_path = file_path
            self.lbl_selected_file.configure(
                text=f"✅ {os.path.basename(file_path)}", text_color="green"
            )

    def append_log(self, text):
        self.console_textbox.configure(state="normal")
        self.console_textbox.insert("end", text)
        self.console_textbox.see("end")
        self.console_textbox.configure(state="disabled")

    def update_queue_ui(self):
        for widget in self.queue_frame.winfo_children():
            widget.destroy()

        if not self.generation_queue:
            ctk.CTkLabel(
                self.queue_frame, text=self._S("queue_empty"), text_color="gray"
            ).pack(pady=10)
            self.queue_frame.update_idletasks()  # Force UI refresh
            return

        for index, item in enumerate(self.generation_queue):
            sport, doc_path, _ = item
            frame = ctk.CTkFrame(
                self.queue_frame, fg_color=("gray85", "gray25"), corner_radius=5
            )
            frame.pack(fill="x", padx=5, pady=2)

            lbl = ctk.CTkLabel(
                frame,
                text=f"{index + 1}. {sport} - ({os.path.basename(doc_path)})",
                anchor="w",
            )
            lbl.pack(side="left", padx=10, pady=5)

            btn_remove = ctk.CTkButton(
                frame,
                text="🗑️",
                width=30,
                fg_color="#b82121",
                hover_color="#8a1717",
                command=lambda i=index: self.remove_from_queue(i),
            )
            btn_remove.pack(side="right", padx=5, pady=5)

            btn_edit = ctk.CTkButton(
                frame,
                text="✏️",
                width=30,
                command=lambda i=index: self.edit_queue_item(i),
            )
            btn_edit.pack(side="right", padx=5, pady=5)

    def remove_from_queue(self, index):
        if 0 <= index < len(self.generation_queue):
            item = self.generation_queue.pop(index)
            self.update_queue_ui()
            self.append_log(f"🗑️ {self._S('log_removed')}'{item[0]}'\n")

    def edit_queue_item(self, index):
        if 0 <= index < len(self.generation_queue):
            sport, doc_path, ai_settings = self.generation_queue.pop(index)

            self.entry_sport.delete(0, "end")
            self.entry_sport.insert(0, sport)
            self.combo_lang.set(ai_settings.get("app_language", "Italiano"))

            self.selected_file_path = doc_path
            if doc_path:
                self.lbl_selected_file.configure(
                    text=f"✅ {os.path.basename(doc_path)}", text_color="green"
                )

            self.combo_url.set(ai_settings.get(
                "raw_url", "OpenAI (Cloud Predefinito)"))
            self.entry_key.delete(0, "end")
            self.entry_key.insert(0, ai_settings.get("key", ""))
            self.combo_model.set(ai_settings.get(
                "raw_model", "gemini-2.5-pro"))
            self.combo_os.set(
                ai_settings.get("os_target", "Windows (.exe) - Predefinito")
            )

            # Restore God-Mode states
            saved_modes = ai_settings.get("module_modes", {})
            saved_contents = ai_settings.get("module_contents", {})
            for mod_id, mode_var in self._module_mode.items():
                saved_mode = saved_modes.get(mod_id, self._AI_LABEL)
                mode_var.set(saved_mode)
                self._on_module_mode_changed(mod_id)
                if saved_mode == self._MANUAL_LABEL and mod_id in saved_contents:
                    tb = self._module_textbox[mod_id]
                    tb.delete("1.0", "end")
                    tb.insert("1.0", saved_contents[mod_id])

            self.entry_temp.delete(0, "end")
            self.entry_temp.insert(0, ai_settings.get("temperature", "0.6"))

            self.entry_primary_goal.delete(0, "end")
            self.entry_primary_goal.insert(
                0, ai_settings.get("primary_goal", "weight"))

            self.update_queue_ui()
            self.append_log(f"✏️ {self._S('log_restored')}\n")

    def add_to_queue(self):
        sport_name = self.entry_sport.get().strip()

        if not sport_name:
            messagebox.showwarning(
                self._S("dialog_warning"), self._S("warn_no_sport"))
            return

        if not self.selected_file_path:
            messagebox.showwarning(
                self._S("dialog_warning"), self._S("warn_no_file"))
            return

        # --- Folder Collision Check ---
        S = STRINGS[self.lang.get()]
        # --- Mandatory App Name Check ---
        manual_app_name = self.app_name_var.get().strip()
        if not manual_app_name:
            messagebox.showwarning(
                self._S("dialog_warning"), self._S("warn_no_app_name"))
            return

        if manual_app_name:
            # Sanitize name for a reliable path check
            safe_folder = re.sub(r"[^\w\s\-]", "", manual_app_name).strip()
            safe_folder = safe_folder.replace(" ", "_")
            safe_folder = re.sub(r"_+", "_", safe_folder).strip("_")

            output_dir = os.path.join(
                BASE_DIR, "generated_output", safe_folder)
            if os.path.exists(output_dir):
                print(f"DEBUG: Folder {safe_folder} already exists. Backend will handle suffixing.")
                # We show a notice but DO NOT return, as V11 handles uniqueness in config_inject.py
                # messagebox.showinfo(S["dialog_ok_title"], S["warn_folder_exists"].format(manual_app_name) + " (Auto-renaming active)")

        url_map = {
            "OpenAI (Cloud Predefinito)": "https://api.openai.com/v1",
            "Ollama (Locale sul tuo PC)": "http://localhost:11434/v1",
            "LM Studio (Locale)": "http://localhost:1234/v1",
            "Groq (Cloud Veloce)": "https://api.groq.com/openai/v1",
            "Gemini (Google)": "https://generativelanguage.googleapis.com/v1beta/openai",
            "Anthropic (Claude)": "https://api.anthropic.com/v1",
        }

        # Mapping for the generated app's internal logic
        provider_map = {
            "OpenAI (Cloud Predefinito)": "openai",
            "Ollama (Locale sul tuo PC)": "ollama",
            "LM Studio (Locale)": "lmstudio",
            "Groq (Cloud Veloce)": "groq",
            "Gemini (Google)": "gemini",
            "Anthropic (Claude)": "anthropic",
        }

        raw_url = self.combo_url.get().strip()
        ai_url = url_map.get(raw_url, raw_url)
        ai_provider = provider_map.get(raw_url, "openai")
        raw_model = self.combo_model.get().strip()
        ai_model = raw_model if raw_model != "Inserimento Manuale..." else ""

        # Collect states and contents of all God-Mode modules
        module_modes = {mid: var.get()
                        for mid, var in self._module_mode.items()}
        module_contents = {
            mid: self._module_textbox[mid].get("1.0", "end").strip()
            for mid in self._module_mode
            if self._is_manual(mid)
        }

        ai_settings = {
            "app_name": self.app_name_var.get().strip(),
            "raw_url": raw_url,
            "url": ai_url,
            "key": self.entry_key.get().strip(),
            "raw_model": raw_model,
            "model": ai_model,
            "provider": ai_provider,
            "temperature": self.entry_temp.get().strip() or "0.6",
            "os_target": self.combo_os.get().strip(),
            "app_language": self.combo_lang.get().strip(),
            "module_modes": module_modes,
            "module_contents": module_contents,
            "primary_goal": self.entry_primary_goal.get().strip() or "weight",
            # Backward compatibility with old field (metrics)
            "progress_mode": "manual" if self._is_manual("metrics") else "auto",
            "custom_progress_html": module_contents.get("metrics", ""),
        }

        try:
            self.generation_queue.append(
                (sport_name, self.selected_file_path, ai_settings))
            self.update_queue_ui()
            self.queue_frame.update_idletasks()  # Force UI refresh for Windows

            self.entry_sport.delete(0, "end")
            self.selected_file_path = None
            self.lbl_selected_file.configure(
                text=self._S("no_file"), text_color="gray")
            self.app_name_var.set("")
            self.append_log(f"✅ Added to queue: '{sport_name}'\n")
        except Exception as e:
            messagebox.showerror(
                S.get("dialog_warning", "Error"), f"Queue Error: {e}")
            self.append_log(f"❌ ERROR in add_to_queue: {e}\n")

    def cancel_generation(self):
        if not self.is_processing:
            return

        self.is_cancelled = True
        self.generation_queue.clear()
        self.update_queue_ui()
        self.append_log(
            "\n⚠️ INTERRUPTION PROCEDURE ACTIVATED. Forced shutdown of the running process...\n"
        )

        if self.current_process:
            try:
                pid = self.current_process.pid
                if sys.platform == "win32":
                    subprocess.run(
                        ["taskkill", "/F", "/T", "/PID", str(pid)],
                        capture_output=True,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )
                else:
                    try:
                        os.killpg(os.getpgid(pid), signal.SIGTERM)
                    except ProcessLookupError:
                        pass
            except Exception as e:
                self.append_log(
                    f"\n⚠️ Error during process interruption: {e}\n"
                )

        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=5.0)

        self.btn_cancel.configure(state="disabled", text=self._S("stopping"))
        self.kill_zombies()

    def kill_zombies(self):
        """
        Radical kill of all orphan or active node/python processes
        to ensure cleanup between tasks.
        """
        self.append_log("🧹 Process cleanup in progress (Zombie Killer)...\n")
        try:
            if sys.platform == "win32":
                # Kill of all node and python processes that could block the filesystem
                # but trying to be conservative (don't kill the builder itself!)
                # In an ideal environment, we would use process groups, but taskkill /F is more brutal and decisive here.
                subprocess.run(
                    ["taskkill", "/F", "/IM", "node.exe", "/T"],
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
                # NOTE: We don't kill python.exe here because we would kill the UI itself!
                # Instead, orchestrator.py is already finished .wait(), so child python.exe should be closed.
            else:
                subprocess.run(["pkill", "-9", "node"], capture_output=True)
        except Exception as e:
            self.append_log(f"⚠️ Error during Zombie Killer: {e}\n")

    def start_generation_loop(self):
        with self._start_lock:
            if self.is_processing:
                messagebox.showinfo(
                    self._S("dialog_processing"), self._S("batch_in_progress")
                )
                return

            if not self.generation_queue:
                messagebox.showwarning(
                    self._S("queue_empty_title"), self._S("warn_queue_empty")
                )
                return

            self.is_processing = True
            self.is_cancelled = False

        self.btn_generate.configure(
            state="disabled", text=self._S("generating"))
        self.btn_cancel.configure(
            state="normal", text="\U0001f6d1 " + self._S("btn_stop")
        )
        self.btn_add_queue.configure(state="disabled")

        self.console_textbox.configure(state="normal")
        self.console_textbox.delete("1.0", "end")
        self.console_textbox.configure(state="disabled")

        self.append_log(
            "🚀 STARTING BATCH PROCESS AND COMPLEX GRAPH GENERATION (QUEUE)\n"
        )
        self.append_log("=========================================\n")

        self._worker_thread = threading.Thread(
            target=self.process_queue_worker, daemon=True
        )
        self._worker_thread.start()

    def process_queue_worker(self):
        success_count = 0
        error_count = 0

        while self.generation_queue and not self.is_cancelled:
            current_item = self.generation_queue.pop(0)
            sport_name, source_file, ai_settings = current_item

            self.after(0, self.update_queue_ui)
            self.after(
                0, self.append_log, f"\n\n🔶 Processing Start: [{sport_name}]\n"
            )
            self.after(
                0,
                self.append_log,
                f"   Base document: {os.path.basename(source_file)}\n\n",
            )

            env = os.environ.copy()
            env["SPORT_NAME"] = sport_name
            env["AI_BASE_URL"] = ai_settings["url"]
            env["AI_API_KEY"] = ai_settings["key"]
            env["AI_MODEL"] = ai_settings["model"]
            env["AI_PROVIDER"] = ai_settings.get("provider", "openai")
            env["AI_TEMPERATURE"] = ai_settings.get("temperature", "0.6")
            env["OS_TARGET"] = ai_settings.get(
                "os_target", "Windows (.exe) - Predefinito"
            )
            env["APP_LANGUAGE"] = ai_settings.get("app_language", "Italiano")
            env["PRIMARY_GOAL_KEY"] = ai_settings.get("primary_goal", "weight")
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"
            env["PYTHONUNBUFFERED"] = "1"

            # ── Bridge God-Mode → Env Var ─────────────────────────────────────
            # For each module in Manual mode, export the content as env var.
            # For modules in AI mode, remove any remains from the previous
            # session to avoid unintended overrides (security).
            module_modes = ai_settings.get("module_modes", {})
            module_contents = ai_settings.get("module_contents", {})

            for mod_id, env_key in _MODULE_ENV_MAP.items():
                mode = module_modes.get(mod_id, self._AI_LABEL)
                if mode == self._MANUAL_LABEL:
                    content = module_contents.get(mod_id, "")
                    if content:
                        env[env_key] = content
                        self.after(
                            0,
                            self.append_log,
                            f"   ✋ AI Bypass [{mod_id}]: manual content injection.\n",
                        )
                    else:
                        # Empty content → remove env var for security
                        env.pop(env_key, None)
                else:
                    # AI Mode → remove env var not to interfere with backend
                    env.pop(env_key, None)
            # ─────────────────────────────────────────────────────────────────

            try:
                os.makedirs(DATA_INPUT_DIR, exist_ok=True)
                original_filename = os.path.basename(source_file)
                dest_file = os.path.join(DATA_INPUT_DIR, original_filename)
                shutil.copy2(source_file, dest_file)
                env["INSTRUCTION_FILE"] = original_filename

                popen_kwargs = {
                    "env": env,
                    "stdout": subprocess.PIPE,
                    "stderr": subprocess.STDOUT,
                    "text": True,
                    "bufsize": 1,
                    "encoding": "utf-8",
                    "errors": "replace",
                }
                if sys.platform != "win32":
                    popen_kwargs["start_new_session"] = True

                self.current_process = subprocess.Popen(
                    [sys.executable, ORCHESTRATORE_PATH], **popen_kwargs
                )

                for line in self.current_process.stdout:
                    if self.is_cancelled:
                        break
                    self.after(0, self.append_log, line)

                self.current_process.wait()

                if self.is_cancelled:
                    self.after(
                        0,
                        self.append_log,
                        f"\n❌ Process for '{sport_name}' Forcibly Interrupted.\n",
                    )
                    break

                if self.current_process.returncode == 0:
                    self.after(
                        0,
                        self.append_log,
                        f"\n✅ APP '{sport_name}' COMPLETED SUCCESSFULLY!\n",
                    )
                    success_count += 1
                else:
                    self.after(
                        0,
                        self.append_log,
                        f"\n⚠️ HANDLED ERROR: Generation failed for '{sport_name}'.\n",
                    )
                    error_count += 1

            except Exception as e:
                self.after(
                    0,
                    self.append_log,
                    f"\n❌ UNEXPECTED EXCEPTION during '{sport_name}': {str(e)}\n",
                )
                error_count += 1
            finally:
                self.current_process = None
                self.kill_zombies()  # Cleanup at each task end

        self.is_processing = False

        if self.is_cancelled:
            self.after(
                0,
                self.append_log,
                "\n=========================================\n🛑 BATCH PROCESSING CANCELLED BY USER.\n",
            )
            self.after(
                0,
                lambda: messagebox.showwarning(
                    self._S("interrupted_title"), self._S("interrupted_msg")
                ),
            )
        else:
            self.after(
                0,
                self.append_log,
                f"\n=========================================\n🏁 BATCH PROCESSING FINISHED.\nSuccesses: {success_count} | Errors: {error_count}\n",
            )
            self.after(
                0,
                lambda: messagebox.showinfo(
                    self._S("completed_title"),
                    f"{self._S('batch_done').format(success_count, error_count)}",
                ),
            )

        self.after(
            0,
            lambda: self.btn_generate.configure(
                state="normal", text="\U0001f680 " + self._S("btn_start")
            ),
        )
        self.after(
            0,
            lambda: self.btn_cancel.configure(
                state="disabled", text="\U0001f6d1 " + self._S("btn_stop")
            ),
        )
        self.after(0, lambda: self.btn_add_queue.configure(state="normal"))
        self.after(0, self.update_queue_ui)


if __name__ == "__main__":
    try:
        app = AppBuilderUI()
        app.update_queue_ui()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nApplication closed by user.")
        sys.exit(0)
