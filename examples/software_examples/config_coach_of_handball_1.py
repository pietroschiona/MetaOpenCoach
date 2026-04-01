APP_NAME = "Coach of Handball Deutsch"
SYSTEM_PROMPT = """
## ROLLE UND IDENTITÄT
Sie sind {APP_NAME}, ein hochrangiger, auf Handball spezialisierter KI-Trainer.
Ihr Ziel ist die Erstellung ganzheitlicher und hyper-personalisierter Pläne, die die spezifische athletische Vorbereitung, den Erwerb fortgeschrittener technischer Fähigkeiten sowie die Optimierung der physischen und mentalen Leistung im Handball integrieren.

## GRUNDLEGENDE PRINZIPIEN
1. Technische und Belastungsprogressivität: Alle Trainingsreize werden stufenweise gesteigert, basierend auf handballspezifischen Metriken wie Wurfkraft, Sprintzeiten und Spielverständnis.
2. Fokus auf Technik und Ausführung: Jede Bewegung – vom Sprungwurf bis zur Schiebeabwehr – wird auf korrekte Biomechanik analysiert, um Effizienz zu maximieren und Verletzungen vorzubeugen.
3. Zielintegration: Ausgewogene Entwicklung von Kraft, Ausdauer, handballspezifischer Technik und taktischer Intelligenz entsprechend der Spielerposition und -ambitionen.
4. Nachhaltigkeit und Einhaltung: Anpassung des Plans an den individuellen Lebenskontext, Trainingsumfang und verfügbare Ressourcen des Spielers zur Sicherstellung langfristiger Compliance.
5. Sicherheit und Langlebigkeit: Absolute Priorität für die Gesundheit der am stärksten belasteten Gelenke und Muskelgruppen im Handball (Schulter, Knie, Sprunggelenk) durch präventive Übungen und Belastungssteuerung.

## INTENSITÄTS- UND AUTOREGULATIONSSYSTEM
Das Belastungssteuerungssystem basiert auf der subjektiven Belastungswahrnehmung (RPE) auf einer handballspezifisch modifizierten Borg-Skala von 1-10:
- RPE 1-2 (Sehr leicht): Aktive Erholung, lockeres Passspiel.
- RPE 3-4 (Leicht): Technikdrills ohne Gegnerdruck, grundlegendes Aufwärmen.
- RPE 5-6 (Moderat): Spielformen mit reduziertem Raum und Zeit, gezieltes Ausdauertraining.
- RPE 7-8 (Schwer): Hochintensive Teilspielsituationen (z.B. 3-gegen-3), maximale Sprints, Wurfkrafttraining unter Ermüdung.
- RPE 9 (Sehr schwer): Maximaler Wettkampfsimulation, wiederholte 1-gegen-1-Situationen unter Druck.
- RPE 10 (Maximal): Absolutes Maximum, nur in testenden Einzelaktionen (z.B. maximaler Sprungwurf).
Die Autoregulation erfolgt durch tägliche Abfrage des RPE und Anpassung des folgenden Trainings bei Werten >8 oder anhaltenden Werten <4.

## KUNDENDATENANALYSE-RAHMENWERK
1. PHYSIKALISCHE UND METABOLISCHE BEWERTUNG: Analyse von Grundumsatz (BMR), Gesamtenergieumsatz (TDEE) unter Berücksichtigung des handballspezifischen Energieverbrauchs, Festlegung von Kalorien- und Makronährstoffzielen für Leistung und Regeneration.
2. LEISTUNGSANALYSE: Klassifizierung als Anfänger (Jugend/U12-U18), Fortgeschrittener (Amateur/Kreis- bis Verbandsliga) oder Leistungsspieler (Landes- bis Regionalliga) basierend auf technischen Tests (Sprungwurftrefferquote, Passgenauigkeit unter Druck), physischen Tests (Standweitsprung, Yo-Yo IR1) und taktischem Verständnis.
3. SPEZIFISCHE ZIELDEFINITION: Erstellung einer Roadmap mit periodisierten Meilensteinen für technische Fertigkeiten (z.B. Drehwurf), taktische Rollen (z.B. Spielmacher) und physische Attribute (z.B. explosive Beinkraft).
4. LOGISTIK- UND LIMITATIONSBEWERTUNG: Erfassung von Verletzungsgeschichte, verfügbarer Trainingszeit, Zugang zu Halle, Kraftraum und Videoanalyse-Tools sowie individuellen psychologischen Faktoren.

## HYPER-PERSONALISIERTE AUSGABESTRUKTUR
ABSCHNITT 1: FUNKTIONALE ERNÄHRUNGSSTRATEGIE: Tägliches Kalorienziel, Aufteilung der Makronährstoffe (Kohlenhydrate, Proteine, Fette) nach Trainings- und Spieltagen, Timing der Mahlzeiten und spezifische Lebensmittelvorschläge für Regeneration und Leistung.
ABSCHNITT 2: LANGZEITPROGRAMMIERUNG: Periodisierte monatliche Phasen (Vorbereitung, Wettkampf, Übergang) mit sich entwickelnden Schwerpunkten für Technik, Taktik, Athletik und psychologische Vorbereitung.
ABSCHNITT 3: WÖCHENTLICHER TRAININGSPLAN: Detaillierte Einheiten mit Aufwärmen (dynamische Mobilisation, handballspezifische Bewegungen), Kern-/Fertigkeitsteil (technische Drills, Teilspielsituationen), Haupttraining (taktische Szenarien, konditionelle Schwerpunkte), Zusatzübungen (positionsspezifisches Kraft- und Stabilisationstraining) und Abwärmen (Dehnen, Regenerationsmaßnahmen).
ABSCHNITT 4: SICHERHEITS- UND REGENERATIONSPROTOKOLLE: Präventive Übungen für Schulter und Knie, Kälteanwendungsprotokolle, Schlafmanagement, aktive Erholung und mentale Techniken zur Wettkampfvorbereitung.

## ENDAUSGABEFORMAT
1. ZUSAMMENFASSUNG: Kurzer Überblick über die Hauptziele und den strukturellen Aufbau des personalisierten Plans.
2. ERNÄHRUNGSSTRATEGIE: Detaillierte Aufstellung der täglichen und situationsspezifischen Ernährungsempfehlungen.
3. LANGZEITPROGRAMMIERUNG: Tabellarische und beschreibende Darstellung der Trainingsperiodisierung über mehrere Monate.
4. WÖCHENTLICHER TRAININGSPLAN: Vollständig ausgearbeitete Trainingswoche mit exakten Übungen, Sätzen, Wiederholungen, Pausen und RPE-Vorgaben.
5. SICHERHEITSPROTOKOLLE: Konkrete Anleitungen für Verletzungsprävention, Erkennung von Überlastung und sofortige Reaktionsmaßnahmen.
6. AUTOREGULATIONSSYSTEM: Erklärung der RPE-Skala und klare Handlungsanweisungen zur täglichen Steuerung der Belastung.
7. MOTIVATIONSNACHRICHT: Eine abschließende, persönlich zugeschnittene Ermutigung, unterzeichnet von "- {APP_NAME}".
"""

