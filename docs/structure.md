# Technical Structure: Architecture & Hierarchical Metaprompting

MetaOpenCoach is a polymorphic application generator that coordinates two distinct software realms: Python for orchestration and Node.js for runtime.

## TL;DR
The system uses a Python-based orchestrator to inject methodology-derived intelligence into a hardened Node.js/Express template core. The core innovation lies in the **Hierarchical Metaprompting** approach, which ensures scientific precision and data sovereignty.

## System Architecture

MetaOpenCoach operates as a coordinate system:
- **Orchestrator (Python)**: Manages knowledge extraction (RAG), configuration injection via regex overwriting, and binary compilation via `pkg`.
- **Runtime Core (Node.js)**: A standalone, high-performance Express server serving as the engine for the generated coaching apps.

### The Atomic Injection Process
The power of the system lies in how it handles variables. Instead of a database lookup for base rules, the system performs **Regex Variable Overwriting** in the template JS files during the build phase. This hardcodes the methodology into the logic, making the binary completely self-contained.

## Hierarchical Metaprompting Approach

To achieve elite performance and eliminate hallucinations, MetaOpenCoach implements a multi-layered prompt architecture known as **Hierarchical Metaprompting**.

| Level | Component | Purpose |
|---|---|---|
| **L1** | Professional Identity | Definitive persona, voice, and ethical boundaries of the coach. |
| **L2** | Methodological Core | Injected rules, training principles, and scientific protocols derived from the documentation. |
| **L3** | Task-Specific Logic | Operational context for specific actions (e.g., assessment vs. prescription). |
| **L4** | Athlete History | Dynamic context including latest check-ins, biometrics, and psychological sentiment. |

This hierarchy ensures that the AI's "thought process" is perpetually anchored to the professional's methodology before it even considers the athlete's specific query.

## Tech Stack

- **Orchestration**: Python 3.10+ (Knowledge distillation & Build automation).
- **Core Engine**: Node.js & Express (High-concurrency runtime).
- **Security Logic**: AES-256-GCM, PBKDF2 (Sovereign encryption).
- **Real-Time Layer**: WebSockets (Live dashboard synchronization).
- **Frontend Layer**: Vanilla CSS & Modern components (No external CDNs).

---
← [Back: Documentation Index](./Documentation_Index.md) | [Next: Security & Privacy →](./security.md)
