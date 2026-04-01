CONTEXT AND OBJECTIVE
You are an expert AI System Architect in Python code generation. Your task is to generate a code snippet that defines a single variable: PROMPT_BUTTONS_LOGIC. The value of this variable will be a multi-line Python string containing JavaScript code for onclick event handlers.

The target sports domain for this execution is: [SPORT_NAME]

### [CRITICAL] NO LAZINESS RULE
- You MUST generate 100% of the content. 
- NEVER use placeholders like `...`.
- NEVER use generic summaries like "Esegui un'analisi completa" or "Genera una sessione".
- EVERY `handleVisualPromptClick` must contain a DEEP, TECHNICAL, and HYPER-DETAILED prompt (at least 50-80 words each) that translates all the parameters from the base commands below.
- NEVER explain what you are doing or add side-talk.
- The output must be ONLY the Python code snippet.

1. "Create an adaptive session of [DURATION_min] minutes for objective: [OBJECTIVE: planche/strength/skill/conditioning]. Available equipment: extrapolate from context. 1-week RPE history: [value]. Technical priority of the session: [text]. Provide: warm up (minutes and exercises), skill work (exercises+set x duration/rep), main strength, accessory work, timing for blocks, and suggested progression for the next 3 sessions."
2. "For the basic session described: [BRIEF SESSION DESCRIPTION], generate 3 variants (Light / Standard / Shock). For each variant indicate changes in volume, intensity, recoveries, and expected RPE. Provide clear decision rules for choosing the variant based on average RPE and weekly sleep."
3. "Program 4 consecutive micro-progressions for [SKILL: e.g. planche] starting from best hold [s] with band [L/M/Ø]. Objective: +[s] in 4 sessions. Specify for each session: main exercise, set x duration/rep, band or lean modification, target RPE, and technical cues for perfect execution."
4. "Prepare a peaking block of [Days: 7-10] days to maximize the test [TEST: e.g. best hold planche +2s] with test date [DATE]. Include tapering, daily programming (intensity, rest), 48h pre-test nutritional strategy, and post-test recovery plan."
5. "Organize the sequence of attempts for the test day on [SKILL: e.g. Straddle Planche]: detailed warm up, 5 ramp attempts with times/objectives, recommended recovery between attempts, criteria for stopping (pain, technique fail, RPE), and final debrief with metrics to record."
6. "Generate a daily prehab & mobility protocol of [DURATION_min] minutes for [AREA: wrists/elbows/shoulders], plan duration: [7/14] days, level: [beginner/intermediate/advanced]. For each day indicate exercises (with weekly progression), repetitions/time, and clear signals to stop."
7. "Create a textual flowchart for acute pain management at [LOCATION: e.g. wrist] with perceived intensity [1-10], onset [acute/insidious], presence of swelling [Y/N]. Provide immediate steps (stop/modify), criteria for deload vs. medical consultation, conservative actions (ice, mobility), and criteria for return to training."
8. "Suggest kcal correction and macronutrient priorities starting from: current weight, weekly weight variation [e.g. 0.2 kg per week], target weight, target protein [e.g. 2g per 1kg]. Provide kcal adjustment range (+/-), recommended macros distribution, and checklist of parameters to monitor in the following 2 weeks."
9. "Create a minimal progression library for equipment: [extract available equipment from profile]. For each key exercise ([full planche and handstand pushups]) provide 5 progression steps and 2 safe regressions, with criteria for advancing and target RPE for each step."
10. "Write a mental prep script of [DURATION_s: e.g. 75] seconds for pre-attempt on [SKILL], intent: [calm/motivation/concentration]. Include: breathing pattern (timing), 3 specific motor cues, a motivational phrase to repeat, and instructions on posture/physical preparation."
11. "Generate a weekly coach-athlete brief: include 1) KPI summary (Weight, Fat Mass, Stress, Sleep, Completed Workouts), 2) a technical priority for the week, 3) two practical tasks (e.g. mobility/nutrition/video), 4) required check-in (day/time), and 5) a short motivational note."
12. "Create an A4 checklist for the [Sport-specific Session] session. Include: header with date/time, pre-workout, equipment, warm-up step by step, skill work, eccentric strength, core, cool-down, video review, KPI, and warning signals. Leave fillable spaces for times/notes. Format clearly for printing."
13. "Prepare 7 mental micro-routines to improve focus and stress management: include 1) pre-workout 60s breathing + 20s visualization, 2) pre-attempt 90s ritual, 3) post-session debrief journaling 5 questions. Provide word-for-word scripts and timing suggestions."
14. "Create a weekly meal plan to achieve macro targets. Provide 7 days with portions, kcal/macros values per meal, and a rationalized weekly shopping list (proteins, carbohydrates, vegetables, fats, snacks)."
15. "Create 8 message templates (SMS/email) for accountability: 1) pre-workout reminder, 2) post-session check-in, 3) critical week (deload), 4) milestone celebration. Maintain a direct and motivating tone. Also provide recommended sending times."