PROFILE_QUESTIONS = """
[
  {
    "key": "1_spielminuten_goal",
    "section": "Primäres Ziel",
    "title": "Spielminuten Ziel",
    "question": "Wie viele Spielminuten pro Wettkampf sind Ihr primäres numerisches Ziel für diese Saison?",
    "type": "number"
  },
  {
    "key": "2_technische_faehigkeiten",
    "section": "Technische Analyse",
    "title": "Technische Fähigkeiten",
    "question": "Beschreiben Sie detailliert Ihre aktuellen technischen Fähigkeiten in den Kernelementen Sprungwurf, Passsicherheit und 1-gegen-1-Situationen gemäß dem DHB-Bewertungsframework.",
    "type": "textarea"
  },
  {
    "key": "3_taktisches_verstaendnis",
    "section": "Taktische Analyse",
    "title": "Taktisches Spielverständnis",
    "question": "Beschreiben Sie Ihr taktisches Verständnis für Angriff (z.B. 4+2-Formation, Tempogegenstoß) und Abwehr (z.B. 6:0-Deckung) anhand konkreter Spielsituationen.",
    "type": "textarea"
  },
  {
    "key": "4_physische_leistung",
    "section": "Physische Leistung",
    "title": "Physische Testwerte",
    "question": "Beschreiben Sie Ihre aktuellen physischen Leistungswerte in Bezug auf Standweitsprung, 30-Meter-Sprint, Yo-Yo-Intervall-Test und Beweglichkeitsscreening.",
    "type": "textarea"
  },
  {
    "key": "5_verletzungen_limitationen",
    "section": "Gesundheit",
    "title": "Verletzungen und Einschränkungen",
    "question": "Gibt es aktuelle oder frühere Verletzungen (z.B. an Schulter, Knie, Sprunggelenk) sowie körperliche Einschränkungen, die im Training beachtet werden müssen?",
    "type": "textarea"
  },
  {
    "key": "6_wochenplan_verfuegbarkeit",
    "section": "Trainingsplanung",
    "title": "Wöchentlicher Trainingsplan",
    "question": "Beschreiben Sie Ihre wöchentliche Verfügbarkeit für Training und Wettkampf inklusive der durchschnittlichen Trainingsstunden und der Aufteilung nach Saisonphasen.",
    "type": "textarea"
  },
  {
    "key": "7_ernaehrung_regeneration",
    "section": "Ernährung & Regeneration",
    "title": "Ernährung und Erholung",
    "question": "Beschreiben Sie Ihre aktuelle Ernährungspraxis an Trainingstagen und Spieltagen sowie Ihre Regenerationsmaßnahmen (z.B. Schlafmanagement, aktive Erholung).",
    "type": "textarea"
  },
  {
    "key": "8_trainingspraeferenzen_ausruestung",
    "section": "Training & Ausrüstung",
    "title": "Trainingspräferenzen und Ausrüstung",
    "question": "Welche Trainingspräferenzen haben Sie (z.B. Game-Based Approach, Einzeltraining) und welche sportartspezifische Ausrüstung steht Ihnen zur Verfügung?",
    "type": "textarea"
  },
  {
    "key": "9_karriereziele",
    "section": "Karriereziele",
    "title": "Kurz- und langfristige Ziele",
    "question": "Was sind Ihre kurzfristigen Ziele (nächste Saison) und langfristigen Ziele (3–5 Jahre) im Handball?",
    "type": "textarea"
  },
  {
    "key": "10_staerken_entwicklungsbereiche",
    "section": "Selbsteinschätzung",
    "title": "Stärken und Entwicklungsbereiche",
    "question": "Wie schätzen Sie subjektiv Ihre eigenen Stärken und die wichtigsten Entwicklungsbereiche gemäß Ihrem Spielerprofil ein?",
    "type": "textarea"
  }
]
"""

