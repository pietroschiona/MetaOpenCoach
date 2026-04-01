APP_NAME = "Coach of Triathlon Italiano"
SYSTEM_PROMPT = """
## RUOLO E IDENTITÀ
Sei {APP_NAME}, un Allenatore AI di Triathlon d'élite, specializzato nella creazione di piani olistici e iper-personalizzati che integrano la preparazione atletica specifica, l'acquisizione di competenze tecniche avanzate e l'ottimizzazione della performance fisica e mentale tipica di questo sport multisciplinare. Il tuo obiettivo è guidare l'atleta attraverso una metodologia strutturata, basata su principi scientifici e un'approfondita analisi dei dati, per raggiungere obiettivi cronometrici e di completamento in modo sostenibile e consapevole.

## PRINCIPI FONDAMENTALI
1. Progressività Tecnica e di Carico: Ogni piano segue una progressione calibrata di volume e intensità, adattata alle metriche specifiche del triathlon (FTP, CSS, VDOT), con incrementi massimi del 10% settimanale e fasi di scarico regolari per favorire la supercompensazione.
2. Enfasi sulla Tecnica ed Efficienza: La qualità dell'esecuzione nelle tre discipline (nuoto, ciclismo, corsa) e nelle transizioni (T1, T2) è prioritaria rispetto al volume fine a sé stesso, per massimizzare l'economia di movimento e prevenire infortuni.
3. Integrazione degli Obiettivi Multidisciplinari: Il piano bilancia in modo periodizzato lo sviluppo della potenza in bici, dell'economia di corsa e della tecnica in vasca, integrandoli con sessioni brick specifiche per condizionare il sistema neuromuscolare alle transizioni.
4. Sostenibilità e Adattamento al Contesto di Vita: Il carico di allenamento è modellato attorno agli impegni lavorativi, familiari e al profilo di recupero individuale dell'atleta, privilegiando la coerenza a lungo termine.
5. Sicurezza e Longevità Atletica: Massima priorità alla salute delle articolazioni e dei gruppi muscolari più sollecitati (spalle, ginocchia, tendine d'Achille), con protocolli proattivi di recupero e monitoraggio dei segnali di sovrallenamento.

## SISTEMA DI INTENSITÀ E AUTOREGOLAZIONE
Utilizza il Sistema Unificato a 5 Zone, adattato alle tre discipline, come riferimento assoluto per prescrivere l'intensità. L'atleta deve autoregolarsi in base alle sensazioni (RPE) e ai dati oggettivi (FC, Potenza, Passo):
- Zona 1 (Recupero Attivo): <68% FCmax, <55% FTP. Sensazione: Conversazione facilissima. Per rigenerazione.
- Zona 2 (Aerobica Base): 69-83% FCmax, 56-75% FTP. Sensazione: Respiro regolare, conversazione agevole. Fondamentale per costruire il motore aerobico.
- Zona 3 (Soglia Aerobica): 84-91% FCmax, 76-90% FTP. Sensazione: Sforzo avvertibile, conversazione a frasi spezzate. Usare con parsimonia.
- Zona 4 (Soglia Anaerobica): 92-97% FCmax, 91-105% FTP. Sensazione: Scomodo ma sostenibile per ripetute limitate. Sviluppo della potenza di soglia.
- Zona 5 (Massima Intensità): >97% FCmax, >105% FTP. Sensazione: Insostenibile a lungo, fatica muscolare acuta. Per intervalli brevi e potenza esplosiva.
L'autoregolazione è obbligatoria: se l'RPE percepito supera di due punti la zona target per più del 20% della sessione, l'atleta deve ridurre l'intensità e annotare la causa (sonno, stress, idratazione).

## FRAMEWORK DI ANALISI DEI DATI DEL CLIENTE
1. VALUTAZIONE FISICA E DEL CONTESTO: Analisi dell'età, del peso, della composizione corporea, della storia infortuni (>2 settimane negli ultimi 12 mesi) e del contesto di vita (ore realistiche di allenamento settimanali, qualità del sonno su scala 1-10, livello di stress lavorativo).
2. ANALISI DEL LIVELLO E DELLA PERFORMANCE: Classificazione in Beginner (<2 anni esperienza, distanze Sprint/Olympic), Intermediate (2-5 anni, completamenti 70.3), Advanced (>5 anni, obiettivi cronometrici su 70.3/Full). Raccolta dei parametri fisiologici cardine: FTP (ciclista), CSS (nuoto), VDOT (corsa) e FC a riposo mattutina (baseline).
3. DEFINIZIONE SPECIFICA DELL'OBIETTIVO: Creazione di una roadmap stagionale che identifichi la gara principale, gli obiettivi di performance per ogni disciplina (tempo target) e le fasi di periodizzazione (Base, Costruzione, Picco, Tapering).
4. VALUTAZIONE LOGISTICA E LIMITAZIONI: Inventario delle attrezzature disponibili (rulli, misuratore di potenza, GPS, pool accessibile), identificazione di limitazioni fisiche attuali (dolori, infortuni lievi) e vincoli di pianificazione (giorni di allenamento preferiti).

## STRUTTURA DELL'OUTPUT IPER-PERSONALIZZATO
SEZIONE 1: STRATEGIA NUTRIZIONALE FUNZIONALE: Prescrizione del fabbisogno calorico giornaliero (TDEE +/- in base all'obiettivo) e della ripartizione dei macronutrienti (CHO 55-65% in carico, 45-50% in scarico; Proteine 1.6-2.2g/kg; Grassi >20%), integrata da protocolli di nutrizione pre/intra/post allenamento e strategie race-specific per la distanza target.
SEZIONE 2: PROGRAMMAZIONE A LUNGO TERMINE: Suddivisione della preparazione in macroblocchi (es. 8 settimane Base, 6 settimane Costruzione, 3 settimane Picco, 2 settimane Tapering) con obiettivi fisiologici dichiarati, volumi settimanali indicativi (km nuoto/bici/corsa) e progressione del carico e dell'intensità.
SEZIONE 3: PIANO DI ALLENAMENTO SETTIMANALE: Per ogni giornata, specifica: Riscaldamento specifico per disciplina, Sessione Principale con parametri esatti (durata, distanza, zone target, ripetute, recupero), Sessioni Accessorie (forza, mobilità, tecnica) e Defaticamento. Include 1-2 sessioni Brick programmate in modo strategico.
SEZIONE 4: PROTOCOLLI DI SICUREZZA E RECUPERO: Piano di recupero attivo (sessioni Z1, foam rolling) e passivo (qualità del sonno, idratazione, crioterapia). Protocollo di risposta a segnali di sovrallenamento (giallo/arancio/rosso) con azioni correttive immediate.

## FORMATO DI OUTPUT FINALE
1. RIEPILOGO ESECUTIVO: Sintesi del profilo atleta, obiettivo stagionale principale e filosofia del piano personalizzato.
2. STRATEGIA NUTRIZIONALE: Dettaglio calorie, macros, timing e protocolli di integrazione.
3. PROGRAMMAZIONE A LUNGO TERMINE: Tabella o descrizione delle fasi di periodizzazione con volumi e focus.
4. PIANO DI ALLENAMENTO SETTIMANALE: Calendario giornaliero dettagliato per la settimana in corso, con istruzioni eseguibili.
5. PROTOCOLLI DI SICUREZZA: Istruzioni per il recupero e la gestione dei segnali di allarme.
6. SISTEMA DI AUTOREGOLAZIONE: Ripresa delle 5 Zone e istruzioni per la modifica in corso d'opera della sessione.
7. MESSAGGIO MOTIVAZIONALE: Un incoraggiamento personalizzato che riprende una caratteristica dell'atleta e lo impegna nel processo, firmato "- {APP_NAME}".
"""

