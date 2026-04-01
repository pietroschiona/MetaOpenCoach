APP_NAME = "Coach Of Powerlifting English"
SYSTEM_PROMPT = """
## ROLE AND IDENTITY
You are {APP_NAME}, an elite AI Powerlifting Coach, expert and specialized in the IPF-competitive sport of powerlifting. Your goal is to create holistic and hyper-personalized strength programs that integrate competition-specific preparation, mastery of the squat, bench press, and deadlift under IPF technical rules, and the optimization of neurological and structural performance for maximal total expression.

## FUNDAMENTAL PRINCIPLES
1. Specificity and Progressive Overload: Every training decision must enhance proficiency in the competition lifts. Strength is built through the systematic, long-term management of load, volume, and intensity, prioritizing submaximal accumulation over constant maximal testing.
2. Technical Mastery and Rule Adherence: Movement quality is non-negotiable. Coaching must enforce IPF technical standards for depth, pause, and lockout, ingraining patterns that guarantee white lights on the platform.
3. Fatigue Management as a Priority: Accumulated fatigue masks true strength. Intelligent programming requires planned deloads, autoregulation, and lifestyle monitoring to ensure the athlete arrives at the platform fresh and potentiated.
4. Individualization and Athlete Context: Programming is built from a comprehensive assessment of an athlete's strength baseline, injury history, anthropometry, and life stressors. No generic template supersedes individual need.
5. Long-Term Athletic Development: Coaching decisions must prioritize the athlete's health and longevity in the sport, avoiding practices that compromise joint integrity or sustainable progress for short-term gains.

## INTENSITY AND AUTOREGULATION SYSTEM
The primary intensity metric is the Rate of Perceived Exertion (RPE) on a scale of 1-10, specifically adapted for heavy, low-rep powerlifting sets.
- RPE 10: Maximum effort, no reps left in reserve. A true competition max.
- RPE 9: One rep left in reserve. Challenging but executed with perfect technique.
- RPE 8: Two reps left in reserve. A weight that moves with speed and authority.
- RPE 7: Three reps left in reserve. Moderate effort, used for volume accumulation.
- RPE 6 or below: Light effort, for warm-ups, technique drills, and active recovery.
Autoregulation is applied by prescribing target RPEs for top sets. Athletes adjust the load based on daily readiness to hit the prescribed RPE, ensuring training stimulus matches recovery capacity. Deviations of more than 1.5 RPE from the prescription trigger program adjustments.

## CLIENT DATA ANALYSIS FRAMEWORK
1. STRENGTH AND PERFORMANCE BASELINE: Estimation of 1RMs for squat, bench press, and deadlift via submaximal testing or last competition total. Calculation of IPF GL Points and DOTS score to establish a performance metric independent of weight class. Classification as Novice (<2 years training, no meets), Intermediate (2-5 years, 1-5 meets), or Advanced (5+ years, national-level).
2. MOVEMENT AND BIOMECHANICAL SCREENING: Assessment of competition lift mechanics: squat depth and stance, bench press arch and touch point, deadlift hip hinge and stance selection. Evaluation of joint mobility (ankle dorsiflexion, shoulder rotation, thoracic extension) and identification of compensatory patterns.
3. GOAL AND COMPETITION LOGISTICS: Definition of target meet date, desired weight class, and total goal. Analysis of training schedule, equipment access (belt, sleeves, rack), and time per session.
4. HEALTH AND RECOVERY AUDIT: Detailed injury history and current pain status. Assessment of sleep duration/quality, occupation, nutritional habits, and stress levels. This determines starting volume, exercise selection, and recovery protocol emphasis.

## HYPER-PERSONALIZED OUTPUT STRUCTURE
SECTION 1: PERFORMANCE NUTRITION STRATEGY: Calorie target (maintenance, slight surplus, or controlled deficit for weight class) and macronutrient breakdown (2.0-2.4g/kg protein, 4-6g/kg carbohydrates during high volume, 1.0-1.2g/kg fats). Weight-cut and rehydration protocol if required for meet.
SECTION 2: MACROCYCLE AND PERIODIZATION ROADMAP: A 12-16 week block periodization plan detailing Accumulation (volume focus), Intensification (load focus), and Peaking (competition specificity) phases. Includes weekly set/rep/intensity ranges and planned deload weeks.
SECTION 3: WEEKLY TRAINING PLAN: Detailed sessions including: Dynamic Warm-up and Mobility Drills; Core Competition Lift Work (prescribed by percentage and RPE); Supplemental Strength Work (e.g., paused variations, close-grip bench); Accessory & Prehab Work (targeting weak points); Cool-down and Mobility.
SECTION 4: RECOVERY AND INJURY PREVENTION PROTOCOLS: Sleep hygiene mandates, deload scheduling, stress management techniques, and pain response protocols (including immediate exercise modification for sharp pain).

## FINAL OUTPUT FORMAT
1. EXECUTIVE SUMMARY: A concise overview of the athlete's profile, primary goals, and the core philosophy of the prescribed plan.
2. PERFORMANCE NUTRITION STRATEGY: Detailed caloric and macronutrient targets, meal timing recommendations, and weight management strategy.
3. LONG-TERM PROGRAMMING: The full macrocycle roadmap with phase objectives, weekly intensity targets, and key performance indicators.
4. WEEKLY TRAINING PLAN: A complete, day-by-day training schedule for the upcoming week with exercises, sets, reps, RPE, and rest periods.
5. SAFETY PROTOCOLS: Clear guidelines on technique standards, pain differentiation (good pain vs. bad pain), and steps to take in case of injury or excessive fatigue.
6. AUTOREGULATION SYSTEM: Instructions on how to use the RPE scale, how to adjust loads daily, and how to report feedback for weekly programming adjustments.
7. MOTIVATIONAL MESSAGE: A final personalized encouragement that reinforces process over outcome, signed "- {APP_NAME}".
"""

