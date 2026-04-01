APP_NAME = "Coach of Escalada Français"
SYSTEM_PROMPT = """
## RÔLE ET IDENTITÉ
Vous êtes {APP_NAME}, un entraîneur d'escalade IA d'élite, expert et spécialisé dans la discipline: Escalade Sportive et Bloc. Votre objectif est de créer des plans holistiques et hyper-personnalisés qui intègrent la préparation athlétique spécifique, l'acquisition de compétences techniques avancées et l'optimisation de la performance physique et mentale propres à ce sport.

## PRINCIPES FONDAMENTAUX
1. Spécificité Progressive et Surcharge Adaptée : Chaque stimulus d'entraînement (hangboard, circuits, voies-projets) doit avoir un transfert identifiable vers l'objectif de performance, avec une progression contrôlée ne dépassant pas 10% de charge par semaine sur les structures tendineuses.
2. Primauté de la Technique et de la Lecture : La qualité de l'exécution gestuelle et l'analyse cognitive des passages priment sur la force brute. 70% des gains chez un grimpeur intermédiaire proviennent de l'amélioration technique.
3. Gestion Intelligente de la Fatigue Tendineuse : Les structures passives (poulies A2/A4, tendons fléchisseurs) ont un temps de remodelage lent (8-12 semaines). L'entraînement intègre des fenêtres de récupération active obligatoires comme vecteur de surcompensation.
4. Personnalisation par les Données : Le plan n'est pas figé ; il est une hypothèse ajustée en temps réel via la collecte de variables objectives (cotation, RPE, douleur) et subjectives (motivation, fluidité) après chaque séance.
5. Sécurité et Durabilité : Priorité absolue à la santé des articulations (épaules, doigts) via le respect du protocole de douleur 0-1-2 et l'intégration systématique d'échauffements, de mobilisations et de protocoles de retour de blessure.

## SYSTÈME D'INTENSITÉ ET D'AUTORÉGULATION
Le système d'Évaluation de l'Effort Perçu (RPE) spécifique à l'escalade est calibré sur une échelle de 1 à 10 :
1-2 : Échauffement léger, mobilité. Aucune fatigue.
3-4 : Grimpe aisée, conversation possible. Récupération active.
5-6 : Effort modéré. Technique propre mais essais nécessaires sur mouvements nouveaux. Fatigue légère en fin de séance.
7-8 : Effort difficile. Engagement à 80-90%. Essais intensifs sur blocs ou voies à la limite. Fatigue perceptible dans les avant-bras et les doigts.
9 : Effort maximum. Engagement à 100%. Réussite ou échec sur des mouvements à la limite absolue. Fatigue importante, nécessite 48-72h de récupération.
10 : Effort maximal, non soutenable. Échec musculaire ou abandon pour cause de douleur. À éviter en entraînement régulier.
Ce RPE est croisé avec la Règle des 0-1-2 de douleur tendineuse : 0/10 autorise la force max, 1-2/10 impose un volume léger, ≥3/10 stoppe la séance.

## CADRE D'ANALYSE DES DONNÉES CLIENT
1. ÉVALUATION PHYSIQUE ET MÉTABOLIQUE : Calcul du métabolisme de base (BMR) et de la dépense énergétique totale (TDEE) pour définir une cible calorique soutenant le ratio poids/force. Évaluation du ratio charge/poids au hangboard (bord 20mm) et de la mobilité fonctionnelle des épaules et des hanches.
2. ANALYSE DU NIVEAU ET DE LA PERFORMANCE : Classification basée sur les cotations max (bloc et voie), le style de grimpe dominant (contact, isométrique, endurance), les inclinaisons préférentielles et l'identification des faiblesses gestuelles (pieds, lecture, coordination).
3. DÉFINITION DES OBJECTIFS SPÉCIFIQUES : Création d'une roadmap et d'une périodisation annuelle basée sur des objectifs concrets à 3, 6 et 12 mois (ex: "enchaîner le projet 8a de La Ramirole avant fin octobre").
4. ÉVALUATION LOGISTIQUE ET LIMITATIONS : Recensement des antécédents de blessures (poulies, épicondylite), de la disponibilité hebdomadaire, de l'accès au matériel (salle, falaise, hangboard, pan) et des contraintes de vie (stress, sommeil).

## STRUCTURE DE SORTIE HYPER-PERSONNALISÉE
SECTION 1 : STRATÉGIE NUTRITIONNELLE FONCTIONNELLE : Cible calorique et répartition des macronutriments (protéines: 1.6-2.0g/kg, glucides adaptés au volume, lipides >0.8g/kg) visant l'optimisation du ratio poids/force et la réparation tendineuse.
SECTION 2 : PROGRAMMATION À LONG TERME : Phasage mensuel détaillant les cycles successifs de force maximale (4-6 semaines), d'endurance de force (4-5 semaines), de technique (3-4 semaines) et de récupération active (1-2 semaines), alignés sur les objectifs saisonniers.
SECTION 3 : PLAN D'ENTRAÎNEMENT HEBDOMADAIRE : Séances structurées avec Échauffement (20min de mobilité dynamique et de grimpe progressive), Coeur/Technique (travail délibéré sur les faiblesses), Séance Principale (hangboard, blocs max ou circuits selon la phase), Accessoires (renforcement stabilisateurs épaules, gainage) et Retour au calme (étirements légers, auto-massage).
SECTION 4 : PROTOCOLES DE SÉCURITÉ ET DE RÉCUPÉRATION : Protocole de gestion de la douleur tendineuse (0-1-2), planning de sommeil (7-9h/nuit), stratégies d'hydratation en falaise, et exercices excentriques de récupération (finger curls, rice bucket).

## FORMAT DE SORTIE FINAL
1. RÉSUMÉ EXÉCUTIF : Synthèse du profil, des objectifs et de la philosophie du plan.
2. STRATÉGIE NUTRITIONNELLE : Recommandations détaillées en calories et macros avec exemples de repas.
3. PROGRAMMATION À LONG TERME : Calendrier des phases d'entraînement et des pics de performance.
4. PLAN D'ENTRAÎNEMENT HEBDOMADAIRE : Détail jour par jour des séances, des exercices, des séries et des répétitions.
5. PROTOCOLES DE SÉCURITÉ : Règles strictes de gestion de la douleur et procédures en cas de signal d'alerte.
6. SYSTÈME D'AUTORÉGULATION : Guide pour ajuster les séances en fonction du RPE et de la douleur ressentie.
7. MESSAGE DE MOTIVATION : Un encouragement final personnalisé, ancré dans la vision à long terme de l'athlète, signé "- {APP_NAME}".
"""

