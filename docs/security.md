# Security & Privacy Shield: Data Sanctity

In MetaOpenCoach, the project operates on an inviolable principle: **health and performance data are sacred**. The architecture is designed to protect both the professional (IP) and the athlete (Privacy).

## TL;DR
MetaOpenCoach implements a multi-layered security strategy including local-first data sovereignty, military-grade encryption (AES-256), a PII redaction engine, and complete intellectual property protection for the coach's methodology.

## 1. Sovereignty by Design (Local-First)
Every generated application is a technological island:
- **Local Assets**: Critical libraries like `Chart.js` and `marked.js` are served internally. External CDNs are avoided to prevent tracking via script injection or analytics.
- **Offline Operations**: The core management system operates independently of cloud backends. The only external connection is to the chosen AI provider, which is gated by the integrated sanitization engine.

## 2. PII Redaction Shield
The integrated **PII Redaction Engine** (located in `server.js`) acts as a textual firewall. Before any message is sent to an external AI provider (OpenAI, Gemini), the system:
1. **Scans**: Identifies emails, phone numbers, and sensitive identifiers using the `redact-pii` production-grade library.
2. **Masks**: Replaces sensitive data with redaction placeholders (e.g., `[EMAIL_REDACTED]`).
3. **Reconstructs**: Only the professional's protected instance interface can re-associate the query with the athlete's real identity.

## 3. Military-Grade Encryption
Athlete profiles and history are stored in a local JSON database protected by:
- **AES-256-GCM**: Authenticated encryption that guarantees both confidentiality and data integrity.
- **PBKDF2 Hashing**: Secure key derivation with **100,000 iterations** of **SHA-512**, making brute-force attacks computationally prohibitive.
- **Random IVs**: Every write operation generates a unique initialization vector to defeat pattern analysis.

## 4. IP Protection for Methodology
For the professional, their method is their market value. MetaOpenCoach ensures:
- **Private Injection**: The methodology is distilled into hardcoded prompts that never leave the instance.
- **No Global Training**: Conversation data is processed within the instance context and is not used to train third-party models.

> [!CAUTION]
> MetaOpenCoach provides the shield, but the professional is responsible for the secure management of API keys and the host execution environment.

---
← [Back: Documentation Index](./Documentation_Index.md) | [Next: Deployment Guide →](./deployment.md)