PROFILE_QUESTIONS = """
[
  {
    "key": "1_ipf_gl_points_goal",
    "section": "Competition Goals",
    "title": "Target IPF GL Points",
    "question": "What is your target IPF GL Points score for your next competition? This is your primary long-term progress metric for cross-weight class comparison.",
    "type": "number"
  },
  {
    "key": "2_training_history_analysis",
    "section": "Training Background",
    "title": "Training History & Programming",
    "question": "Describe your detailed training history. Include years of structured barbell training, prior programming exposure (linear, DUP, conjugate), average training days per week, and any significant detraining periods.",
    "type": "textarea"
  },
  {
    "key": "3_competition_history_mechanics",
    "section": "Competition Background",
    "title": "Competition History & Technique",
    "question": "Detail your competition history: meets competed, results, equipment used (belt, sleeves, wraps), federations, and best competition total. Describe your current technique execution for the squat, bench, and deadlift under IPF rules, including any known bar path tendencies or compensatory patterns.",
    "type": "textarea"
  },
  {
    "key": "4_strength_baseline_assessment",
    "section": "Performance Metrics",
    "title": "Current Strength Baseline",
    "question": "Describe your current estimated or tested 1RM for the squat, bench press, and deadlift. If available, provide your last verified competition total and body weight. Note any significant technical limitations observed during recent submaximal or maximal attempts.",
    "type": "textarea"
  },
  {
    "key": "5_injury_history_limitations",
    "section": "Medical & Injury Background",
    "title": "Injury History & Limitations",
    "question": "List all prior musculoskeletal injuries relevant to powerlifting (shoulders, elbows, lower back, hips, knees). Include onset mechanism, treatment received, and current status. Note any active pain, joint discomfort, or movement restrictions during the squat, bench, or deadlift.",
    "type": "textarea"
  },
  {
    "key": "6_weekly_schedule_availability",
    "section": "Lifestyle & Logistics",
    "title": "Weekly Schedule & Availability",
    "question": "Detail your weekly schedule and availability for training sessions. Include your occupation (sedentary vs. physical), number of days you can commit to training, and preferred training times. Specify any time constraints per session.",
    "type": "textarea"
  },
  {
    "key": "7_nutrition_recovery_habits",
    "section": "Nutrition & Recovery",
    "title": "Nutrition & Recovery Habits",
    "question": "Describe your current nutrition and recovery habits. Include details on sleep duration and consistency, general dietary habits, protein intake, and access to recovery modalities (massage, physiotherapy, sauna). Note any history with weight class management or planned cuts.",
    "type": "textarea"
  },
  {
    "key": "8_training_preferences_equipment",
    "section": "Training Environment",
    "title": "Training Preferences & Equipment",
    "question": "Describe your training preferences and equipment access. Specify your available gym equipment (power rack, calibrated plates, specialty bars), preferred training split, and any strong preferences regarding exercise selection or training intensity methods.",
    "type": "textarea"
  },
  {
    "key": "9_psychological_approach_competition",
    "section": "Mental Preparation",
    "title": "Psychological Approach & Competition",
    "question": "Describe your mental approach to training and competition. How do you typically handle missed lifts in training, competitive anxiety, and pre-competition preparation? What is your historical attempt selection strategy?",
    "type": "textarea"
  },
  {
    "key": "10_long_term_development_focus",
    "section": "Long-Term Planning",
    "title": "Long-Term Development Focus",
    "question": "Beyond your immediate IPF GL Points goal, what are your long-term development priorities? Identify the primary technical weaknesses or strength gaps (e.g., squat depth, bench press off chest, deadlift lockout) you want to address in the next macrocycle.",
    "type": "textarea"
  }
]
"""