## LANGUAGE

Write all prompt texts STRICTLY AND ONLY in [APP_LANGUAGE].

GUIDED EXECUTION PROCESS

1. Prompt Analysis: Analyze the 15 "BASE COMMANDS" provided in the source context.
2. Variable Name Mapping: Map each prompt to a JavaScript variable name from the mandatory list provided below, in sequential order.
3. Conceptual Translation for the Target Domain: Translate the PROMPT text of each of the 15 commands to make it specific STRICTLY AND ONLY for [SPORT_NAME] **and strictly in [APP_LANGUAGE]**. The translation must be deep: replace Calisthenics placeholders, exercises, and metrics with equivalents relevant to the new sport, maintaining the original intent of the command.
4. Variable Generation: Assemble the final JavaScript code within the PROMPT_BUTTONS_LOGIC Python variable.

MANDATORY JAVASCRIPT VARIABLE MAPPING (NON-NEGOTIABLE)
You must use the following list of 15 JavaScript variable names. Map the first name to the first prompt in the reference document, the second name to the second prompt, and so on until the fifteenth.
promptBtnFull.onclick
promptBtnTraining.onclick
promptBtnNutrition.onclick
promptBtnPlan.onclick
promptBtnSkill.onclick
promptBtnWeeklyAnalysis.onclick
promptBtnRecovery.onclick
promptBtnTimeSaver.onclick
promptBtnMindBody.onclick
promptBtnInjury.onclick
promptBtnVariation.onclick
promptBtnCycle.onclick
promptBtnPreEvent.onclick
promptBtnBodyComp.onclick
promptBtnChecklist.onclick

FINAL OUTPUT RULES (ABSOLUTE)

- Exclusive Output: The final output must be ONLY the Python code block. Do not include markdown blocks like ```python, explanations, comments, or any text before or after the code.
- Code Structure: The entire output must define a single Python variable called PROMPT_BUTTONS_LOGIC. The code must start with PROMPT_BUTTONS_LOGIC = """ and end with """. DO NOT include CONFIG = { ... } or other structures.
- Variable Value: The value must be a single multi-line Python string.
- String Content (JavaScript Code):
  - The code must contain exactly 15 lines of onclick assignments.
  - Each line must use one of the variables from the "MANDATORY MAPPING" section, in exact sequential order.
  - The variable.onclick = () => handleVisualPromptClick("..."); structure must be preserved.
  - The only part to modify is the text within the quotes of handleVisualPromptClick(), **which must be STRICTLY AND ONLY in [APP_LANGUAGE]**.

## ONE-SHOT EXAMPLE (EXACT FORMAT REQUIRED)
PROMPT_BUTTONS_LOGIC = """
promptBtnFull.onclick = () => handleVisualPromptClick("Crea una sessione adattiva di [DURATION_min] minuti specifica per [SPORT_NAME] con focus su [OBJECTIVE]. Considera l'attrezzatura disponibile nel profilo, lo storico RPE dell'ultima settimana e la priorità tecnica. Fornisci: riscaldamento dettagliato, lavoro tecnico su [SKILL], forza principale, complementari e progressione suggerita per le prossime 3 sessioni.");
...
"""

NOW GENERATE ALL 15 BUTTONS FOR [SPORT_NAME] IN [APP_LANGUAGE]. BE EXTREMELY VERBOSE AND DETAILED. NO ELLIPSES.

Now, generate the code snippet for the STRICTLY AND ONLY sport [SPORT_NAME] in STRICTLY AND ONLY IN [APP_LANGUAGE].
sport [NOME_DELLO_SPORT].
.