PROFILE_QUESTIONS = """
[
  {
    "key": "1_tempo_gara_goal",
    "section": "Obiettivi",
    "title": "Tempo Target Gara",
    "question": "Qual è il tuo obiettivo cronometrico principale per la gara chiave della stagione, espresso in minuti totali?",
    "type": "number"
  },
  {
    "key": "2_anamnesi_esperienza",
    "section": "Anamnesi Sportiva",
    "title": "Livello ed Esperienza",
    "question": "Descrivi in dettaglio la tua esperienza nel triathlon, indicando anni di pratica, distanze affrontate e come ti collochi tra i livelli Beginner, Intermediate o Advanced del Metodo TRIFASE.",
    "type": "textarea"
  },
  {
    "key": "3_parametri_attuali",
    "section": "Parametri Fisiologici",
    "title": "Metriche di Performance",
    "question": "Descrivi i tuoi parametri fisiologici attuali, se conosciuti (FTP, CSS, VDOT, FC a riposo) e come hai ottenuto queste misurazioni.",
    "type": "textarea"
  },
  {
    "key": "4_distribuzione_intensita",
    "section": "Analisi Tecnica",
    "title": "Zone di Intensità",
    "question": "Come gestisci attualmente la distribuzione delle intensità (Zone 1-5) nelle tre discipline durante una settimana tipo?",
    "type": "textarea"
  },
  {
    "key": "5_infortuni_limitazioni",
    "section": "Salute e Prevenzione",
    "title": "Storia Infortuni",
    "question": "Descrivi eventuali infortuni pregressi o limitazioni fisiche, con particolare attenzione a spalle, ginocchia e piedi, aree critiche per il triatleta.",
    "type": "textarea"
  },
  {
    "key": "6_disponibilita_settimanale",
    "section": "Pianificazione",
    "title": "Programma Settimanale",
    "question": "Descrivi la tua disponibilità oraria settimanale reale per l'allenamento, includendo spostamenti, impegni fissi e finestre temporali preferite.",
    "type": "textarea"
  },
  {
    "key": "7_nutrizione_recupero",
    "section": "Nutrizione e Recupero",
    "title": "Strategie Nutrizionali",
    "question": "Descrivi le tue attuali abitudini nutrizionali, l'approccio al recupero attivo/passivo e la qualità media del sonno e dello stress.",
    "type": "textarea"
  },
  {
    "key": "8_attrezzatura_preferenze",
    "section": "Attrezzatura e Monitoraggio",
    "title": "Dispositivi e Accessi",
    "question": "Descrivi l'attrezzatura a tua disposizione (potenziometro, cardiofrequenzimetro, accesso piscina) e le tue preferenze di allenamento (es. sessioni brick, lavoro tecnico).",
    "type": "textarea"
  },
  {
    "key": "9_gestione_mentale",
    "section": "Psicologia dello Sport",
    "title": "Aspetto Motivazionale",
    "question": "Come gestisci le flessioni motivazionali e gli infortuni minori durante una preparazione lunga? Descrivi il tuo approccio mentale.",
    "type": "textarea"
  },
  {
    "key": "10_analisi_gare",
    "section": "Analisi Gare",
    "title": "Debriefing Precedenti",
    "question": "Quali sono state le lezioni principali apprese dalle tue gare recenti, in termini di ritmo, transizioni, nutrizione in gara e gestione della fatica?",
    "type": "textarea"
  }
]
"""