PROFILE_QUESTIONS = """
[
  {
    "key": "1_ratio_poids_force_goal",
    "section": "Objectifs de Performance",
    "title": "Ratio Poids/Force Cible",
    "question": "Quel est votre objectif de ratio poids/force (charge totale tenue / poids de corps) sur une prise de bord 20 mm pour ce cycle d'entraînement ?",
    "type": "number"
  },
  {
    "key": "2_profil_grimpe_actuel",
    "section": "Évaluation Technique Initiale",
    "title": "Profil de Grimpe Actuel",
    "question": "Décrivez en détail votre profil de grimpe actuel : cotations maximales en tête et en bloc, style dominant (contact, isométrie, endurance de force) et inclinaisons préférentielles (dalle, dévers).",
    "type": "textarea"
  },
  {
    "key": "3_faiblesses_gestuelles",
    "section": "Évaluation Technique Initiale",
    "title": "Faiblesses Gestuelles Identifiées",
    "question": "Listez et décrivez vos faiblesses gestuelles actuelles (ex: précision des pieds, recul, gestion des mouvements coordonnés, lecture des repos).",
    "type": "textarea"
  },
  {
    "key": "4_historique_blessures",
    "section": "Évaluation Physique",
    "title": "Historique des Blessures",
    "question": "Décrivez votre historique de blessures liées à l'escalade (poulies A2/A4, tendinopathies, conflits d'épaule) et les protocoles de suivi actuels.",
    "type": "textarea"
  },
  {
    "key": "5_disponibilités_entrainement",
    "section": "Logistique et Planification",
    "title": "Disponibilités Hebdomadaires",
    "question": "Détaillez votre emploi du temps hebdomadaire idéal pour l'entraînement : nombre de séances, durée, accès à une salle, à du matériel spécifique (hangboard, pan) et à la falaise.",
    "type": "textarea"
  },
  {
    "key": "6_strategie_nutrition_recuperation",
    "section": "Nutrition et Récupération",
    "title": "Stratégie Nutrition et Récup",
    "question": "Décrivez vos habitudes actuelles en matière de nutrition (apports protéiques, gestion des glucides) et de récupération (qualité du sommeil, protocoles de mobilité, gestion de l'hydratation en falaise).",
    "type": "textarea"
  },
  {
    "key": "7_preferences_materiel",
    "section": "Logistique et Planification",
    "title": "Préférences et Accès Matériel",
    "question": "Quel est votre accès à du matériel d'entraînement spécifique (type de hangboard, campus board, Kilter/Tension Board) et quelles sont vos préférences ou contraintes pour les séances ?",
    "type": "textarea"
  },
  {
    "key": "8_objectifs_temporaires",
    "section": "Objectifs de Performance",
    "title": "Objectifs à 3-6-12 Mois",
    "question": "Formulez vos objectifs concrets à 3, 6 et 12 mois (ex: enchaîner un projet de falaise spécifique, progresser en bloc, consolider un niveau). Soyez le plus précis possible.",
    "type": "textarea"
  }
]
"""

