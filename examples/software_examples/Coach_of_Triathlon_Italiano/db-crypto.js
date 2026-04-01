const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const ALGORITHM = 'aes-256-gcm';

// We now expect the calling code (server.js) to provide the Data Encryption Key (DEK)
function encrypt(text, dek) {
    if (!dek) throw new Error("Missing DEK for encryption");
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(ALGORITHM, dek, iv);
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    const authTag = cipher.getAuthTag().toString('hex');
    return JSON.stringify({
        iv: iv.toString('hex'),
        data: encrypted,
        authTag: authTag
    });
}

function decrypt(encryptedRaw, dek) {
    if (!dek) throw new Error("Missing DEK for decryption");
    try {
        const payload = JSON.parse(encryptedRaw);
        if (!payload.iv || !payload.data || !payload.authTag) {
            return encryptedRaw;
        }
        const decipher = crypto.createDecipheriv(ALGORITHM, dek, Buffer.from(payload.iv, 'hex'));
        decipher.setAuthTag(Buffer.from(payload.authTag, 'hex'));
        let decrypted = decipher.update(payload.data, 'hex', 'utf8');
        decrypted += decipher.final('utf8');
        return decrypted;
    } catch (e) {
        return encryptedRaw;
    }
}

// Utility to derive a key from a password
// FIX VUL-002: use async crypto.pbkdf2 to avoid blocking the Event Loop.
// 100k SHA-512 iterations take ~300-800ms: pbkdf2Sync would block the server for all users.
function deriveKeyFromPassword(password, saltHex) {
    return new Promise((resolve, reject) => {
        const salt = Buffer.from(saltHex, 'hex');
        crypto.pbkdf2(password, salt, 100000, 32, 'sha512', (err, derivedKey) => {
            if (err) reject(err);
            else resolve(derivedKey);
        });
    });
}

module.exports = {
    encrypt,
    decrypt,
    deriveKeyFromPassword,
    ALGORITHM
};
