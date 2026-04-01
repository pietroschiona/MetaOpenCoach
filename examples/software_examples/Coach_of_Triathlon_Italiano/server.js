// ============================================================
// TASK 2: Silent Crash Prevention
// Capture any unhandled error and keep the window open
// ============================================================
process.on('uncaughtException', (err) => {
    console.error('\n====================================================');
    console.error('CRITICAL FATAL ERROR (uncaughtException):', err);
    console.error('====================================================\n');
    console.log('Press ENTER to close this window...');
    process.stdin.resume();
    process.stdin.once('data', () => process.exit(1));
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('\n====================================================');
    console.error('UNHANDLED PROMISE (unhandledRejection):', reason);
    console.error('====================================================\n');
});

try {
    require.resolve('express');
} catch (e) {
    console.error('\n====================================================');
    console.error('FATAL ERROR: Missing Node dependencies (e.g. express).');
    console.error('Please run "npm install" before starting the server.');
    console.error('====================================================\n');
    process.exit(1);
}

const express = require('express');
const path = require('path');
const fs = require('fs');
const fsPromises = require('fs').promises;
const { exec } = require('child_process');
const http = require('http');
const { WebSocketServer } = require('ws');
const helmet = require('helmet');
const cors = require('cors');
const { SyncRedactor } = require('redact-pii');
const analyticsEngine = require('./analytics-engine');
const dbCrypto = require('./db-crypto');
const auth = require('./server-auth'); // NEW: Import auth engine
const ragEngine = require('./rag_engine'); // NEW: Vector RAG Engine


// --- INITIAL CONFIGURATION ---
const app = express();
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      ...helmet.contentSecurityPolicy.getDefaultDirectives(),
      "script-src": ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
      "style-src": ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
      "img-src": ["'self'", "data:", "https:"],
      "connect-src": ["'self'", "ws:", "wss:", "http:", "https:"]
    },
  },
}));
app.use(cors());
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

let shutdownTimer = null; // Centralized shutdown handler
const SHUTDOWN_TIMEOUT = 45000; // 45 seconds (increased to support slow navigation)
const STARTUP_GRACE_PERIOD = 600000; // 10 minutes for first startup

function resetShutdownTimer() {
    if (shutdownTimer) {
        clearTimeout(shutdownTimer);
        shutdownTimer = null;
    }
}

function startShutdownTimer(delay = SHUTDOWN_TIMEOUT) {
    resetShutdownTimer();
    shutdownTimer = setTimeout(() => {
        if (wss.clients.size === 0) {
            console.log(`[SHUTDOWN] No clients connected for ${delay/1000}s. Shutting down...`);
            shutdown();
        }
    }, delay);
}

const redactor = new SyncRedactor({
  builtInRedactors: {
    digits: { enabled: false }
  }
});


let port = Number(process.env.PORT) || 3000;

// TASK 1: File Mutabili → Percorso persistente esterno per file pacchettizzati
const isPkg = typeof process.pkg !== 'undefined';
const baseDir = isPkg ? path.dirname(process.execPath) : process.cwd();
const dbPath = path.join(baseDir, 'database.json');

let startupTimeout = null;

// --- DATABASE MANAGEMENT (JSON FILE) ASYNC ---
// FIX: Serialized write queue to prevent race conditions on database.json.
// All writes are queued and never executed in parallel.
let dbWriteQueue = Promise.resolve();

// --- PREDEFINED AI CONFIGURATION (Injected by gaGemini.py) ---
const AI_PROVIDER_DEFAULT = 'lmstudio';
const AI_BASE_URL_DEFAULT = 'http://localhost:1234/v1';
const AI_MODEL_DEFAULT = 'qwen3.5-2b';
const PERSONALIZED_CONTEXT_BASE = `# DATI SPECIFICI DEL CLIENTE - DA UTILIZZARE SEMPRE
Stai creando un piano per \${user.name}. Di seguito sono riportati i suoi dati aggiornati.
Applica rigorosamente il tuo framework di analisi a questi dati per generare l'output iper-personalizzato.
## PROFILO STATICO
\${profileContext}
## \${dynamicDataContext}
Ricorda di iniziare la tua risposta rivolgendoti a \${user.name} e di firmare sempre con "- {APP_NAME}".`;
const VARIABLES_TO_EXTRACT = `[
    {
        "id": "var_current_race_time",
        "label": "Tempo Attuale Obiettivo (min)",
        "unit": "min",
        "type": "number",
        "key": "var_current_race_time"
    },
    {
        "id": "var_ftp_cycling",
        "label": "Potenza di Soglia Funzionale (FTP) Ciclismo",
        "unit": "W",
        "type": "number",
        "key": "var_ftp_cycling"
    },
    {
        "id": "var_critical_swim_speed",
        "label": "Velocità Critica di Nuoto (CSS)",
        "unit": "m/s",
        "type": "number",
        "key": "var_critical_swim_speed"
    },
    {
        "id": "var_running_vdot",
        "label": "Indice di Corsa (VDOT)",
        "unit": "punti",
        "type": "number",
        "key": "var_running_vdot"
    },
    {
        "id": "var_resting_heart_rate",
        "label": "Frequenza Cardiaca a Riposo (FC a riposo)",
        "unit": "bpm",
        "type": "number",
        "key": "var_resting_heart_rate"
    }
]`;
const PROFILE_QUESTIONS_BASE = `[
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
]`;