CLIENTS_PROFILE_QUESTIONS = [
    {
        "key": "1_ratio_force_poids_goal",
        "section": "Objectifs",
        "title": "Ratio Force/Poids Objectif",
        "question": "Quel est la valeur numérique précise du ratio charge totale / poids de corps que vous visez sur une prise de 20 mm au test de max hang, ce ratio étant un indicateur clé de la force spécifique pour votre objectif principal en escalade selon la méthode Vertical Intelligence ?",
        "type": "number"
    },
    {
        "key": "2_profil_grimpe_actuel",
        "section": "Évaluation Technique",
        "title": "Profil de Grimpe Actuel",
        "question": "Décrivez en détail votre profil de grimpe actuel, incluant vos cotations maximales distinctes en tête et en bloc, votre style dominant (contact, isométrie, endurance de force), vos inclinaisons de prédilection et vos principales faiblesses gestuelles identifiées (ex: précision des pieds, gestion des repos).",
        "type": "textarea"
    },
    {
        "key": "3_historique_entrainement_recent",
        "section": "Évaluation Technique",
        "title": "Historique d'Entraînement Récent",
        "question": "Décrivez votre historique d'entraînement des 3 à 6 derniers mois : structure hebdomadaire, outils utilisés (hangboard, pan, falaise), volume et intensité habituels, et précisez si vous êtes actuellement en phase de progression active ou de plateau, avec les facteurs explicatifs que vous percevez.",
        "type": "textarea"
    },
    {
        "key": "4_evaluation_force_mobilite",
        "section": "Évaluation Physique",
        "title": "Force et Mobilité",
        "question": "Évaluez votre condition physique spécifique à l'escalade : décrivez vos résultats aux tests de force (max hang, campus board si applicable), votre ratio poids/force actuel, et détaillez votre mobilité fonctionnelle au niveau des épaules (rotation, stabilité) et des hanches (ouverture, flexion).",
        "type": "textarea"
    },
    {
        "key": "5_blessures_limitations",
        "section": "Santé et Intégrité Physique",
        "title": "Blessures et Limitations",
        "question": "Listez et décrivez tout antécédent de blessure ou douleur chronique liée à l'escalade, en particulier au niveau des poulies des doigts (A2/A4), des tendons fléchisseurs, des coudes (épicondylite) ou des épaules, ainsi que toute autre limitation physique pouvant impacter l'entraînement.",
        "type": "textarea"
    },
    {
        "key": "6_disponibilite_hebdomadaire",
        "section": "Logistique et Planification",
        "title": "Disponibilité Hebdomadaire",
        "question": "Précisez votre disponibilité hebdomadaire pour l'entraînement : nombre de séances envisageables, durée typique, moments de la journée favorables, et décrivez vos accès aux infrastructures (salle de bloc/voie, falaise en extérieur, hangboard personnel, pan Gullich ou Kilter Board).",
        "type": "textarea"
    },
    {
        "key": "7_habitudes_nutrition_recuperation",
        "section": "Style de Vie",
        "title": "Nutrition et Récupération",
        "question": "Décrivez vos habitudes alimentaires actuelles (répartition des macronutriments, timing des repas), d'hydratation, de supplémentation éventuelle, ainsi que vos protocoles de récupération (qualité et quantité de sommeil, étirements, gestion du stress) et leur adéquation perçue avec votre charge d'entraînement.",
        "type": "textarea"
    },
    {
        "key": "8_preferences_entrainement",
        "section": "Préférences et Motivation",
        "title": "Préférences d'Entraînement",
        "question": "Exprimez vos préférences et aversions concernant les méthodologies d'entraînement (ex: séances très structurées vs. libres, travail technique ciblé vs. volume), le type de feedback souhaité, ainsi que votre appétence pour le travail de force pure au hangboard ou en salle de musculation.",
        "type": "textarea"
    },
    {
        "key": "9_contexte_psychologique_environnement",
        "section": "Contexte Additionnel",
        "title": "Contexte Psychologique",
        "question": "Décrivez votre état psychologique général lié à l'escalade : motivation actuelle, présence de blocages mentaux spécifiques (peur du vol, gestion de l'échec sur un projet), et impact estimé des facteurs de stress extra-sportifs (professionnel, personnel) sur votre récupération et votre performance.",
        "type": "textarea"
    },
    {
        "key": "10_suivi_auto_evaluation",
        "section": "Contexte Additionnel",
        "title": "Suivi et Auto-évaluation",
        "question": "Quelles sont vos habitudes actuelles de suivi d'entraînement (carnet, application) et comment évaluez-vous vous-même une séance typique (selon des critères comme le RPE, la douleur aux doigts, la qualité du mouvement) pour guider les ajustements de votre programme ?",
        "type": "textarea"
    }
]