CLIENTS_PROFILE_QUESTIONS = [
    {
        "key": "1_tempo_gara_obiettivo",
        "section": "Obiettivi",
        "title": "Tempo Gara Target",
        "question": "Qual è il tempo target, espresso in minuti, che l'atleta si propone di realizzare nella gara principale della stagione, considerando la distanza (Sprint, Olympic, 70.3, Full Ironman) e le condizioni attese, come definito nell'ambito del piano di periodizzazione TRIFASE?",
        "type": "number"
    },
    {
        "key": "2_livello_prestazione_attuale",
        "section": "Valutazione Prestazione",
        "title": "Livello Attuale",
        "question": "Descrivi in dettaglio il tuo attuale livello di performance nelle tre discipline, includendo eventuali test recenti (FTP in watt, CSS in minuti/100m, VDOT o tempo sui 3000m) e le sensazioni soggettive durante gli allenamenti di endurance e intensità.",
        "type": "textarea"
    },
    {
        "key": "3_competenze_tecniche_disciplina",
        "section": "Valutazione Prestazione",
        "title": "Competenze Tecniche",
        "question": "Analizza le tue competenze tecniche specifiche per nuoto (bracciata, respirazione, virate), ciclismo (cambio marce, posizione in sella, gestione della potenza) e corsa (appoggio del piede, cadenza, postura), evidenziando i punti di forza e gli aspetti da migliorare.",
        "type": "textarea"
    },
    {
        "key": "4_storia_allenamento_recente",
        "section": "Valutazione Prestazione",
        "title": "Storia Allenamenti Recenti",
        "question": "Descrivi la struttura e il volume dei tuoi allenamenti nelle ultime 4-6 settimane, specificando la distribuzione tra le tre discipline, le ore totali, la presenza di sessioni brick e l'eventuale utilizzo del principio di polarizzazione del carico (80% bassa intensità, 20% alta intensità).",
        "type": "textarea"
    },
    {
        "key": "5_infortuni_limiti_fisici",
        "section": "Salute e Infortuni",
        "title": "Infortuni e Limiti",
        "question": "Elenca e descrivi in dettaglio qualsiasi infortunio o interruzione superiore a due settimane negli ultimi 12 mesi, con particolare attenzione a spalle (nuoto), ginocchia, tendini d'Achille e fascia plantare (corsa/bici), specificando le attuali limitazioni o necessità di lavoro preventivo.",
        "type": "textarea"
    },
    {
        "key": "6_disponibilita_settimanale",
        "section": "Disponibilità",
        "title": "Disponibilità Settimanale",
        "question": "Indica la tua disponibilità reale settimanale per l'allenamento, includendo il numero massimo di sessioni, la durata preferita per ciascuna, i giorni e gli orari (mattina/sera) più favorevoli, e i vincoli fissi di lavoro, famiglia o altri impegni che impattano la pianificazione.",
        "type": "textarea"
    },
    {
        "key": "7_abitudini_nutrizionali_recupero",
        "section": "Nutrizione e Recupero",
        "title": "Abitudini Nutrizionali",
        "question": "Descrivi le tue attuali abitudini alimentari, l'apporto di macronutrienti (carboidrati, proteine, grassi), l'uso di integratori, la strategia di idratazione e le pratiche di recupero attivo/passivo (sonno, foam rolling, crioterapia) che utilizzi regolarmente.",
        "type": "textarea"
    },
    {
        "key": "8_preferenze_metodologie_allenamento",
        "section": "Preferenze Allenamento",
        "title": "Preferenze e Metodi",
        "question": "Esponi le tue preferenze riguardo alle metodologie di allenamento (es. lavori in soglia, ripetute, lunghe distanze), il tipo di sessioni che ritieni più efficaci o motivanti e l'accesso ad attrezzature specifiche (rulli, piscina, tapis roulant) che hai a disposizione.",
        "type": "textarea"
    },
    {
        "key": "9_monitoraggio_segnali_sovrallenamento",
        "section": "Contesto Aggiuntivo",
        "title": "Monitoraggio e Segnali",
        "question": "Descrivi come monitori abitualmente il tuo carico e recupero (es. FC a riposo, qualità del sonno, HRV, TSS) e se hai recentemente sperimentato segnali di sovrallenamento come stanchezza cronica, irritabilità o stagnazione della performance nonostante l'allenamento.",
        "type": "textarea"
    },
    {
        "key": "10_contesto_psicologico_aspettative",
        "section": "Contesto Aggiuntivo",
        "title": "Aspetti Psicologici",
        "question": "Condividi il tuo attuale stato motivazionale, le eventuali flessioni o ansie pre-gara, le aspettative sul rapporto con il coach e come gestisci mentalmente le fasi di carico elevato e il tapering nella preparazione di una competizione importante.",
        "type": "textarea"
    }
]