async function readDb(dek) {
    await dbWriteQueue; // Reader lock: wait for pending writes
    const defaultData = { 
        settings: { 
            apiKey: '', 
            aiProvider: process.env.AI_PROVIDER || AI_PROVIDER_DEFAULT, 
            aiBaseUrl: process.env.AI_BASE_URL || AI_BASE_URL_DEFAULT, 
            aiModel: process.env.AI_MODEL || AI_MODEL_DEFAULT,
            configDone: false
        }, 
        users: [], 
        analytics: { lastCalculation: null, globalMetrics: {}, patterns: {}, benchmarks: {} } 
    };

    try {
        const rawData = await fsPromises.readFile(dbPath, 'utf8');
        if (!dek) return defaultData; // If no key, we can't read encrypted data
        
        try {
            const decrypted = dbCrypto.decrypt(rawData, dek);
            const parsed = JSON.parse(decrypted);
            // Ensure the object has the minimum structure
            return { ...defaultData, ...parsed };
        } catch (decryptErr) {
            console.warn("[DB] Decryption or parsing error, returning default.");
            return defaultData;
        }
    } catch (error) {
        return defaultData;
    }
}

async function writeDb(data, dek) {
    if (!dek) return;
    try {
        const jsonStr = JSON.stringify(data, null, 2);
        const encrypted = dbCrypto.encrypt(jsonStr, dek);
        await fsPromises.writeFile(dbPath, encrypted, 'utf8');
    } catch (error) {
        console.error("Encrypted database write error:", error.message);
    }
}

/**
 * safeWriteDb — Serialized wrapper for writeDb.
 * Queues each write guaranteeing sequential execution.
 * Prevents database corruption from concurrent API calls.
 */
function safeWriteDb(data, dek) {
    dbWriteQueue = dbWriteQueue
        .then(() => writeDb(data, dek))
        .catch(e => console.error('[DB WRITE QUEUE] Serialized write error:', e.message));
    return dbWriteQueue;
}

async function initDb() {
    try {
        const stats = await fsPromises.stat(dbPath);
        if (stats.size > 10 * 1024 * 1024) {
            console.warn(`\n[SCALABILITY WARN] database.json has reached critical size (${(stats.size / 1024 / 1024).toFixed(2)} MB). Memory footprint may cause instability (OOM). Recommended to limit active users per instance.\n`);
        }
        await fsPromises.access(dbPath);
    } catch (err) {
        if (err.code === 'ENOENT') {
            const isPkg = typeof process.pkg !== 'undefined';
            console.log(`[DB] Database not found at ${dbPath}. Creating new database...`);
            const emptyDb = {
                settings: { 
                    apiKey: '', 
                    aiProvider: 'lmstudio', 
                    aiBaseUrl: 'http://localhost:1234/v1', 
                    aiModel: 'qwen3.5-2b',
                    configDone: false
                },
                users: [],
                analytics: { lastCalculation: null, globalMetrics: {}, patterns: {}, benchmarks: {} }
            };
            await fsPromises.writeFile(dbPath, JSON.stringify(emptyDb, null, 2), 'utf8');
        }
    }
}

// --- UTILITY FUNCTIONS ---
function openBrowser(targetPort) {
    const url = `http://localhost:${targetPort || port}`;
    let command;
    switch (process.platform) {
        case 'darwin': command = `open ${url}`; break;
        case 'win32': command = `start "" "${url}"`; break;
        default: command = `xdg-open ${url}`; break;
    }
    console.log(`Executing command to open browser: ${command}`);
    exec(command, (err) => {
        if (err) {
            console.error("Error opening browser automatically:", err);
            console.warn(`Manually open this address in your browser: ${url}`);
        }
    });
}

function redactPII(text) {
    // If we're using localhost, we skip PII redaction
    const baseUrl = process.env.AI_BASE_URL || 'https://api.openai.com/v1';
    if (baseUrl.includes('localhost') || baseUrl.includes('127.0.0.1')) {
        return text;
    }
    return redactor.redact(text);
}
// NEW: Function to notify clients
function broadcastAnalyticsUpdate() {
    const message = JSON.stringify({ type: 'analytics_update' });
    wss.clients.forEach(client => {
        if (client.readyState === 1) { // WebSocket.OPEN
            client.send(message);
        }
    });
    console.log("Analytics update notification sent to all clients.");
}

// --- MIDDLEWARE ---
const publicPath = path.join(__dirname, 'public');
app.use(express.static(publicPath));
// FIX: 50KB limit for JSON body to prevent token-stuffing and silent 413 crashes.
app.use(express.json({ limit: '50kb' }));

