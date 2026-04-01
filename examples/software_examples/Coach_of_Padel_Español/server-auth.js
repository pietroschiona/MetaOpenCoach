const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const dbCrypto = require('./db-crypto');

const isPkg = typeof process.pkg !== 'undefined';
const baseDir = isPkg ? path.dirname(process.execPath) : process.cwd();

const authPath = path.join(baseDir, 'auth.json');
const sessionsPath = path.join(baseDir, 'sessions.json');

function loadSessions() {
    if (fs.existsSync(sessionsPath)) {
        try {
            const data = JSON.parse(fs.readFileSync(sessionsPath, 'utf8'));
            for (const token in data) {
                if (data[token].dek) {
                    data[token].dek = Buffer.from(data[token].dek, 'hex');
                }
            }
            return data;
        } catch (e) {
            console.error("Error loading sessions:", e);
            return {};
        }
    }
    return {};
}

function saveSessions() {
    try {
        const dataToSave = {};
        for (const token in activeSessions) {
            dataToSave[token] = {
                ...activeSessions[token],
                dek: activeSessions[token].dek ? activeSessions[token].dek.toString('hex') : null
            };
        }
        fs.writeFileSync(sessionsPath, JSON.stringify(dataToSave, null, 2), 'utf8');
    } catch (e) {
        console.error("Error saving sessions:", e);
    }
}

function readAuthFile() {
    if (fs.existsSync(authPath)) {
        return JSON.parse(fs.readFileSync(authPath, 'utf8'));
    }
    return { users: {} };
}

function writeAuthFile(data) {
    fs.writeFileSync(authPath, JSON.stringify(data, null, 2), 'utf8');
}

// Generate a random DEK (Data Encryption Key) to be wrapped by KEK (Key Encryption Key)
function generateDEK() {
    return crypto.randomBytes(32); // 256 bits
}

// FIX VUL-002: registerUser is now async because deriveKeyFromPassword returns a Promise.
async function registerUser(username, password) {
    const authData = readAuthFile();
    if (authData.users[username]) {
        throw new Error('Username already exists');
    }

    const salt = crypto.randomBytes(16).toString('hex');
    const kek = await dbCrypto.deriveKeyFromPassword(password, salt); // Key Encryption Key
    const dek = generateDEK(); // Data Encryption Key

    // Encrypt DEK with KEK
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(dbCrypto.ALGORITHM, kek, iv);
    let wrappedDEK = cipher.update(dek, null, 'hex');
    wrappedDEK += cipher.final('hex');
    const authTag = cipher.getAuthTag().toString('hex');

    authData.users[username] = {
        salt,
        iv: iv.toString('hex'),
        wrappedDEK,
        authTag
    };

    writeAuthFile(authData);

    return { username, sessionToken: generateSessionToken(username, dek), dek };
}

// FIX VUL-002: verifyUser is now async to await deriveKeyFromPassword.
async function verifyUser(username, password) {
    const authData = readAuthFile();
    const userRecord = authData.users[username];
    if (!userRecord) {
        throw new Error('Invalid username or password');
    }

    const kek = await dbCrypto.deriveKeyFromPassword(password, userRecord.salt);

    // Decrypt DEK
    try {
        const decipher = crypto.createDecipheriv(dbCrypto.ALGORITHM, kek, Buffer.from(userRecord.iv, 'hex'));
        decipher.setAuthTag(Buffer.from(userRecord.authTag, 'hex'));
        let dekStr = decipher.update(userRecord.wrappedDEK, 'hex', 'hex');
        dekStr += decipher.final('hex');
        const dek = Buffer.from(dekStr, 'hex');

        return { username, sessionToken: generateSessionToken(username, dek), dek };
    } catch (e) {
        throw new Error('Invalid username or password');
    }
}

// In-memory sessions (persisted to sessions.json)
const activeSessions = loadSessions();

function generateSessionToken(username, dek) {
    const token = crypto.randomBytes(32).toString('hex');
    activeSessions[token] = { username, dek, expiresAt: Date.now() + 24 * 60 * 60 * 1000 }; // 24h
    saveSessions();
    return token;
}

function getSessionDEK(token) {
    if (!token || !activeSessions[token]) {
        return null;
    }
    const session = activeSessions[token];
    if (Date.now() > session.expiresAt) {
        delete activeSessions[token];
        saveSessions();
        return null;
    }
    // Auto-extend session
    session.expiresAt = Date.now() + 24 * 60 * 60 * 1000;
    saveSessions();
    return session.dek;
}

function hasUsers() {
    const authData = readAuthFile();
    return Object.keys(authData.users).length > 0;
}

function logout(token) {
    if (token && activeSessions[token]) {
        delete activeSessions[token];
        saveSessions();
    }
}

module.exports = {
    registerUser,
    verifyUser,
    getSessionDEK,
    hasUsers,
    logout
};