PERSONALIZED_CONTEXT = """
CONFIG = {
    "PERSONALIZED_CONTEXT": \"\"\"
# DATI SPECIFICI DEL CLIENTE - DA UTILIZZARE SEMPRE
Stai creando un piano per ${user.name}. Di seguito sono riportati i suoi dati aggiornati.
Applica rigorosamente il tuo framework di analisi a questi dati per generare l'output iper-personalizzato.
## PROFILO STATICO
${profileContext}
## ${dynamicDataContext}
Ricorda di iniziare la tua risposta rivolgendoti a ${user.name} e di firmare sempre con "- {APP_NAME}".
\"\"\"
}
"""

PROMPT_BUTTONS_LOGIC = """
promptBtnFull.onclick = () => handleVisualPromptClick("Crea una sessione adattiva di [DURATION_min] minuti per l'obiettivo: [OBJECTIVE: potenza ciclistica/soglia corsa/tecnica nuoto/condizionamento generale]. Estrai l'attrezzatura disponibile dal profilo atleta (es. rulli, misuratore potenza, vasca). Storia RPE settimanale: [valore]. Priorità tecnica della sessione: [testo]. Fornisci: riscaldamento specifico (minuti ed esercizi di mobilità per la disciplina target), lavoro tecnico (esercizi + serie x durata/ripetizioni, es. nuoto: 8x50m focalizzati su rotazione), blocco principale di forza o potenza (es. ciclismo: 3x10' a Z4 con recupero 5' a Z1), lavoro accessorio (es. corsa: salite brevi o esercizi di forza a corpo libero), tempistica precisa per ogni blocco (in minuti) e progressione suggerita per le prossime 3 sessioni con incrementi di volume o intensità.");
promptBtnTraining.onclick = () => handleVisualPromptClick("Per la sessione base descritta: [BRIEF SESSION DESCRIPTION], genera 3 varianti (Leggera / Standard / Shock) specifiche per il triathlon. Per ogni variante indica le modifiche nel volume (es. da 40km a 30km in bici), intensità (es. cambiamento di zona Z2 a Z3), recuperi (es. da 2' a 4' tra le ripetute), e RPE atteso (da 4 a 9). Fornisci regole decisionali chiare per scegliere la variante in base alla media RPE degli ultimi 3 allenamenti e alla qualità media del sonno settimanale (es. se sonno <6/10 e RPE>7, usa variante Leggera).");
promptBtnNutrition.onclick = () => handleVisualPromptClick("Programma 4 micro-progressioni consecutive per [SKILL: es. nuoto a bracciata alta] partendo dal valore attuale [es. CSS 1:35/100m]. Obiettivo: miglioramento di [+0.05 m/s] in 4 sessioni. Specifica per ogni sessione: esercizio principale (es. nuoto con palette), serie x durata/rip (es. 10x100m a CSS+0.05), modifiche all'attrezzatura (es. uso/rimozione di pull buoy o palette), RPE target (da 5 a 8), e segnali tecnici per l'esecuzione perfetta (es. 'gomito alto in fase di trazione', 'ridurre il numero di bracciate per vasca').");
promptBtnPlan.onclick = () => handleVisualPromptClick("Prepara un blocco di picco di [Giorni: 7-10] giorni per massimizzare il test [TEST: es. FTP test +5%] con data del test [DATA]. Includi: tapering specifico (riduzione volume del 40-60% mantenendo intensità), programmazione giornaliera (intensità e riposo per nuoto, bici, corsa), strategia nutrizionale delle 48h pre-test (apporto di carboidrati, timing dei pasti, idratazione), e piano di recupero post-test (giorni di scarico attivo, ri-alimentazione, analisi dei dati).");
promptBtnSkill.onclick = () => handleVisualPromptClick("Organizza la sequenza di tentativi per il giorno del test su [SKILL: es. Test dei 3000m in corsa]: riscaldamento dettagliato (20' con progressivi e allunghi), 5 tentativi a rampa con tempi/obiettivi specifici (es. primo tentativo a ritmo gara, incrementi successivi), recupero raccomandato tra i tentativi (es. 5' di cammino attivo), criteri per l'interruzione (dolore articolare, cedimento tecnico, RPE >9), e debrief finale con metriche da registrare (FC a riposo post-test, percezione dello sforzo, split per km).");
promptBtnWeeklyAnalysis.onclick = () => handleVisualPromptClick("Genera un protocollo giornaliero di prehab & mobilità di [DURATION_min] minuti per [AREA: spalle/anche/caviglie], durata piano: [7/14] giorni, livello: [beginner/intermediate/advanced]. Per ogni giorno indica esercizi specifici per il triatleta (con progressione settimanale), ripetizioni/tempo (es. rotazioni scapolari 2x15, mobilità di caviglia 1' per lato), e segnali chiari per fermarsi (es. dolore acuto, formicolio, perdita di range di movimento).");
promptBtnRecovery.onclick = () => handleVisualPromptClick("Crea un diagramma di flusso testuale per la gestione del dolore acuto in [LOCATION: es. ginocchio] con intensità percepita [1-10], esordio [acuto/insidioso], presenza di gonfiore [S/N]. Fornisci passi immediati (interrompi/modifica l'allenamento), criteri per deload vs. consulto medico (es. se gonfiore e dolore>7, consulta), azioni conservative (ghiaccio, compressione, mobilità leggera), e criteri per il ritorno all'allenamento (assenza di dolore a riposo, range di movimento completo, test di carico graduale positivo).");
promptBtnTimeSaver.onclick = () => handleVisualPromptClick("Suggerisci una correzione calorica e le priorità macronutrienti partendo da: peso attuale [kg], variazione peso settimanale [es. -0.5 kg a settimana], peso target [kg], proteine target [es. 2g per kg]. Fornisci intervallo di aggiustamento kcal (+/- 200-500 kcal), distribuzione raccomandata dei macronutrienti (carboidrati 50-65%, proteine 20-25%, grassi 20-30%), e checklist di parametri da monitorare nelle 2 settimane successive (peso a digiuno, energia negli allenamenti, qualità del sonno, fame percepita).");
promptBtnMindBody.onclick = () => handleVisualPromptClick("Crea una libreria minima di progressione per l'attrezzatura disponibile: [estrai attrezzatura dal profilo, es. rulli smart, vasca 25m, scarpe da corsa]. Per ogni esercizio chiave ([es. intervalli di potenza in bici e ripetute in salita nella corsa]) fornisci 5 step di progressione (es. aumento watt, diminuzione recupero) e 2 regressioni sicure (es. riduzione pendenza, uso della bici da strada), con criteri per avanzare (RPE<7 per 2 sessioni consecutive) e RPE target per ogni step (da 5 a 9).");
promptBtnInjury.onclick = () => handleVisualPromptClick("Scrivi uno script di preparazione mentale di [DURATION_s: es. 90] secondi pre-tentativo su [SKILL: es. partenza in acque libere], intento: [calma/motivazione/concentrazione]. Includi: pattern respiratorio (es. 4 secondi inspiro, 6 secondi espiro per 5 cicli), 3 segnali motori specifici (es. 'spalle rilassate', 'rotazione del busto', 'focalizzazione sull'orizzonte'), una frase motivazionale da ripetere (es. 'Sono pronto, sono fluido'), e istruzioni sulla postura/preparazione fisica (es. 'controllo della posizione del corpo in galleggiamento').");
promptBtnVariation.onclick = () => handleVisualPromptClick("Genera un briefing settimanale coach-atleta per il triathlon: includi 1) riepilogo KPI (Peso, Massa Grassa, Stress percepito, Sonno medio, Allenamenti Completati), 2) una priorità tecnica per la settimana (es. 'transizione rapida T1'), 3) due compiti pratici (es. 'video analisi della bracciata' e 'piano nutrizionale per la lunga distanza'), 4) check-in richiesto (giorno/ora, es. mercoledì 18:00), e 5) una nota motivazionale breve legata all'obiettivo di stagione.");
promptBtnCycle.onclick = () => handleVisualPromptClick("Crea una checklist in formato A4 per la sessione [Sport-specific Session: es. Brick Bici+Corsa]. Includi: intestazione con data/ora, pre-workout (idratazione, snack), attrezzatura (casco, scarpe, gel), riscaldamento passo-passo (10' bici Z1, 5' progressivi), lavoro tecnico (es. transizioni), forza eccentrica (es. discese tecniche), core (es. plank 3x30''), cool-down (10' corsa Z1), revisione video (angoli da filmare), KPI (NP, TSS, passo medio), e segnali di allarme (dolore al tendine d'Achille, vertigini). Lascia spazi compilabili per tempi/note. Formatta chiaramente per la stampa.");
promptBtnPreEvent.onclick = () => handleVisualPromptClick("Prepara 7 micro-routine mentali per migliorare la focalizzazione e la gestione dello stress: includi 1) pre-workout 60s di respirazione + 20s di visualizzazione della sessione perfetta, 2) pre-tentativo 90s di rituale (controllo attrezzatura, frase chiave, scan corporeo), 3) debrief post-sessione di journaling con 5 domande (es. 'Cosa ho imparato?', 'Dove ho perso concentrazione?'). Fornisci script parola per parola e suggerimenti di tempistica (es. eseguire la routine 1 sempre 5' prima di iniziare).");
promptBtnBodyComp.onclick = () => handleVisualPromptClick("Crea un piano pasti settimanale per raggiungere i target macro. Fornisci 7 giorni con porzioni (es. 120g di petto di pollo, 80g di riso integrale), valori kcal/macro per pasto (colazione: 400 kcal, C50g P25g G10g), e una lista della spesa razionalizzata settimanale (proteine: pollo, pesce, uova; carboidrati: riso, quinoa, patate; verdure: broccoli, spinaci; grassi: avocado, olio EVO; snack: frutta secca, yogurt greco).");
promptBtnChecklist.onclick = () => handleVisualPromptClick("Crea 8 template di messaggio (SMS/email) per l'accountability nel triathlon: 1) promemoria pre-workout (es. 'Ricorda la sessione di soglia oggi alle 18'), 2) check-in post-sessione (es. 'Invia RPE e note tecniche'), 3) settimana critica (deload, es. 'Questa è la settimana di scarico, rispetto i recuperi'), 4) celebrazione traguardo (es. 'Complimenti per il nuovo PB sui 10km!'). Mantieni un tono diretto e motivante. Fornisci anche gli orari di invio consigliati (es. promemoria 2 ore prima, check-in entro 1h dal termine).");
"""

VARIABLES_TO_EXTRACT = """
[
    {"id": "var_current_race_time", "label": "Tempo Attuale Obiettivo (min)", "unit": "min", "type": "number"},
    {"id": "var_ftp_cycling", "label": "Potenza di Soglia Funzionale (FTP) Ciclismo", "unit": "W", "type": "number"},
    {"id": "var_critical_swim_speed", "label": "Velocità Critica di Nuoto (CSS)", "unit": "m/s", "type": "number"},
    {"id": "var_running_vdot", "label": "Indice di Corsa (VDOT)", "unit": "punti", "type": "number"},
    {"id": "var_resting_heart_rate", "label": "Frequenza Cardiaca a Riposo (FC a riposo)", "unit": "bpm", "type": "number"}
]
"""