app.use((req, res, next) => {
    if (req.path.startsWith('/api/auth') || req.path.startsWith('/api/public') || req.path === '/api/settings/test-ai') {
        return next();
    }
    const token = req.headers['authorization']?.split(' ')[1];
    if (token) {
        const dek = auth.getSessionDEK(token);
        if (dek) {
            req.dek = dek;
            req.userToken = token;
            return next();
        }
    }
    // Allow static files and HTML pages to load without auth, only block API
    if (!req.path.startsWith('/api/')) {
        return next();
    }
    // Check if auth file has users, if not, it's first run
    if (!auth.hasUsers()) {
        res.status(401).json({ error: 'First run', code: 'FIRST_RUN' });
        return;
    }
    res.status(401).json({ error: 'Unauthorized' });
});

app.post('/api/auth/register', async (req, res) => {
    const { username, password } = req.body;
    if (!username || !password) return res.status(400).json({ error: 'Username and password required' });
    try {
        // FIX VUL-002: await required because registerUser is now async (pbkdf2 non-blocking)
        const result = await auth.registerUser(username, password);
        // Force database encryption on first registration
        const database = await readDb(); // Reads in clear if not yet encrypted
        await safeWriteDb(database, result.dek);
        res.json({ message: 'User registered', token: result.sessionToken });
    } catch (e) {
        res.status(400).json({ error: e.message });
    }
});

// FIX VUL-002: login handler becomes async to await verifyUser (now non-blocking)
app.post('/api/auth/login', async (req, res) => {
    const { username, password } = req.body;
    try {
        const result = await auth.verifyUser(username, password);
        res.json({ message: 'Login successful', token: result.sessionToken });
    } catch (e) {
        res.status(401).json({ error: e.message });
    }
});

app.post('/api/auth/logout', (req, res) => {
    const token = req.headers['authorization']?.split(' ')[1];
    auth.logout(token);
    res.json({ message: 'Logged out' });
});

app.get('/api/auth/status', (req, res) => {
    const hasUsers = auth.hasUsers();
    res.json({ hasUsers });
});


// ====================================================================================
// =================== SOURCE OF TRUTH FOR PROFILE QUESTIONS =====================
// ====================================================================================
// ── ANALYTICS DEBOUNCE (prevents OOM on batch I/O) ──────────────
let analyticsTimer = null;
function scheduleAnalyticsRecalculation(dek) {
    if (analyticsTimer) clearTimeout(analyticsTimer);
    analyticsTimer = setTimeout(async () => {
        analyticsTimer = null;
        try {
            const currentDb = await readDb(dek);
            analyticsEngine.runFullRecalculation(currentDb);
            await safeWriteDb(currentDb, dek);
            broadcastAnalyticsUpdate();
        } catch(e) {
            console.warn('[ANALYTICS] Recalculation error:', e.message);
        }
    }, 1500);
}
// ────────────────────────────────────────────────────────────────

const PROFILE_QUESTIONS = [
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
];


// =================== SYSTEM PROMPT: CALICOACH 1.0 =====================================
// ====================================================================================
const SYSTEM_PROMPT = `
## RUOLO E IDENTITÀ
Sei Coach of Triathlon Italiano, un Allenatore AI di Triathlon d'élite, specializzato nella creazione di piani olistici e iper-personalizzati che integrano la preparazione atletica specifica, l'acquisizione di competenze tecniche avanzate e l'ottimizzazione della performance fisica e mentale tipica di questo sport multisciplinare. Il tuo obiettivo è guidare l'atleta attraverso una metodologia strutturata, basata su principi scientifici e un'approfondita analisi dei dati, per raggiungere obiettivi cronometrici e di completamento in modo sostenibile e consapevole.

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
7. MESSAGGIO MOTIVAZIONALE: Un incoraggiamento personalizzato che riprende una caratteristica dell'atleta e lo impegna nel processo, firmato "- Coach of Triathlon Italiano".
`;
// ====================================================================================
// --- API ENDPOINTS ---
// =================== AGNOSTIC AI ENDPOINTS =========================================
app.get('/api/settings/ai-config', async (req, res) => {
    const db = await readDb(req.dek);
    const settings = db.settings || {};
    res.json({
        apiKey: settings.apiKey || '',
        aiProvider: settings.aiProvider || 'lmstudio',
        aiBaseUrl: settings.aiBaseUrl || 'http://localhost:1234/v1',
        aiModel: settings.aiModel || 'qwen3.5-2b',
        configDone: !!settings.configDone
    });
});

app.post('/api/settings/ai-config', async (req, res) => {
    const { apiKey, aiProvider, aiBaseUrl, aiModel } = req.body;
    const db = await readDb(req.dek);
    
    db.settings = {
        ...db.settings,
        apiKey: (apiKey || '').trim(),
        aiProvider: aiProvider || 'openai',
        aiBaseUrl: (aiBaseUrl || 'https://api.openai.com/v1').trim(),
        aiModel: (aiModel || 'gpt-4o-mini').trim(),
        configDone: true
    };
    
    await safeWriteDb(db, req.dek);
    res.json({ message: 'AI configuration saved successfully!' });
});

app.get('/api/users', async (req, res) => {
    const db = await readDb(req.dek);
    res.json(db.users); 
});

app.get('/api/users/:id', async (req, res) => {
    const db = await readDb(req.dek);
    const user = db.users.find(u => u.id === req.params.id);
    if (!user) return res.status(404).json({ error: "User not found" });
    res.json(user);
});