CLIENTS_PROFILE_QUESTIONS = [
    {
        "key": "1_ipf_gl_points_goal",
        "section": "Primary Goals",
        "title": "IPF GL Points Target",
        "question": "What is the exact numeric target value for your IPF GL Points score, the primary long-term progress metric that accounts for body weight and total, which you aim to achieve by the conclusion of your next competitive macrocycle?",
        "type": "number"
    },
    {
        "key": "2_training_history",
        "section": "Performance Background",
        "title": "Training History Analysis",
        "question": "Detail your complete training history including years of structured barbell training, prior programming exposure (e.g., linear, DUP, conjugate), average training days per week, and any significant periods of detraining or inactivity that would impact your current baseline.",
        "type": "textarea"
    },
    {
        "key": "3_current_performance",
        "section": "Performance Background",
        "title": "Current Performance Level",
        "question": "Provide your most recent sanctioned meet total or submaximal assessment estimates for the squat, bench press, and deadlift, including the date, equipment used (belt/sleeves/wraps), and the calculated IPF GL Points or DOTS score from that performance.",
        "type": "textarea"
    },
    {
        "key": "4_technical_assessment",
        "section": "Performance Background",
        "title": "Technical Skill Assessment",
        "question": "Describe your current technical execution of the competition lifts, including any known movement compensations, bar path tendencies, and specific strengths or weaknesses identified in previous screenings for squat depth, bench press arch stability, or deadlift hip hinge mechanics.",
        "type": "textarea"
    },
    {
        "key": "5_injuries_limitations",
        "section": "Physical Data",
        "title": "Injury History & Limitations",
        "question": "List all prior musculoskeletal injuries, particularly to hips, shoulders, knees, elbows, and spine, detailing onset mechanism, treatment received, current status, and any active pain or range-of-motion limitations during the squat, bench press, or deadlift movements.",
        "type": "textarea"
    },
    {
        "key": "6_weekly_availability",
        "section": "Logistics & Lifestyle",
        "title": "Weekly Training Schedule",
        "question": "Outline your typical weekly availability for training sessions, including preferred number of days, session duration, time of day, and any fixed constraints such as work hours, family commitments, or travel that could impact training consistency and recovery timing.",
        "type": "textarea"
    },
    {
        "key": "7_nutrition_recovery",
        "section": "Logistics & Lifestyle",
        "title": "Nutrition & Recovery Habits",
        "question": "Describe your current dietary habits, including approximate macronutrient intake, meal timing, any restrictions or preferences, supplementation use, and your typical sleep duration, quality, and access to other recovery modalities like massage or sauna.",
        "type": "textarea"
    },
    {
        "key": "8_training_preferences",
        "section": "Training Preferences",
        "title": "Training Methodologies & Access",
        "question": "Explain your preferences regarding training methodologies, session structure, favorite accessory movements, access to gym equipment (e.g., full power rack, specialty bars, calibrated plates), and any strong aversions to specific exercises or weekly frequencies.",
        "type": "textarea"
    },
    {
        "key": "9_competition_strategy",
        "section": "Additional Context",
        "title": "Competition Goals & Strategy",
        "question": "State your target competition date, desired IPF weight class, and your strategic philosophy for attempt selection, including how you determine openers and handle in-meet adjustments based on real-time performance and energy levels on the platform.",
        "type": "textarea"
    },
    {
        "key": "10_psychological_factors",
        "section": "Additional Context",
        "title": "Psychological Performance Factors",
        "question": "Discuss how you typically handle missed lifts in training, manage pre-competition anxiety, and conduct post-meet debriefs to identify technical, strategic, and psychological areas for improvement as part of your long-term development as a competitive powerlifter.",
        "type": "textarea"
    }
]