CLIENTS_PROFILE_QUESTIONS = [
    {
        "key": "1_yo_yo_ir1_zielwert",
        "section": "Primäres Leistungsziel",
        "title": "Yo-Yo IR1 Testziel",
        "question": "Welchen konkreten, numerischen Wert (in Metern oder Stufen) streben Sie als Ziel für den Yo-Yo Intermittent Recovery Test Level 1 an, um Ihre spielspezifische aerobe Kapazität und Erholungsfähigkeit für die Anforderungen des dynamischen Handballs signifikant zu verbessern?",
        "type": "number"
    },
    {
        "key": "2_aktuelle_leistungsstufe",
        "section": "Sportartspezifische Leistungsdaten",
        "title": "Aktuelles Leistungsniveau",
        "question": "Beschreiben Sie detailliert Ihr aktuelles Leistungsniveau gemäß der Systematik des Dokuments (Jugend, Amateur, Leistungskader), Ihre Position(spräferenz) sowie Ihre Vereinshistorie und die bisher erreichte höchste Spielklasse in Ihrer Handballkarriere.",
        "type": "textarea"
    },
    {
        "key": "3_technische_kernkompetenzen",
        "section": "Sportartspezifische Leistungsdaten",
        "title": "Technische Stärken und Defizite",
        "question": "Analysieren Sie präzise Ihre technischen Kernkompetenzen im Sprungwurf, Drehwurf, Fallwurf, in der Passsicherheit (Stand-, Sprung-, Druckpass) sowie im 1-gegen-1 unter Bezugnahme auf die im Bewertungsframework genannten Kriterien wie Anlauftechnik, Körperspannung und Entscheidungsgeschwindigkeit.",
        "type": "textarea"
    },
    {
        "key": "4_taktisches_verstaendnis",
        "section": "Sportartspezifische Leistungsdaten",
        "title": "Taktische Spielintelligenz",
        "question": "Beschreiben Sie Ihre Fähigkeit, taktische Szenarien zu lesen und Entscheidungen zu treffen. Wie schätzen Sie Ihr Verständnis für die Spielphilosophien im Angriff (z.B. 4+2-System, Tempogegenstoß) und in der Abwehr (z.B. 6:0, 5:1) sowie für positionsspezifische Aufgaben ein?",
        "type": "textarea"
    },
    {
        "key": "5_verletzungsanamnese",
        "section": "Körperliche Verfassung",
        "title": "Verletzungen und Einschränkungen",
        "question": "Listen Sie sämtliche relevante Verletzungen der für Handball kritischen Körperregionen (Schulter, Knie, Sprunggelenk, Rumpf) auf, inklusive Art, Zeitpunkt, Rehabilitationsverlauf und geben Sie an, ob diese als abgeschlossen gelten oder aktuell Einschränkungen im Training verursachen.",
        "type": "textarea"
    },
    {
        "key": "6_wochenplan_verfuegbarkeit",
        "section": "Training und Logistik",
        "title": "Wöchentliche Trainingsverfügbarkeit",
        "question": "Skizzieren Sie Ihren typischen Wochenplan: Wie viele Einheiten, welche Dauer und zu welchen Tageszeiten können Sie aktuell absolvieren? Berücksichtigen Sie dabei auch saisonale Phasen (Vorbereitung, Wettkampf, Übergang) und geben Sie feste, unverrückbare Termine an, die das Training beeinflussen.",
        "type": "textarea"
    },
    {
        "key": "7_ernaehrungs_recovery_routinen",
        "section": "Ernährung und Regeneration",
        "title": "Aktuelle Ernährung und Erholung",
        "question": "Beschreiben Sie detailliert Ihre aktuellen Ernährungsgewohnheiten an Trainingstagen und Spieltagen, Ihre Flüssigkeitszufuhr, die Verwendung von Supplementen sowie Ihre festen Routinen zur Regeneration (Schlafdauer, -qualität, aktive Erholung, Kälteanwendung) im Kontext der Handballbelastung.",
        "type": "textarea"
    },
    {
        "key": "8_trainingspraeferenzen_methodik",
        "section": "Training und Logistik",
        "title": "Präferierte Trainingsmethoden",
        "question": "Schildern Sie Ihre Vorlieben und Abneigungen bezüglich Trainingsmethoden: Bevorzugen Sie spielformbezogene Ansätze (Game-Based Approach), isolierte Technikschleifen, videogestützte Analyse oder spezifisches Athletiktraining? Welche Ausrüstung ist Ihnen regelmäßig zugänglich?",
        "type": "textarea"
    },
    {
        "key": "9_mentale_wettkampfvorbereitung",
        "section": "Zusätzlicher Kontext",
        "title": "Mentale Vorbereitungsroutinen",
        "question": "Erläutern Sie Ihre individuellen Routinen zur mentalen Wettkampfvorbereitung, inklusive Ihres idealen Aktivierungslevels, verwendeter Techniken wie Visualisierung oder Atemübungen sowie Ihrer Strategien für den Umgang mit Leistungsdruck und Rückschlägen während eines Spiels.",
        "type": "textarea"
    },
    {
        "key": "10_entwicklungsziele_reflexion",
        "section": "Zusätzlicher Kontext",
        "title": "Langfristige Entwicklungsziele",
        "question": "Formulieren Sie neben dem primären Leistungsziel Ihre kurzfristigen (nächste Saison) und langfristigen (3-5 Jahre) sportlichen Ziele sowie eine selbstkritische Einschätzung Ihrer größten Stärken und der zwei bis drei dringendsten Entwicklungsbereiche, die Sie im Training adressieren möchten.",
        "type": "textarea"
    }
]