// Funzione per ottenere il numero della settimana ISO
Date.prototype.getWeek = function() {
  const date = new Date(this.getTime());
  date.setHours(0, 0, 0, 0);
  date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
  const week1 = new Date(date.getFullYear(), 0, 4);
  return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7);
}

app.post('/api/users', async (req, res) => {
    const db = await readDb(req.dek);
    const newUser = req.body;
    if (db.users.some(u => u.id === newUser.id)) return res.status(400).json({ error: "User ID already exists." });
    
    newUser.chatHistory = []; 
    newUser.longTermSummary = "";
    newUser.createdAt = Date.now();
    newUser.progressData = { weightHistory: [], performanceHistory: [], adherenceHistory: [] };
    newUser.riskFactors = { lastUpdate: null, adherenceScore: 0, progressScore: 0, engagementScore: 0, riskLevel: 'medium', predictedChurnDate: null };
    
    // Logica di salvataggio più robusta
    const benchmarkProfile = { initialWeight: 0, targetWeight: 0 };
    const goalKey = (process.env.PRIMARY_GOAL_KEY || 'weight').toLowerCase();
    
    for (const [key, value] of Object.entries(newUser.profile || {})) {
        const lowerKey = key.toLowerCase();
        if (lowerKey.includes(goalKey) || lowerKey.includes('peso')) {
            const parsedVal = parseFloat(value);
            if (!isNaN(parsedVal)) {
                if (benchmarkProfile.initialWeight === 0) benchmarkProfile.initialWeight = parsedVal;
                benchmarkProfile.targetWeight = parsedVal;
            }
        }
    }
    newUser.benchmarkProfile = benchmarkProfile;
    
    db.users.push(newUser);
    await safeWriteDb(db, req.dek);
    res.status(201).json(newUser);
});

app.put('/api/users/:id', async (req, res) => {
    const db = await readDb(req.dek);
    const userIndex = db.users.findIndex(u => u.id === req.params.id);
    if (userIndex === -1) return res.status(404).json({ error: "User not found" });
    
    const existingUser = db.users[userIndex];
    const updatedUser = { ...existingUser, ...req.body, id: req.params.id };

    if (!updatedUser.benchmarkProfile) {
        updatedUser.benchmarkProfile = { initialWeight: 0, targetWeight: 0 };
    }
    if (updatedUser.profile['3_obiettivo_peso']) {
        updatedUser.benchmarkProfile.targetWeight = parseFloat(updatedUser.profile['3_obiettivo_peso']);
    }

    db.users[userIndex] = updatedUser;
    await safeWriteDb(db, req.dek);
    res.json({ message: "Profile updated!" });
});

app.delete('/api/users/:id', async (req, res) => {
    const db = await readDb(req.dek);
    const initialLength = db.users.length;
    db.users = db.users.filter(u => u.id !== req.params.id);
    if (db.users.length === initialLength) return res.status(404).json({ error: "User not found" });
    await safeWriteDb(db, req.dek);
    scheduleAnalyticsRecalculation(req.dek);
    res.json({ message: "User deleted" });
});

app.get('/api/database', async (req, res) => {
    // Removed console.log to avoid log flooding in production
    const db = await readDb(req.dek);
    res.json(db);
});

// Helper function: calls LLM API with built-in https/http module (pkg compatible)
function llmPost(url, body, headers, timeoutMs) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const transport = parsed.protocol === 'https:' ? require('https') : require('http');
    const postData = JSON.stringify(body);
    let safeHostname = parsed.hostname;
    // Force IPv4 to avoid ECONNREFUSED ::1 with local models (LM Studio/Ollama)
    if (safeHostname === 'localhost') safeHostname = '127.0.0.1';

    const options = {
      hostname: safeHostname,
      port: parsed.port || (parsed.protocol === 'https:' ? 443 : 80),
      path: parsed.pathname + (parsed.search || ''),
      method: 'POST',
      headers: { ...headers, 'Content-Length': Buffer.byteLength(postData) }
    };
    const req = transport.request(options, (res) => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        try { resolve({ data: JSON.parse(data), status: res.statusCode }); }
        catch (e) { reject(new Error(`JSON parse error: ${data.slice(0, 200)}...`)); }
      });
    });
    req.on('error', reject);
    if (timeoutMs) req.setTimeout(timeoutMs, () => { req.destroy(); reject(new Error('timeout')); });
    req.write(postData);
    req.end();
  });
}