PERSONALIZED_CONTEXT = """
CONFIG = {
    "PERSONALIZED_CONTEXT": \"\"\"# SPECIFIC CLIENT DATA - ALWAYS TO BE USED
You are creating a plan for ${user.name}. Below is their data.
Strictly apply your analysis framework to this data to generate the hyper-personalized output.
## STATIC PROFILE
${profileContext}
## ${dynamicDataContext}
Remember to start your response by addressing ${user.name} and always sign with "- {APP_NAME}".\"\"\"
}
"""

PROMPT_BUTTONS_LOGIC = """
promptBtnFull.onclick = () => handleVisualPromptClick("Create an adaptive powerlifting session of [DURATION_min] minutes tailored for an IPF competitor. Primary objective: [OBJECTIVE: max strength/technical skill/peaking/conditioning]. Available equipment: extrapolate from the athlete's profile (e.g., power rack, calibrated plates, bench, bands, chains). Consider the 1-week RPE history: [value]. Technical priority for this session: [text, e.g., improving squat depth consistency]. Provide a comprehensive plan including: specific warm-up (exercises, reps, and minutes), technique skill work (e.g., pause squats for sets x reps), main strength work (exercise, percentage/RPE, sets, reps), accessory hypertrophy work (exercises, sets, reps), strict timing for each block (e.g., 15min warm-up, 30min main lift), and a clear suggested progression for the next 3 sessions based on today's performance and RPE targets.");
promptBtnTraining.onclick = () => handleVisualPromptClick("For the described powerlifting training session: [BRIEF SESSION DESCRIPTION, e.g., heavy squat day with 5x5 @80%], generate 3 distinct variants (Light / Standard / Shock) for an IPF athlete. For each variant, explicitly detail changes in volume (total sets and reps), intensity (percentage of 1RM or RPE target), inter-set recovery times (in seconds/minutes), and the expected post-set RPE (Rate of Perceived Exertion) for the main lifts. Provide clear, data-driven decision rules for the coach to choose the variant based on the athlete's average RPE from the previous microcycle and their reported weekly sleep quality and duration, linking specific sleep scores to intensity modifications.");
promptBtnSkill.onclick = () => handleVisualPromptClick("Program 4 consecutive micro-progression sessions for the powerlifting skill: [SKILL: e.g., competition pause bench press], starting from a current best of [weight]kg for [reps] or a [s] second hold. Objective: increase by [+weight]kg or [+reps] reps in 4 sessions. Specify for each session: main exercise (e.g., Spoto press, 2-count pause bench), set x rep scheme (e.g., 4x4), specific modification (e.g., using [L/M/Ø] bands for accommodating resistance, or altering bench grip width in cm), target RPE for the top set (6-9.5), and 3 technical execution cues for perfect form (e.g., 'drive traps into bench', 'pull bar apart', 'controlled touch on sternum').");
promptBtnPlan.onclick = () => handleVisualPromptClick("Prepare a detailed peaking block of [Days: 7-10] days to maximize performance for an IPF powerlifting meet or 1RM test on [TEST: e.g., Squat 1RM], with the competition date on [DATE]. Include a precise tapering protocol: daily programming outlining exercise selection (competition lifts only or minimal variations), intensity (%1RM progression from 85% down to 90%+), volume (set/rep reduction), and rest days. Detail a 48-hour pre-test nutritional strategy focusing on carbohydrate loading, sodium and water manipulation, and meal timing. Also, provide a structured post-test recovery plan for the 72 hours following the meet, including nutrition, hydration, active recovery, and a deload week structure.");
promptBtnPreEvent.onclick = () => handleVisualPromptClick("Organize the complete attempt sequence for an IPF powerlifting meet day for the [LIFT: e.g., Squat]. Provide a minute-by-minute detailed warm-up protocol (exercises, reps, jumps to opener). Outline 5 specific ramp attempts (including weights as percentages of projected max, e.g., 50%x5, 70%x3, 80%x2, 90%x1, 95%x1) with objective for each (e.g., 'activate CNS', 'groove technique'). Specify recommended recovery time between attempts (e.g., 5-8 minutes), and clear criteria for stopping the warm-up or changing attempt selections (based on acute pain location, technique failure like excessive forward lean, or RPE exceeding 9). Conclude with a final debrief framework listing metrics to record (e.g., bar speed, perceived stability, commands followed).");
promptBtnBodyComp.onclick = () => handleVisualPromptClick("Generate a daily prehab & mobility protocol of [DURATION_min] minutes for the [AREA: e.g., shoulders/lower back/hips] critical for powerlifting, to be followed for [7/14] consecutive days, designed for a [beginner/intermediate/advanced] level athlete. For each day, list specific exercises (e.g., banded pull-aparts, cat-cow, 90/90 hip rotations) with a clear weekly progression in load, time under tension, or range of motion. Specify exact repetitions or hold times for each exercise. Include clear, objective signals to stop an exercise immediately (e.g., sharp pain, numbness, or compensatory movement patterns) and guidelines for overall session termination.");
promptBtnInjury.onclick = () => handleVisualPromptClick("Create a detailed textual flowchart for acute pain management in a powerlifter at [LOCATION: e.g., anterior shoulder] with a perceived intensity of [1-10], onset [acute/insidious], and presence of swelling [Y/N]. Provide immediate on-site steps (stop the lift, modify movement, apply compression). Establish criteria for a training deload (e.g., pain <3, no swelling) versus requiring immediate medical consultation (e.g., pain >7, clicking, instability). List conservative actions (e.g., ice application protocol, pain-free mobility exercises like scapular circles). Define strict, objective criteria for a phased return to training (e.g., pain-free full range of motion, strength symmetry >90%, ability to perform a light bench press with empty bar without symptoms).");
promptBtnNutrition.onclick = () => handleVisualPromptClick("Suggest precise kcal correction and macronutrient priorities for a powerlifter. Starting data: current weight [kg], weekly weight variation [e.g., +0.5 kg per week], target weight for meet [kg], target protein intake [e.g., 2.2g per kg]. Provide a calculated kcal adjustment range (e.g., +/- 200-400 kcal from current intake). Recommend a detailed macronutrient distribution (grams and percentages for protein, carbohydrates, fats) aligned with the training phase (accumulation vs. peaking). Supply a checklist of parameters to monitor closely over the following 2 weeks: daily morning weight, sleep quality, session RPE, hunger levels, and waist circumference to assess efficacy and adjust.");
promptBtnVariation.onclick = () => handleVisualPromptClick("Create a minimal exercise progression library for a powerlifter with the following available equipment: [extract available equipment from profile, e.g., barbell, rack, bench, bands, chains]. For each key competition lift variation ([e.g., Low Bar Squat and Competition Bench Press]), provide 5 distinct progression steps (e.g., Box Squat, Tempo Squat, Paused Squat, Competition Squat, Squat with Chains) and 2 safe regressions (e.g., Goblet Squat, Safety Bar Squat). For each step and regression, specify clear criteria for advancing (e.g., 'achieve 3x5 @8 RPE with perfect depth'), the target RPE range for working sets, and the primary technical focus point.");
promptBtnMindBody.onclick = () => handleVisualPromptClick("Write a verbatim mental preparation script of [DURATION_s: e.g., 75] seconds for a powerlifter immediately before a maximal attempt on the [LIFT: e.g., Deadlift], with the primary intent of [calm/motivation/concentration]. Include: a specific breathing pattern with exact timing (e.g., 4-second inhale, 2-second hold, 6-second exhale for 3 cycles), 3 lift-specific motor cues (e.g., 'lats tight', 'push floor away', 'chest proud'), a short, powerful motivational phrase to repeat internally, and concrete instructions on final posture and physical preparation (e.g., 'set feet at hip-width', 'grip the bar until knuckles are white', 'take a big belly breath and brace').");
promptBtnWeeklyAnalysis.onclick = () => handleVisualPromptClick("Generate a structured weekly coach-athlete brief for an IPF powerlifter. Include: 1) KPI summary table (Body Weight, Fat Mass estimate, Stress Level 1-10, Average Sleep Hours/Quality, Completed Workouts vs. Planned). 2) One technical priority for the upcoming week (e.g., 'Improve deadlift lockout speed'). 3) Two practical, actionable tasks (e.g., 'Perform 3 sets of banded face pulls post-training' and 'Record and send a side-view video of your squat opener'). 4) Required check-in schedule (Day and Time, e.g., 'Wednesday, 7 PM via voice note'). 5) A short, personalized motivational note referencing the athlete's long-term goal of qualifying for Nationals.");
promptBtnChecklist.onclick = () => handleVisualPromptClick("Create a printable A4 checklist for a [Sport-specific Session: e.g., Intensification Phase Deadlift Day] powerlifting session. Include a header with fields for Date/Time/Athlete Name. Sections must cover: Pre-workout nutrition/hydration log, Equipment checklist (belt, wrist wraps, chalk, notebook), Step-by-step warm-up (with fillable spaces for weights/reps), Skill work (e.g., deficit deadlifts, with sets/reps/RPE fields), Main Eccentric Strength work (e.g., paused deadlifts), Accessory/Core work, Cool-down/mobility exercises, Video review notes (cues to check), Session KPI (Avg. RPE, Tonnage), and Warning signals (pain location, excessive fatigue). Format clearly with checkboxes and lines for notes.");
promptBtnRecovery.onclick = () => handleVisualPromptClick("Prepare 7 distinct mental micro-routines to improve focus and manage pre-competitive stress for a powerlifter. Include: 1) A pre-workout 60-second breathing exercise (box breathing) followed by a 20-second visualization of a technically perfect lift. 2) A pre-attempt 90-second ritual combining tactical breathing, proprioceptive cues (e.g., tapping the thigh three times), and a performance keyword. 3) A post-session debrief journaling template with 5 specific questions (e.g., 'What was the RPE discrepancy between planned and actual?', 'Where did technique break down on the hardest set?'). Provide word-for-word scripts for each routine and precise timing suggestions for integration into the training week.");
promptBtnTimeSaver.onclick = () => handleVisualPromptClick("Create a detailed weekly meal plan for a powerlifter designed to achieve the following daily macro targets: Protein [g], Carbs [g], Fats [g], totaling [kcal] kcal. Provide 7 individual days, each listing meals (Breakfast, Lunch, Pre-Workout, Post-Workout, Dinner) with specific food portions in grams/cups, calculated kcal and macros per meal, and a running daily total. Generate a rationalized, non-redundant weekly shopping list categorized into: Proteins (chicken breast, lean beef, eggs, whey), Carbohydrates (jasmine rice, oats, sweet potatoes), Vegetables (broccoli, spinach, bell peppers), Fats (avocado, olive oil, nuts), and Snacks (Greek yogurt, berries).");
promptBtnCycle.onclick = () => handleVisualPromptClick("Create 8 direct and motivating message templates (for SMS/email) for coach-athlete accountability in powerlifting. Templates: 1) Pre-workout reminder (sent 90 minutes prior). 2) Post-session check-in (prompting for RPE, notes). 3) Critical week notification (e.g., deload or peak week). 4) Milestone celebration (new 1RM or qualifying total). 5) Mid-week motivation boost. 6) Weekly planning prompt. 7) Nutrition adherence check. 8) Recovery protocol reminder. For each template, maintain a concise, professional, and supportive tone. Also, provide a recommended sending day/time for each message type relative to the athlete's training schedule and time zone.");
"""

VARIABLES_TO_EXTRACT = """
[
    {"id": "var_current_total", "label": "Current Competition Total", "unit": "kg", "type": "number"},
    {"id": "var_body_weight", "label": "Daily Body Weight", "unit": "kg", "type": "number"},
    {"id": "var_session_rpe", "label": "Top Set RPE", "unit": "RPE (1-10)", "type": "number"},
    {"id": "var_sleep_quality", "label": "Sleep Quality Score", "unit": "score (1-10)", "type": "number"},
    {"id": "var_stress_level", "label": "Perceived Stress Level", "unit": "score (1-10)", "type": "number"}
]
"""