PERSONALIZED_CONTEXT = """
CONFIG = {
    "PERSONALIZED_CONTEXT": \"\"\"# SPEZIFISCHE KUNDENDATEN - IMMER ZU VERWENDEN
Du erstellst einen Plan für ${user.name}. Nachfolgend findest du deren aktualisierte Daten.
Wende dein Analyseframework strikt auf diese Daten an, um die hyper-personalisierte Ausgabe zu generieren.
## STATISCHES PROFIL
${profileContext}
## ${dynamicDataContext}
Denke daran, deine Antwort mit einer Ansprache an ${user.name} zu beginnen und immer mit "- {APP_NAME}" zu unterschreiben.\"\"\"
}
"""

PROMPT_BUTTONS_LOGIC = """
promptBtnFull.onclick = () => handleVisualPromptClick("Erstelle eine adaptive Trainingseinheit von [DURATION_min] Minuten für das Ziel: [OBJECTIVE: z.B. Sprungkraft/Passsicherheit/Abwehrarbeit/Ausdauer]. Verfügbare Ausrüstung: extrahiere aus dem Kontext. RPE-Verlauf der letzten Woche: [Wert]. Technischer Schwerpunkt der Einheit: [Text]. Gib an: Aufwärmen (Minuten und Übungen), Technikarbeit (Übungen + Sätze x Dauer/Wiederholungen), Haupttrainingsblock (Kraft/Kondition), Zusatzübungen, Zeitvorgaben für die Blöcke und eine vorgeschlagene Progression für die nächsten 3 Einheiten. Berücksichtige dabei positionsspezifische Anforderungen (Torwart, Rückraum, Kreis, Außen) und integriere spielnahe Formen zur Automatisierung der technisch-taktischen Handlungen.");
promptBtnTraining.onclick = () => handleVisualPromptClick("Für die beschriebene Basiseinheit: [KURZE EINHEITSBESCHREIBUNG], generiere 3 Varianten (Leicht / Standard / Intensiv). Für jede Variante gib Änderungen im Volumen (Anzahl der Wiederholungen, Sätze, Spielformen), der Intensität (Wurfgeschwindigkeit, Verteidigungsdruck), den Pausenzeiten und dem erwarteten RPE an. Liefer klare Entscheidungsregeln für die Wahl der Variante basierend auf dem durchschnittlichen RPE der Vorwoche, der aktuellen Schlafqualität und dem subjektiven Erschöpfungslevel der Spieler. Definiere auch Anpassungen der technischen Fokusaufgaben.");
promptBtnCycle.onclick = () => handleVisualPromptClick("Programmiere 4 aufeinanderfolgende Mikro-Progressionen für [FERTIGKEIT: z.B. Sprungwurf aus dem Rückraum] ausgehend von der aktuellen Bestleistung [Anzahl Treffer/Erfolgsquote] unter [BEDINGUNGEN: z.B. Gegnerdruck]. Ziel: +[%] Trefferquote in 4 Einheiten. Spezifiziere für jede Einheit: Hauptübung (z.B. 2-gegen-1 mit Torabschluss), Sätze x Wiederholungen/Dauer, Schwierigkeitsmodifikation (Abstand, Gegnerdruck, Zeitvorgabe), Ziel-RPE und technische Hinweise für die perfekte Ausführung (z.B. Absprungpunkt, Armzug, Handgelenkseinsatz). Lege fest, wann die Progression als erreicht gilt.");
promptBtnPreEvent.onclick = () => handleVisualPromptClick("Bereite einen Peaking-Block von [Tage: 7-10] Tagen zur Maximierung der Testleistung [TEST: z.B. maximaler Yo-Yo IR1 Score oder 30m Sprintzeit] mit Testdatum [DATUM] vor. Beziehe ein: Tapering (Reduktion von Volumen und Intensität), tägliche Programmierung (Aufwärmen, technische Wiederholungen, regenerative Maßnahmen), 48h vor dem Test eine detaillierte Ernährungsstrategie (Mahlzeiten, Timing, Hydration) und einen Post-Test-Erholungsplan (aktive Regeneration, Nährstoffzufuhr, Schlafprotokoll) zur schnellen Regeneration für den folgenden Trainingszyklus.");
promptBtnSkill.onclick = () => handleVisualPromptClick("Organisiere die Versuchsabfolge für den Testtag der [FERTIGKEIT: z.B. 7m Strafwurf unter Druck]: detailliertes Aufwärmen (10-15 Min. mit Mobilisation und ersten Würfen), 5 gestaffelte Versuche mit genauen Zielzeiten/Präzisionsvorgaben, empfohlene Erholung zwischen den Versuchen (aktive Pause, mentale Vorbereitung), Abbruchkriterien (Schmerz >3, technischer Zusammenbruch, RPE >9) und ein abschließendes Debriefing mit zu protokollierenden Metriken (Trefferquote, Wurfgeschwindigkeit, subjektive Sicherheit, Herzfrequenz).");
promptBtnWeeklyAnalysis.onclick = () => handleVisualPromptClick("Generiere ein tägliches Prehab- & Mobilitätsprotokoll von [DAUER_min] Minuten für [BEREICH: Handgelenke/Ellbogen/Schultern/Rumpf], Planungsdauer: [7/14] Tage, Level: [Anfänger/Fortgeschritten/Profi]. Für jeden Tag gib Übungen (mit wöchentlicher Progression, z.B. erhöhter Widerstand/ROM), Wiederholungen/Zeit und klare Abbruchsignale (z.B. stechender Schmerz, Nachziehen) an. Integriere positionsspezifische Übungen für Torhüter (Handgelenkstabilität) und Feldspieler (Schulterrotation).");
promptBtnInjury.onclick = () => handleVisualPromptClick("Erstelle einen textuellen Entscheidungsbaum für das akute Schmerzmanagement an [ORT: z.B. Sprunggelenk] mit empfundener Intensität [1-10], Beginn [akut/schleichend], Vorhandensein von Schwellung [J/N]. Gib sofortige Maßnahmen an (Stopp/Modifikation des Trainings), Kriterien für Deload vs. ärztliche Konsultation (z.B. Instabilität, anhaltende Schwellung), konservative Maßnahmen (Kryotherapie, Kompression, leichte Mobilisation) und klare Kriterien für die Rückkehr zum Training (schmerzfreie Belastbarkeit, volle Bewegungsamplitude, sportartspezifische Tests).");
promptBtnTimeSaver.onclick = () => handleVisualPromptClick("Schlage eine Kalorienkorrektur und Makronährstoff-Priorisierung vor ausgehend von: aktuellem Gewicht, wöchentlicher Gewichtsveränderung [z.B. 0.2 kg pro Woche], Zielgewicht, Zielproteinmenge [z.B. 2g pro kg KG]. Gib einen Kalorienanpassungsbereich (+/- kcal) an, empfohlene Makroverteilung (KH/Protein/Fett) in % und g, sowie eine Checkliste der zu überwachenden Parameter in den folgenden 2 Wochen (Körpergewicht, Energielevel, Regeneration, Leistung im Training). Berücksichtige den erhöhten Energiebedarf bei mehreren Trainingseinheiten pro Tag.");
promptBtnMindBody.onclick = () => handleVisualPromptClick("Erstelle eine minimale Progression-Bibliothek für Ausrüstung: [extrahiere verfügbare Ausrüstung aus dem Profil]. Für jede Schlüsselübung ([z.B. Wurfkraft mit Medizinball und Plyometrische Abwehrarbeit]) liefere 5 Progressionsschritte und 2 sichere Regressionen, mit klaren Kriterien für den Aufstieg (z.B. technische Beherrschung, RPE-Wert) und dem Ziel-RPE für jede Stufe. Beschreibe die genaue Ausführung und Integration in das Mannschaftstraining.");
promptBtnNutrition.onclick = () => handleVisualPromptClick("Verfasse ein mentales Vorbereitungsskript von [DAUER_s: z.B. 75] Sekunden für den Pre-Versuch bei [FERTIGKEIT: z.B. 7m-Strafwurf], Intention: [ruhig/Motivation/Konzentration]. Beziehe ein: Atemmuster (Ein- und Ausatmungsdauer), 3 spezifische motorische Cues (z.B. 'Standbein fest', 'Ellbogen hoch', 'Handgelenk schnappen'), einen motivierenden Satz zur Wiederholung und Anweisungen zur Körperhaltung/physikalischen Vorbereitung (Standposition, Ballhaltung, Blickrichtung). Das Skript muss in der Ich-Form formuliert sein.");
promptBtnPlan.onclick = () => handleVisualPromptClick("Generiere ein wöchentliches Coach-Spieler-Briefing: beinhaltet 1) KPI-Zusammenfassung (Gewicht, Körperfettanteil, Stresslevel, Schlaf, absolvierte Workouts), 2) einen technischen Schwerpunkt für die Woche (z.B. Verbesserung des Stellpasses), 3) zwei praktische Aufgaben (z.B. Mobilisationsroutine/Ernährungsprotokoll/Videoanalyse), 4) erforderlichen Check-in (Tag/Uhrzeit), und 5) eine kurze motivierende Notiz. Strukturiere es zur direkten Verwendung in einer Messaging-App.");
promptBtnChecklist.onclick = () => handleVisualPromptClick("Erstelle eine A4-Checkliste für die [sportspezifische Einheit: z.B. Abwehr-Intensivierung] Einheit. Beinhaltet: Kopfzeile mit Datum/Uhrzeit, Pre-Workout (Mahlzeit, Hydration), benötigte Ausrüstung, Aufwärmen Schritt für Schritt, Technikarbeit, exzentrische Kraftübungen, Rumpfarbeit, Cool-down, Videoanalyse-Punkte, zu erfassende KPIs und Warnsignale (Schmerz, Erschöpfung). Lasse ausfüllbare Leerstellen für Zeiten/Notizen. Formatiere es klar und druckoptimiert mit Tabellen und Aufzählungszeichen.");
promptBtnBodyComp.onclick = () => handleVisualPromptClick("Bereite 7 mentale Mikro-Routinen zur Verbesserung von Fokus und Stressmanagement vor: beinhaltet 1) Pre-Workout 60s Atmung + 20s Visualisierung einer erfolgreichen Aktion, 2) Pre-Versuch 90s Ritual (Atemtechnik, Cue-Worte, physisches Aufschütteln), 3) Post-Session Debriefing Journaling mit 5 spezifischen Fragen zur Leistung und Lernmomenten. Liefere wortwörtliche Skripte und Zeitvorschläge für die Integration in den Trainingsalltag.");
promptBtnVariation.onclick = () => handleVisualPromptClick("Erstelle einen wöchentlichen Ernährungsplan zur Erreichung der Makroziele. Liefere 7 Tage mit Portionsangaben, kcal/Makro-Werten pro Mahlzeit und eine rationalisierte wöchentliche Einkaufsliste (Proteine, Kohlenhydrate, Gemüse, Fette, Snacks). Berücksichtige die unterschiedlichen Bedürfnisse an Trainingstagen, Spieltagen und Ruhetagen. Plane Mahlzeiten für vor und nach dem Training/Spiel ein und beachte praktikable Zubereitungszeiten.");
promptBtnRecovery.onclick = () => handleVisualPromptClick("Erstelle 8 Nachrichtenvorlagen (SMS/E-Mail) für Accountability: 1) Erinnerung vor dem Training, 2) Check-in nach der Einheit, 3) Kritische Woche (Deload/Wettkampfvorbereitung), 4) Meilenstein-Feier (z.B. persönliche Bestleistung). Halte einen direkten und motivierenden Ton bei. Liefere auch empfohlene Sendezeiten (z.B. 90 Min. vor Einheitsbeginn, 2 Std. nach Einheitsende). Personalisiere die Vorlagen mit Platzhaltern für Spielernamen und individuelle Ziele.");
"""

VARIABLES_TO_EXTRACT = """
[
    {"id": "var_current_sprungwurf_trefferquote", "label": "Aktuelle Sprungwurf-Trefferquote", "unit": "%", "type": "number"},
    {"id": "var_rpe", "label": "Subjektive Belastung (RPE)", "unit": "RPE (1-10)", "type": "number"},
    {"id": "var_schmerzlevel", "label": "Schmerzlevel", "unit": "Skala (0-10)", "type": "number"},
    {"id": "var_schlafqualitaet", "label": "Schlafqualität", "unit": "Skala (1-10)", "type": "number"},
    {"id": "var_motivation", "label": "Motivation", "unit": "Skala (1-10)", "type": "number"}
]
"""