PERSONALIZED_CONTEXT = """
CONFIG = {
    "PERSONALIZED_CONTEXT": \"\"\"
# DONNÉES SPÉCIFIQUES DU CLIENT - À UTILISER IMPÉRATIVEMENT
Tu établis un plan pour ${user.name}. Ci-dessous ses données actualisées.
Applique strictement ton cadre d'analyse à ces données pour générer une sortie hyper-personnalisée.
## PROFIL STATIQUE
${profileContext}
## ${dynamicDataContext}
Rappel : commence toujours ta réponse en t'adressant à ${user.name} et signe toujours par "- {APP_NAME}".
\"\"\"
}
"""

PROMPT_BUTTONS_LOGIC = """
promptBtnFull.onclick = () => handleVisualPromptClick("Crée une session d'escalade adaptative de [DURATION_min] minutes pour l'objectif: [OBJECTIVE: force_maximale/power_endurance/technique/récupération_active]. Équipement disponible: extraire du profil (ex: pan Güllich, barre à pull-up, système de poulies, prise type 20mm). Historique RPE de la semaine: [valeur]. Priorité technique de la session: [texte]. Fournis: échauffement détaillé (minutes et exercices spécifiques escalade), travail technique (exercices de lecture ou placement sur pan, séries x durée), bloc de force principale (ex: max hangs, campus board léger), travail accessoire (ex: renforcement antagonistes, gainage), timing précis pour chaque bloc, et une progression suggérée pour les 3 prochaines sessions avec ajustements de charge et de complexité.");
promptBtnTraining.onclick = () => handleVisualPromptClick("Pour la session de base décrite: [BRIEF SESSION DESCRIPTION], génère 3 variantes (Légère / Standard / Choc). Pour chaque variante, indique les changements précis de volume (nombre de voies/blocs, temps sous tension), d'intensité (% de la force max, cotation), de récupération entre les essais et blocs, et le RPE attendu. Fournis des règles de décision claires pour choisir la variante en fonction du RPE moyen de la semaine écoulée et de la qualité du sommeil (heures et perception de la récupération).");
promptBtnNutrition.onclick = () => handleVisualPromptClick("Programme 4 micro-progressions consécutives pour la [SKILL: ex: tenue sur prise 20mm en demi-fléchi] en partant d'un meilleur temps de [s] avec élastique [L/M/Ø]. Objectif: +[s] en 4 sessions. Spécifie pour chaque session: l'exercice principal (ex: repeaters, max hangs), le format série x durée/repetition, la modification de l'élastique ou de l'inclinaison du corps, le RPE cible, et des indices techniques détaillés pour une exécution parfaite (position des épaules, engagement du dos, répartition du poids, respiration).");
promptBtnPlan.onclick = () => handleVisualPromptClick("Prépare un bloc d'affûtage de [Jours: 7-10] jours pour maximiser la performance lors du test [TEST: ex: meilleure tenue sur prise 20mm +2s] avec date de test [DATE]. Inclut une phase de tapering progressive, la programmation quotidienne (intensité, volume, repos actif), une stratégie nutritionnelle détaillée pour les 48h pré-test (timing des repas, hydratation, glycogène), et un plan de récupération post-test structuré sur plusieurs jours pour prévenir les blessures et optimiser la supercompensation.");
promptBtnSkill.onclick = () => handleVisualPromptClick("Organise la séquence des tentatives pour le jour de test sur la [SKILL: ex: Tenue en lever de pied sur prise à deux doigts]: échauffement détaillé progressif (mobilité, activation, essais à intensité croissante), 5 tentatives de rampe avec temps/objectifs précis pour chacune, temps de récupération recommandé entre les tentatives (actif/passif), critères d'arrêt immédiat (douleur >2/10, dégradation technique flagrante, RPE >9), et un debrief final avec les métriques à enregistrer (temps tenu, perception de l'effort, qualité de l'exécution, douleur résiduelle).");
promptBtnWeeklyAnalysis.onclick = () => handleVisualPromptClick("Génère un protocole quotidien de prévention et mobilité de [DURATION_min] minutes pour la [ZONE: poignets/coudes/épaules], durée du plan: [7/14] jours, niveau: [débutant/intermédiaire/avancé]. Pour chaque jour, indique des exercices spécifiques (avec une progression hebdomadaire claire), les répétitions/temps de maintien, et des signaux clairs pour arrêter (douleur aiguë, sensation de pincement, perte de contrôle neuromusculaire). Adapte les exercices à la sollicitation en escalade (ex: rotations de poignet sous charge, étirements des fléchisseurs).");
promptBtnRecovery.onclick = () => handleVisualPromptClick("Crée un organigramme textuel pour la gestion de la douleur aiguë à l'[EMPLACEMENT: ex: poulie A2] avec une intensité perçue [1-10], un début [aigu/insidieux], présence de gonflement [O/N]. Fournis les étapes immédiates (arrêt total/modification de la prise), les critères pour un déload versus une consultation médicale urgente, les actions conservatrices (glace, compression, mobilisation douce), et les critères stricts pour un retour à l'entraînement (absence de douleur au repos, au touché, et lors de tests de charge légère).");
promptBtnTimeSaver.onclick = () => handleVisualPromptClick("Suggère une correction calorique et des priorités en macronutriments en partant de: poids actuel, variation de poids hebdomadaire [ex: 0.2 kg par semaine], poids cible, protéines cibles [ex: 2g par kg]. Fournis une plage d'ajustement kcal (+/-), une distribution recommandée des macros (protéines, glucides, lipides) adaptée à un grimpeur, et une checklist de paramètres à surveiller sur les 2 semaines suivantes (poids, force relative, qualité de la récupération, fringales, état des tendons).");
promptBtnMindBody.onclick = () => handleVisualPromptClick("Crée une bibliothèque de progression minimale pour l'équipement: [extraire l'équipement disponible du profil]. Pour chaque exercice clé ([ex: deadhang sur prise 20mm et traction type front lever]) fournis 5 étapes de progression et 2 régressions sécuritaires, avec des critères précis pour passer à l'étape supérieure (temps de maintien, RPE, technique) et le RPE cible pour chaque étape. Inclus des alternatives si l'équipement spécifique manque.");
promptBtnInjury.onclick = () => handleVisualPromptClick("Écris un script de préparation mentale de [DURATION_s: ex: 75] secondes pour pré-tentative sur [SKILL], intention: [calme/motivation/concentration]. Inclus: un pattern respiratoire spécifique (durée inspiration/rétention/expiration), 3 indices moteurs précis (ex: 'scapulas engagées', 'hanche serrée', 'regard sur la prise de sortie'), une phrase motivationnelle à répéter, et des instructions sur la posture physique et la préparation immédiate (balancement, prise de conscience corporelle).");
promptBtnVariation.onclick = () => handleVisualPromptClick("Génère un briefing hebdomadaire coach-athlète: inclus 1) Résumé des KPI (Poids, Masse Grasse, Stress, Sommeil, Sessions Complétées), 2) une priorité technique pour la semaine (ex: amélioration du placement de pied en dévers), 3) deux tâches pratiques (ex: réaliser 10 min de mobilité de hanches quotidienne / filmer un essai sur projet), 4) le check-in requis (jour/horaire), et 5) une note motivationnelle courte liée à l'objectif de cycle.");
promptBtnCycle.onclick = () => handleVisualPromptClick("Crée une checklist format A4 pour la session [Session spécifique à l'escalade]. Inclus: un en-tête avec date/heure, la pré-séance (repas, hydratation), l'équipement nécessaire, l'échauffement étape par étape, le travail technique, la force excentrique (ex: négatifs au campus), le gainage spécifique, le retour au calme, la revue vidéo, les KPI à noter, et les signaux d'alerte (douleur, fatigue excessive). Laisse des espaces remplissables pour les temps/notes. Formate clairement pour impression.");
promptBtnPreEvent.onclick = () => handleVisualPromptClick("Prépare 7 micro-routines mentales pour améliorer la concentration et la gestion du stress: inclus 1) pré-séance: respiration 60s + visualisation 20s du déroulé parfait, 2) pré-tentative: rituel de 90s (respiration, ancrage, cue moteur), 3) post-session: debrief journalier avec 5 questions précises. Fournis les scripts mot à mot avec des suggestions de timing et d'environnement pour chaque routine.");
promptBtnBodyComp.onclick = () => handleVisualPromptClick("Crée un plan de repas hebdomadaire pour atteindre les cibles macro. Fournis 7 jours avec des portions, les valeurs kcal/macros par repas, et une liste de courses rationalisée pour la semaine (protéines, glucides, légumes, graisses, collations). Adapte les aliments à la disponibilité française et aux besoins d'un grimpeur (densité nutritionnelle, collations pré/post entraînement).");
promptBtnChecklist.onclick = () => handleVisualPromptClick("Crée 8 modèles de messages (SMS/email) pour l'accountability: 1) rappel pré-séance, 2) check-in post-séance, 3) semaine critique (deload), 4) célébration de milestone. Maintenir un ton direct et motivant. Fournis également les heures d'envoi recommandées en fonction des habitudes typiques d'un grimpeur (ex: matin pour le rappel, soir pour le check-in).");
"""

VARIABLES_TO_EXTRACT = """
[
    {"id": "var_current_cotation", "label": "Cotation Actuelle (max bloc/voie)", "unit": "grade", "type": "string"},
    {"id": "var_rpe_seance", "label": "RPE Global de la Séance (1-10)", "unit": "note", "type": "number"},
    {"id": "var_douleur_doigts", "label": "Douleur dans les Doigts (0-10)", "unit": "note", "type": "number"},
    {"id": "var_qualite_sommeil", "label": "Qualité Moyenne du Sommeil Hebdomadaire (1-10)", "unit": "note", "type": "number"},
    {"id": "var_poids_corporel", "label": "Poids Corporel (à jeun)", "unit": "kg", "type": "number"}
]
"""
