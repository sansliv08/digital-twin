# AI Digital Twin — Conversational Portfolio & LLM System

[![Demo](https://img.shields.io/badge/Live%20Demo-Coming%20Soon-blue)](#)
[![Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20Next.js%20%7C%20Docker%20%7C%20Coolify-0f172a)](#architecture--technical-decisions)

An interactive conversational assistant (*Digital Twin*) built to represent my professional profile, skills, and career background in a natural, context-aware conversation. Beyond a simple chatbot, this project was designed to demonstrate **applied LLM engineering**, dynamic context grounding, persistent session memory, and self-hosted deployment on private infrastructure.

## What This Project Demonstrates

* **Context Grounding & Prompt Engineering:** Combines structured and unstructured personal data (`facts.json`, `summary.txt`, `style.txt`, and a Markdown CV) into a dynamic system prompt enriched with real-time date/time context.
* **Guardrails & Reliability:** Explicit behavioral constraints in the system prompt to prevent hallucinations outside the provided context, resist prompt injection / jailbreak attempts, and maintain a professional tone.
* **Efficient Memory Management:** Conversation history persisted per `session_id` using a sliding window (last 10 messages) to balance conversational continuity, response latency, and token cost.
* **Containerized Full-Stack & Self-Hosted Infrastructure:** FastAPI backend and Next.js (`output: "standalone"`) frontend packaged with Docker and deployed with **Coolify**.

---

## Architecture & Technical Decisions

```text
twin/
├── backend/                # FastAPI API, dynamic prompt assembly, and memory management
│   ├── data/               # Knowledge base (Markdown CV, facts, summary, and style notes)
│   ├── context.py          # System prompt construction and behavioral guardrails
│   ├── resources.py        # Context file loader and text normalization
│   ├── server.py           # REST endpoints (/chat, /health, /conversation/{session_id})
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Production container (port 80)
├── frontend/               # Next.js web interface (App Router + TypeScript + Tailwind CSS)
│   ├── app/                # Application pages and routing
│   ├── components/         # UI and conversational chat components
│   ├── next.config.ts      # Configured with output: "standalone" for Docker builds
│   └── Dockerfile          # Optimized multi-stage production build (port 3000)
└── memory/                 # Local JSON session persistence (mounted via Docker volume)