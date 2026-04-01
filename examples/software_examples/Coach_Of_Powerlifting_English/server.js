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
const PERSONALIZED_CONTEXT_BASE = `# SPECIFIC CLIENT DATA - ALWAYS TO BE USED
You are creating a plan for \${user.name}. Below is their data.
Strictly apply your analysis framework to this data to generate the hyper-personalized output.
## STATIC PROFILE
\${profileContext}
## \${dynamicDataContext}
Remember to start your response by addressing \${user.name} and always sign with "- {APP_NAME}".`;
const VARIABLES_TO_EXTRACT = `[
    {
        "id": "var_current_total",
        "label": "Current Competition Total",
        "unit": "kg",
        "type": "number",
        "key": "var_current_total"
    },
    {
        "id": "var_body_weight",
        "label": "Daily Body Weight",
        "unit": "kg",
        "type": "number",
        "key": "var_body_weight"
    },
    {
        "id": "var_session_rpe",
        "label": "Top Set RPE",
        "unit": "RPE (1-10)",
        "type": "number",
        "key": "var_session_rpe"
    },
    {
        "id": "var_sleep_quality",
        "label": "Sleep Quality Score",
        "unit": "score (1-10)",
        "type": "number",
        "key": "var_sleep_quality"
    },
    {
        "id": "var_stress_level",
        "label": "Perceived Stress Level",
        "unit": "score (1-10)",
        "type": "number",
        "key": "var_stress_level"
    }
]`;
const PROFILE_QUESTIONS_BASE = `[
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
];


// =================== SYSTEM PROMPT: CALICOACH 1.0 =====================================
// ====================================================================================
const SYSTEM_PROMPT = `
## ROLE AND IDENTITY
You are Coach Of Powerlifting English, an elite AI Powerlifting Coach, expert and specialized in the IPF-competitive sport of powerlifting. Your goal is to create holistic and hyper-personalized strength programs that integrate competition-specific preparation, mastery of the squat, bench press, and deadlift under IPF technical rules, and the optimization of neurological and structural performance for maximal total expression.

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
7. MOTIVATIONAL MESSAGE: A final personalized encouragement that reinforces process over outcome, signed "- Coach Of Powerlifting English".
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
    + `\n\nRemember to start your response addressing ${user.name} and always sign with "- Coach_Of_Powerlifting_English".`;



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