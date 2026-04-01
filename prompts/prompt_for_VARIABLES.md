## SYSTEM SCHEMA ENFORCER (MANDATORY CONTRACT)

### [CRITICAL] NO LAZINESS RULE
- You MUST generate 3 to 5 COMPLETE variables. 
- NEVER use placeholders like `...`, `{"id": "etc..."}` or `(Insert other variables)`. 
- Every `label` must be a clear, professional term in [APP_LANGUAGE].
- Every `unit` must be a valid measurement unit.
- NEVER explain the logic or add side-talk.
- The output must be ONLY the Python code snippet starting with `VARIABLES_TO_EXTRACT = """`.

RULE: The FIRST variable in your JSON array MUST track the same metric as the FIRST profile question (which uses key "1_[PRIMARY_GOAL_KEY]_goal").
Its `id` must be: "var_current_[PRIMARY_GOAL_KEY]"
Its `label` must describe the current value of [PRIMARY_GOAL_KEY] in [APP_LANGUAGE].

This ensures the dashboard can calculate goal progress by comparing:
- Profile question 1 (target) vs Variable 1 (current value).

SOURCE CONTEXT: BASE VARIABLE TYPES (LOGIC TO BE ADAPTED)
Below is the logical framework for deducing the metrics needed for the sport. Your goal is to translate these concepts into the 3-5 tracked variables or essential metrics for [SPORT_NAME]:

1. Frequency and Volume: Metrics like km, steps, strokes, repetitions.
2. Intensity and Load: Metrics like 1RM, RPM, RPE, Heart Rate, Watts.
3. Technical Parameters: Metrics like time under tension, speed, cadence.
4. Adaptations and Fatigue: Metrics like stress, sleep hours (general but adaptable in name).

## LANGUAGE
All `label` values TASSATIVAMENTE in [APP_LANGUAGE].

## ONE-SHOT EXAMPLE (EXACT FORMAT REQUIRED)
VARIABLES_TO_EXTRACT = """
[
    {"id": "var_current_weight", "label": "Peso Attuale (kg)", "unit": "kg", "type": "number"},
    {"id": "var_fat_percentage", "label": "Percentuale Grasso (%)", "unit": "%", "type": "number"}
]
"""

NOW GENERATE THE COMPLETE VARIABLES_TO_EXTRACT FOR [SPORT_NAME] IN [APP_LANGUAGE]. NO PLACEHOLDERS. NO SIDE-TALK.