// Background RAG Compression
async function compressUserMemory(userId, apiKey, baseUrl, modelName, dek) {
    try {
        const db = await readDb(dek);
        const userIndex = db.users.findIndex(u => u.id === userId);
        if (userIndex === -1) return;
        const user = db.users[userIndex];
        
        // Compress everything except the last 4 messages
        const messagesToCompress = user.chatHistory.slice(0, -4);
        if (messagesToCompress.length === 0) return;

        const chatLog = messagesToCompress.map(m => `${m.role}: ${m.content}`).join('\n');
        const compressionPrompt = `
The following is a chat history between a sports AI Coach and athlete ${user.name}.
Previous historical summary:
"""
${user.longTermSummary || "None."}
"""

New messages for update:
"""
${chatLog}
"""

I ask you to update the "Previous historical summary" by integrating any FUNDAMENTAL information extracted from the "New messages" (e.g., injuries, diet changes, important training plan variations, logistical problems). 
RIGOROUSLY DISCARD all chatter, greetings, generic encouragements, and daily training tables. The goal is to maintain absolute brevity (maximum 10-15 bullet points).
Respond EXCLUSIVELY with the new updated summary. Do not include preambles or greetings.
`;
        const payload = {
            model: modelName,
            messages: [{ role: "system", content: "Sei un analista di dati sportivi. Il tuo unico compito è aggiornare concisamente un riassunto medico/tecnico." }, { role: "user", content: compressionPrompt }],
            temperature: 0.1
        };

        const response = await llmPost(
            `${baseUrl}/chat/completions`,
            payload,
            { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
            30000
        );
        const newSummary = (response.data.choices && response.data.choices[0] && response.data.choices[0].message)
                           ? response.data.choices[0].message.content.trim() : "";
                           
        if (newSummary) {
            // Reload DB for race conditions
            const freshDb = await readDb(dek);
            const freshUserIndex = freshDb.users.findIndex(u => u.id === userId);
            if (freshUserIndex !== -1) {
                const freshUser = freshDb.users[freshUserIndex];
                freshUser.longTermSummary = newSummary;
                
                const uncompressedStartTimestamp = user.chatHistory[user.chatHistory.length - 4].timestamp;
                freshUser.chatHistory = freshUser.chatHistory.filter(m => m.timestamp >= uncompressedStartTimestamp);
                
                freshDb.users[freshUserIndex] = freshUser;
                await safeWriteDb(freshDb, dek);
                console.log(`[RAG] Memory compression executed for User ${userId.slice(0,8)}. History updated.`);
            }
        }
    } catch(e) {
        console.error(`[RAG] Error during memory compression for User ${userId}:`, e.message);
    }
}

// ====== ENDPOINT TEST AI ISOLATO (Non richiede userId) ======
app.post('/api/settings/test-ai', async (req, res) => {
  const db = await readDb(req.dek);
  const settings = db.settings || {};
  
  const apiKey = req.body.apiKey || process.env.AI_API_KEY || settings.apiKey;
  const baseUrl = req.body.aiBaseUrl || process.env.AI_BASE_URL || settings.aiBaseUrl || 'https://api.openai.com/v1';
  const modelName = req.body.aiModel || process.env.AI_MODEL || settings.aiModel || 'gpt-4o-mini';

  if (!apiKey && !baseUrl.includes('localhost') && !baseUrl.includes('127.0.0.1')) {
     return res.status(400).json({ error: 'API key is not configured.' });
  }

  try {
    const response = await llmPost(
      `${baseUrl}/chat/completions`,
      { model: modelName, messages: [{ role: "user", content: "Ping" }], max_tokens: 5 },
      { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      15000
    );
    res.json({ message: "Test passed! The AI provider responds correctly." });
  } catch (error) {
    res.status(500).json({ error: `Test failed: ${error.message}` });
  }
});

// ====== ENDPOINT /api/chat AGNOSTICO E CON RAG VETTORIALE ======
app.post('/api/chat', async (req, res) => {
  const db = await readDb(req.dek);
  const settings = db.settings || {};
  
  const apiKey = process.env.AI_API_KEY || settings.apiKey;
  const baseUrl = process.env.AI_BASE_URL || settings.aiBaseUrl || 'https://api.openai.com/v1';
  const modelName = process.env.AI_MODEL || settings.aiModel || 'gpt-4o-mini';

  if (!apiKey && !baseUrl.includes('localhost') && !baseUrl.includes('127.0.0.1')) {
     return res.status(400).json({ error: 'API key is not configured.' });
  }
  
  const { userId, message } = req.body;
  // FIX: Truncate user message to 4000 chars (~1000 tokens) to prevent
  // token-stuffing and excessive payloads to LLM APIs.
  const MAX_MESSAGE_CHARS = 4000;
  const sanitizedMessage = (message || '').slice(0, MAX_MESSAGE_CHARS);

  const user = db.users.find(u => u.id === userId);
  if (!user) return res.status(404).json({ error: 'User not found.' });
  if (!user.chatHistory) { user.chatHistory = []; }

  const profileContext = PROFILE_QUESTIONS.map(q => {
      const value = (user.profile && user.profile[q.key]) ? user.profile[q.key].trim() : 'Not specified';
      return `- ${q.title}: ${value}`;
  }).join('\n');
  
  let dynamicDataContext = '# UPDATED DYNAMIC DATA (LAST CHECK-IN)';
  const { progressData } = user;
  let hasDynamicData = false;

  if (progressData && progressData.weightHistory && progressData.weightHistory.length > 0) {
      const lastWeightEntry = progressData.weightHistory[progressData.weightHistory.length - 1];
      dynamicDataContext += `\n- Last Recorded Weight: ${lastWeightEntry.weight || 'N/A'} kg`;
      if (lastWeightEntry.bodyFat) {
          dynamicDataContext += ` (Body Fat: ${lastWeightEntry.bodyFat} %)`;
      }
      hasDynamicData = true;
  }

  if (progressData && progressData.adherenceHistory && progressData.adherenceHistory.length > 0) {
      const lastAdherenceEntry = progressData.adherenceHistory[progressData.adherenceHistory.length - 1];
      if (lastAdherenceEntry.stressLevel) {
           dynamicDataContext += `\n- Stress Level (last week): ${lastAdherenceEntry.stressLevel}/10`;
      }
      if (lastAdherenceEntry.sleepHours) {
           dynamicDataContext += `\n- Sleep Hours (avg last week): ${lastAdherenceEntry.sleepHours} h`;
      }
      if (lastAdherenceEntry.rpe) {
           dynamicDataContext += `\n- Avg RPE (last week): ${lastAdherenceEntry.rpe}/10`;
      }
      hasDynamicData = true;
  }

  if (!hasDynamicData) {
      dynamicDataContext += '\nNo dynamic data recorded yet.';
  }
  
  // PII Redaction
  const redactedUserMsg = redactPII(sanitizedMessage);
  const redactedProfileContext = redactPII(profileContext);
  const redactedDynamicData = redactPII(dynamicDataContext);

  const personalizedContext = (PERSONALIZED_CONTEXT_BASE || "")
    .replace('${user.name}', user.name)
    .replace('${profileContext}', redactedProfileContext)
    .replace('${dynamicDataContext}', redactedDynamicData)
    .replace('${user.longTermSummary}', user.longTermSummary ? redactPII(user.longTermSummary) : "No relevant historical data extracted yet.")
    + `\n\nRemember to start your response addressing ${user.name} and always sign with "- Coach_of_Triathlon_Italiano".`;



  // ── SLIDING WINDOW + RAG ──────────────────────────────────
  const TOKEN_BUDGET = 9000;
  const estimateTokens = (str) => Math.ceil((str || '').length / 4);

  const fullHistory = user.chatHistory || [];
  const windowMessages = [];
  let usedTokens = estimateTokens(SYSTEM_PROMPT) + estimateTokens(personalizedContext);

  // 1. Fill window from most recent messages
  for (let i = fullHistory.length - 1; i >= 0; i--) {
    const t = estimateTokens(fullHistory[i].content);
    if (usedTokens + t > TOKEN_BUDGET) break;
    windowMessages.unshift(fullHistory[i]);
    usedTokens += t;
  }

  // 2. Messages outside window → RAG candidates
  const windowSet = new Set(windowMessages.map((_, idx) =>
    fullHistory.length - windowMessages.length + idx));
  const ragCandidates = fullHistory.filter((_, idx) => !windowSet.has(idx));

  // 3. If there are RAG candidates and current message has semantic meaning
  let ragContext = '';
  if (ragCandidates.length > 0) {
    try {
      const currentSettings = db.settings || {};
      const ragBaseUrl = currentSettings.aiBaseUrl || AI_BASE_URL_DEFAULT;
      const ragApiKey  = currentSettings.apiKey    || '';
      const ragModel   = currentSettings.aiModel   || AI_MODEL_DEFAULT;

      const queryVec = await ragEngine.generateEmbedding(
        sanitizedMessage, ragBaseUrl, ragApiKey, ragModel);

      // Assign dummy embedding if missing (degraded mode)
      const candidatesWithVec = ragCandidates
        .filter(m => Array.isArray(m.embedding) && m.embedding.length > 0)
        .map(m => ({ content: redactPII(m.content), role: m.role, embedding: m.embedding }));

      if (candidatesWithVec.length > 0) {
        const topK = ragEngine.getTopK(queryVec, candidatesWithVec, 5);
        if (topK.length > 0) {
          ragContext = '\n\n## RELEVANT HISTORY (from previous sessions)\n'
            + topK.map(r => `[${r.role.toUpperCase()}]: ${r.content}`).join('\n---\n') + '\n---';
        }
      }
    } catch (ragErr) {
      console.warn('[RAG WARN] Historical retrieval failed:', ragErr.message);
    }
  }

  // 4. Assembla i messaggi finali
  const finalSystemPrompt = SYSTEM_PROMPT + personalizedContext + ragContext;
  
  const messagesPayload = [
    { role: 'system', content: finalSystemPrompt },
    ...windowMessages.map(m => ({
        role: m.role === 'assistant' ? 'assistant' : 'user',
        content: redactPII(m.content)
    })),
    { role: 'user', content: redactedUserMsg }
  ];
  // ────────────────────────────────────────────────────────────
  


  try {
    console.log(`[CHAT] Sending request to ${modelName}. Cold start possible (max wait 4 min)...`);
    const response = await llmPost(
      `${baseUrl}/chat/completions`,
      { model: modelName, messages: messagesPayload, temperature: 1 },
      { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      240000
    );

    const aiReply = (response.data.choices && response.data.choices[0] && response.data.choices[0].message) 
                   ? response.data.choices[0].message.content 
                   : "Error: Invalid response from LLM API.";

    res.json({ reply: aiReply });

    // Immediate response to client — we DON'T wait for embeddings
    user.chatHistory.push({ role: "user", content: sanitizedMessage, timestamp: Date.now(), embedding: [] });
    user.chatHistory.push({ role: "assistant", content: aiReply, timestamp: Date.now(), embedding: [] });

    // Update embeddings in background (fire-and-forget)
    setImmediate(async () => {
      try {
        const freshDb = await readDb(req.dek);
        const freshUser = freshDb.users.find(u => u.id === userId);
        if (!freshUser) return;
        const uEmb = await ragEngine.generateEmbedding(sanitizedMessage, baseUrl, apiKey, modelName);
        const aEmb = await ragEngine.generateEmbedding(aiReply, baseUrl, apiKey, modelName);
        // Update last 2 messages (user + assistant) with real embeddings
        const hist = freshUser.chatHistory;
        if (hist.length >= 2) {
          hist[hist.length - 2].embedding = uEmb;
          hist[hist.length - 1].embedding = aEmb;
        }
        await safeWriteDb(freshDb, req.dek);
      } catch(e) {
        // Silent: failed embeddings don't compromise chat
      }
    });

    // RAG BACKGROUND COMPRESSION
    // If we have at least 10 messages, trigger async compression
    if (user.chatHistory.length >= 10 && user.chatHistory.length % 10 === 0) {
        compressUserMemory(user.id, apiKey, baseUrl, modelName, req.dek);
    }

    // FIX: DB scalability limitation (Sliding Window to reduce memory footprint)
    const MAX_CHAT_HISTORY = 40; // Keep only last 40 messages per user to prevent OOM kill on flat 50MB+ file
    if (user.chatHistory.length > MAX_CHAT_HISTORY) {
        user.chatHistory = user.chatHistory.slice(-MAX_CHAT_HISTORY);
    }

    // FIX: Anonymized log: doesn't expose username in clear in production logs.
    console.log(`[CHAT] Response generated for userId: ${userId.slice(0,8)}...`);
    const userIndex = db.users.findIndex(u => u.id === userId);
    if (userIndex !== -1) {
        analyticsEngine.calculateRiskFactors(user);
        db.users[userIndex] = user;
    }
    
    await safeWriteDb(db, req.dek);

    scheduleAnalyticsRecalculation(req.dek);

  } catch (error) {
    if (error.message && error.message.includes('timeout')) {
         console.error("Timeout during LLM API request.");
         res.status(500).json({ error: 'The coach is temporarily unavailable due to a timeout.' });
    } else {
         console.error("LLM API error:", error.message || error);
         res.status(500).json({ error: 'The coach is temporarily unavailable due to an LLM communication error.' });
    }
  }
});

app.post('/api/users/:id/progress', async (req, res) => {
    const { id } = req.params;
    const { weight, bodyFat, adherence } = req.body;
    const db = await readDb(req.dek);
    const userIndex = db.users.findIndex(u => u.id === id);

    if (userIndex === -1) return res.status(404).json({ error: "User not found" });

    const user = db.users[userIndex];
    const todayDate = new Date();
    const today = todayDate.toISOString().split('T')[0];
    const weekIdentifier = `${todayDate.getFullYear()}-W${String(todayDate.getWeek()).padStart(2, '0')}`;

    if (user.progressData.adherenceHistory.some(entry => entry.week === weekIdentifier)) {
        return res.status(403).json({ error: "Check-in for this week already performed." });
    }
    
    // --- START CORRECT BLOCK: Initial Weight Saving ---
    if (weight) {
        const parsedWeight = parseFloat(weight);
        // Check if it's the FIRST weight registration ever
        if (user.progressData.weightHistory.length === 0) {
            console.log(`[PROGRESS] First weight check-in for userId: ${id.slice(0,8)}. Initial weight: ${parsedWeight} kg.`);
            // Ensure benchmarkProfile exists
            if (!user.benchmarkProfile) {
                user.benchmarkProfile = { initialWeight: 0, targetWeight: 0 };
            }
            user.benchmarkProfile.initialWeight = parsedWeight;
        }
        user.progressData.weightHistory.push({ date: today, weight: parsedWeight, bodyFat: bodyFat ? parseFloat(bodyFat) : null });
    }
    // --- END CORRECT BLOCK ---

    if (adherence) {
        user.progressData.adherenceHistory.push({ week: weekIdentifier, ...adherence });
    }
    
    analyticsEngine.calculateRiskFactors(user);
    db.users[userIndex] = user;
    await safeWriteDb(db, req.dek);
    
    scheduleAnalyticsRecalculation(req.dek);
    
    res.json({ message: "Progress saved, analytics updated and initial weight confirmed!" });
});

app.get('/api/analytics/dashboard', async (req, res) => {
    const db = await readDb(req.dek);
    if (!db.analytics || !db.analytics.globalMetrics) {
        return res.status(500).json({ error: "Analytics data not yet calculated." });
    }

    // Calculate at-risk clients (existing logic)
    const atRiskClients = db.users.filter(u => u.riskFactors && u.riskFactors.riskLevel === 'high')
        .sort((a, b) => (a.riskFactors.adherenceScore || 0) - (b.riskFactors.adherenceScore || 0));

    // --- NEW LOGIC: Identify clients with missing check-in for current week ---
    const today = new Date();
    const currentWeekIdentifier = `${today.getFullYear()}-W${String(today.getWeek()).padStart(2, '0')}`;
    
    const clientsMissingCheckin = db.users.filter(user => {
        // If there's no adherence data, check-in is definitely missing
        if (!user.progressData || !user.progressData.adherenceHistory || user.progressData.adherenceHistory.length === 0) {
            return true;
        }
        // Check if there's an entry for the current week
        const hasCheckedInThisWeek = user.progressData.adherenceHistory.some(
            entry => entry.week === currentWeekIdentifier
        );
        // Return true (add to list) if they HAVEN'T done check-in
        return !hasCheckedInThisWeek;
    });
    // --- END NEW LOGIC ---

    // Calculate risk distribution (existing logic)
    const riskDistribution = [0, 0, 0]; // low, medium, high
    db.users.forEach(u => {
        if (u.riskFactors) {
            if (u.riskFactors.riskLevel === 'low') riskDistribution[0]++;
            else if (u.riskFactors.riskLevel === 'medium') riskDistribution[1]++;
            else if (u.riskFactors.riskLevel === 'high') riskDistribution[2]++;
        }
    });

    // Calculate adherence trend (existing logic)
    const adherenceTrend = { labels: [], data: [] };
    const allAdherenceEntries = db.users.flatMap(u => 
        (u.progressData && u.progressData.adherenceHistory) ? u.progressData.adherenceHistory : []
    );

    for (let i = 25; i >= 0; i--) {
        const targetDate = new Date();
        targetDate.setDate(targetDate.getDate() - (i * 7));
        
        const year = targetDate.getFullYear();
        const weekNum = targetDate.getWeek();
        const weekIdentifier = `${year}-W${String(weekNum).padStart(2, '0')}`;
        
        const label = `W${weekNum}`;
        adherenceTrend.labels.push(label);

        const entriesThisWeek = allAdherenceEntries.filter(entry => entry.week === weekIdentifier);
        
        let totalAdherenceRatio = 0;
        if (entriesThisWeek.length > 0) {
            const sumOfRatios = entriesThisWeek.reduce((sum, entry) => {
                if (entry.workouts_planned > 0) {
                    return sum + (entry.workouts_completed / entry.workouts_planned);
                }
                return sum;
            }, 0);
            totalAdherenceRatio = sumOfRatios / entriesThisWeek.length;
        }
        
        adherenceTrend.data.push(totalAdherenceRatio);
    }
    
    // Aggiungi la nuova lista alla risposta JSON
    res.json({
        globalMetrics: db.analytics.globalMetrics,
        atRiskClients,
        clientsMissingCheckin, // <-- NUOVO DATO INVIATO AL FRONTEND
        chartData: {
            riskDistribution,
            adherenceTrend
        }
    });
});
// ====================================================================================

wss.on('connection', ws => {
  ws.lastSeen = Date.now();
  console.log(`[WS] Client connected (${wss.clients.size} total).`);
  resetShutdownTimer();

  ws.on('message', message => {
    resetShutdownTimer(); // Reset also on client activity
    try {
      const data = JSON.parse(message);
      if (data.type === 'heartbeat_ack') {
        ws.lastSeen = Date.now();
      }
    } catch(e) {}
  });

  ws.on('close', () => {
    console.log(`[WS] Client disconnected. Remaining: ${wss.clients.size}`);
    if (wss.clients.size === 0) {
      startShutdownTimer();
    }
  });

  ws.on('error', error => { console.error('WebSocket error:', error); });
});

// Manual heartbeat every 10 seconds (sent from server)
const heartbeatInterval = setInterval(() => {
  const now = Date.now();
  wss.clients.forEach(ws => {
    // If client hasn't responded for more than 30 seconds, terminate
    if (now - ws.lastSeen > 30000) {
      console.log('[HEARTBEAT] Client timeout (>30s), terminating connection.');
      return ws.terminate();
    }
    // Send heartbeat signal
    if (ws.readyState === 1) { // WebSocket.OPEN
        ws.send(JSON.stringify({ type: 'heartbeat' }));
    }
  });
}, 10000);

function shutdown() {
  console.log('[SHUTDOWN IGNORED] Server will remain active to allow client reconnection.');
  // We don't close the server and don't execute process.exit(0).
  // This prevents closing during navigation on static pages like settings.html.
}

wss.on('close', shutdown);

function startServer(portToTry) {
  server.listen(portToTry, async () => {
    await initDb();
    port = portToTry; // Update global variable with actual port
    console.log(`\n🚀 MetaOpenCoach_Base listening on http://localhost:${port}`);
    console.log(`📁 Database:       ${dbPath}`);
    console.log(`📦 Packaged (pkg): ${!!process.pkg}`);
    console.warn(`\n[SECURITY] If you expose the app on network (not on localhost), you MUST implement an HTTPS proxy to protect the Bearer Token in transit from MITM attacks.\n`);

    openBrowser(port);

    startShutdownTimer(STARTUP_GRACE_PERIOD);
  });

  server.on('error', (e) => {
    if (e.code === 'EADDRINUSE') {
      console.log(`Port ${portToTry} busy, trying ${portToTry + 1}...`);
      startServer(portToTry + 1);
    } else {
      console.error("Server error:", e);
    }
  });
}

startServer(port);