#!/usr/bin/env python3
"""
BikinPlan Multi-Agent & Visual Diagram Generator
Menghasilkan:
1. Konfigurasi Agen Multi-Platform (CLAUDE.md, .cursorrules, .cursor/rules/architecture.mdc)
2. Diagram Visual ERD & Flowchart 4-Fase berbasis Mermaid.js
Prinsip: Ponytail (minimal code, stdlib only, type-safe, runnable verification).
"""

import re
from typing import Dict, Any

def parse_ddl_to_mermaid(sql: str) -> str:
    """Mem-parse PostgreSQL DDL menjadi kode Mermaid erDiagram yang valid."""
    lines = sql.splitlines()
    tables = {}
    relations = []
    current_table = None

    table_re = re.compile(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z0-9_]+)', re.IGNORECASE)
    ref_re = re.compile(r'REFERENCES\s+([a-zA-Z0-9_]+)\s*\(([a-zA-Z0-9_]+)\)', re.IGNORECASE)
    pk_re = re.compile(r'\bPRIMARY\s+KEY\b', re.IGNORECASE)

    for line in lines:
        t_match = table_re.search(line)
        if t_match:
            current_table = t_match.group(1).lower()
            tables[current_table] = []
            continue

        if current_table:
            clean = line.strip().rstrip(',')
            if clean.startswith(')') or clean.startswith(');'):
                current_table = None
                continue
            if clean.startswith('--') or not clean:
                continue

            ref_match = ref_re.search(clean)
            if ref_match:
                parent = ref_match.group(1).lower()
                relations.append(f'    {parent} ||--o{{ {current_table} : "relates_to"')

            parts = clean.split()
            if len(parts) >= 2:
                col_name = parts[0].strip('"`')
                if col_name.upper() in ['CONSTRAINT', 'UNIQUE', 'CHECK', 'FOREIGN', 'PRIMARY']:
                    continue
                col_type = parts[1].split('(')[0].lower()
                is_pk = bool(pk_re.search(clean))
                tag = ' PK' if is_pk else (' FK' if ref_match else '')
                tables[current_table].append((col_type, col_name, tag))

    mermaid = ['erDiagram']
    for rel in sorted(set(relations)):
        mermaid.append(rel)
    for t_name, cols in tables.items():
        mermaid.append(f'    {t_name} {{')
        for c_type, c_name, tag in cols[:12]:
            mermaid.append(f'        {c_type} {c_name}{tag}')
        mermaid.append('    }')
    return '\n'.join(mermaid)

def generate_mermaid_flowchart(plan: Dict[str, Any]) -> str:
    """Menghasilkan diagram alur kerja 4-fase BikinPlan menggunakan Mermaid flowchart."""
    return """flowchart TD
    subgraph F1 [Fase 1: Frontend Mockup & Stubs]
        F1_A[Inisialisasi Project & Design Tokens] --> F1_B[Layout Shell: Navbar & Dark Mode]
        F1_B --> F1_C[UI Components & Data Mock Tiruan]
        F1_C --> F1_Check{"Checkpoint: Validasi Tampilan di Browser"}
    end

    subgraph F2 [Fase 2: Client State & Validation]
        F1_Check -->|UI Disetujui| F2_A[Formulir Interaktif & Modal Dialog]
        F2_A --> F2_B[Validasi Skema Zod Input]
        F2_B --> F2_C[State URL Query & Local Storage Cache]
        F2_C --> F2_Check{"Checkpoint: Validasi Interaksi Form"}
    end

    subgraph F3 [Fase 3: Database DDL & Backend API]
        F2_Check -->|Interaksi Disetujui| F3_A[Skema Database DDL PostgreSQL]
        F3_A --> F3_B[Autentikasi Session & Role Guard]
        F3_B --> F3_C[Kontrak Endpoint RESTful API]
        F3_C --> F3_Check{"Checkpoint: Uji Endpoint Mock/Real API"}
    end

    subgraph F4 [Fase 4: Integrasi End-to-End & Polish]
        F3_Check -->|API Disetujui| F4_A[Wiring Frontend ke API Riil]
        F4_A --> F4_B[Audit Keamanan & Sanitasi Input]
        F4_B --> F4_C[Optimasi SEO, PWA & Production Build]
    end

    style F1 fill:#121722,stroke:#3b82f6,stroke-width:2px,color:#fff
    style F2 fill:#121722,stroke:#10b981,stroke-width:2px,color:#fff
    style F3 fill:#121722,stroke:#f59e0b,stroke-width:2px,color:#fff
    style F4 fill:#121722,stroke:#ec4899,stroke-width:2px,color:#fff"""

def generate_claude_markdown(plan: Dict[str, Any]) -> str:
    """Menghasilkan file CLAUDE.md khusus untuk Claude Code CLI."""
    p = plan
    s = p.get("stack", {})
    return f"""# CLAUDE.md — Panduan Kerja Claude Code CLI

Panduan resmi Claude Code CLI untuk proyek **{p['name']}** ({p['categoryTitle']}).

## 🛠️ Perintah Utama Proyek
- **Dev Server:** `npm run dev`
- **Lint & Format:** `npm run lint` && `npm run format`
- **Type Check:** `npm run type-check` (atau `npx tsc --noEmit`)
- **Production Build:** `npm run build`
- **Task Runner BikinPlan:** `python cli.py next` (atau `bikinplan next`)
- **Tandai Task Selesai:** `python cli.py complete <TASK_REF>`
- **Mock API Server:** `python cli.py mock` (atau `python serve.py`)

## ⚡ Prinsip Ponytail (Minimal Code & Anti-Slop)
1. **Kode Minimal:** Tulis kode sesedikit mungkin yang bekerja dengan benar ("boring over clever").
2. **Standard Library & Native First:** Utamakan Web API native browser dan library yang sudah ada. Jangan menambah package baru jika tidak diminta eksplisit.
3. **No AI Slop:** Dilarang menambahkan komentar basa-basi seperti `// handle user click`, `// this function does...`. Tulis kode yang self-explanatory.
4. **Verifikasi Mandiri:** Wajib menyertakan minimal 1 uji verifikasi sebelum melaporkan task selesai.

## 🧭 Metodologi 4-Fase (Frontend Mock First)
1. **Fase 1 (Frontend Mockup):** Gunakan data tiruan (mock fixture). DILARANG membuat tabel DB atau API server functions sebelum UI divalidasi pengguna di browser!
2. **Fase 2 (Client State):** Hubungkan validasi Zod dan manipulasi state lokal di browser.
3. **Fase 3 (Database & API):** Buat skema DDL PostgreSQL, autentikasi session, dan RESTful endpoints.
4. **Fase 4 (Integrasi & Polish):** Sambungkan frontend ke API nyata dan uji build produksi.

## 📋 Eksekusi Task
Buka `TASKS.md` atau jalankan `python cli.py next`. Kerjakan HANYA satu task aktif per putaran prompt.
"""

def generate_cursor_rules(plan: Dict[str, Any]) -> str:
    """Menghasilkan file .cursorrules untuk Cursor IDE Composer & Agent."""
    p = plan
    s = p.get("stack", {})
    return f"""# .cursorrules — Aturan Kerja Cursor IDE

You are an expert full-stack engineer working on {p['name']}.
Category: {p['categoryTitle']} | Stack: {s.get('name', 'Modern Stack')}

## Golden Rules
1. **Follow TASKS.md Step-by-Step:**
   Always inspect TASKS.md. Work strictly on the current active task. Do not jump ahead to future tasks or unapproved features.

2. **Frontend Mock First Rule:**
   Do NOT generate database tables, ORM migrations, or backend API routes during Phase 1 and 2. Use mock fixture data until the user approves the UI in the browser.

3. **Ponytail Principle (Minimalist Code):**
   - The best code is no code. Write the minimal clean implementation that solves the problem.
   - Rely on native browser Web APIs and existing dependencies.
   - No unnecessary abstraction layers, no premature optimizations, no AI boilerplate comments.

4. **Strict Type Safety:**
   - Always validate inputs at trust boundaries using Zod.
   - Keep TypeScript strict without using 'any'.
"""

def generate_cursor_mdc(plan: Dict[str, Any]) -> str:
    """Menghasilkan file .cursor/rules/architecture.mdc untuk Cursor Rules 2.0."""
    p = plan
    s = p.get("stack", {})
    return f"""---
description: Architecture rules, phase checkpoints, and minimal-code standards for {p['name']}
globs: src/**/*.{{ts,tsx,js,jsx}}, db/**/*, routes/**/*
alwaysApply: true
---

# Architecture & Engineering Guidelines: {p['name']}

## Project Context
- **Name:** {p['name']}
- **Category:** {p['categoryTitle']}
- **Target Audience:** {p.get('targetAudience', 'Mahasiswa & Umum')}
- **Stack:** {s.get('name', 'Modern Stack')}

## Mandatory Phased Checkpoints
1. **Phase 1 (Frontend Stubs):** Mock data only. User must verify layout in browser before Phase 2.
2. **Phase 2 (Client State):** Forms, Zod schemas, URL search params.
3. **Phase 3 (DB & API):** PostgreSQL DDL, Better-Auth / JWT sessions, REST contracts.
4. **Phase 4 (End-to-End):** Wiring TanStack Query to real endpoints, security audit, production build.

## Code Standards
- Adhere strictly to the **Ponytail principle** (minimal code, zero-slop).
- Follow schemas in `PRD.md` and active task in `TASKS.md`.
"""

def generate_one_prompt(plan: Dict[str, Any]) -> str:
    """Menghasilkan Autonomous Master Prompt v2 (One-Prompt All-Done Loop Protocol)."""
    p = plan
    return f"""Kamu adalah Principal Fullstack Engineer yang bertindak sebagai Autonomous Implementation Agent. Kamu ditugaskan membangun aplikasi "{p['name']}" dari awal sampai selesai berdasarkan berkas spesifikasi di folder ini:
1. `PRD.md` — Spesifikasi produk, arsitektur, DDL PostgreSQL, kontrak API, dan blueprint struktur file.
2. `TASKS.md` — 24 micro-tasks berfase dengan checklist eksekusi dan kriteria acceptance test.
3. `AGENTS.md` & `CLAUDE.md` — Aturan main anti-slop, konvensi kode, dan prinsip Ponytail.

PROTOKOL EKSEKUSI OTONOM MANDIRI (AUTONOMOUS EXECUTION LOOP):
Lakukan pengerjaan secara mandiri dan berurutan mengikuti siklus loop berikut:

1. BACA & INTERNALISASI:
   Baca seluruh `PRD.md`, `TASKS.md`, dan `AGENTS.md`. Pahami pembagian 4 Fase:
   - FASE 1: Fondasi, Layout Shell & Mockup UI Statis (Wajib menggunakan data tiruan mock-fixtures dari PRD.md).
   - FASE 2: Client State, Validasi Zod & Form Interaktif.
   - FASE 3: Database DDL PostgreSQL, Session Auth & RESTful API Endpoints.
   - FASE 4: Integrasi End-to-End, Hardening Trust Boundary & Production Build.

2. ATURAN EMAS "FRONTEND MOCK FIRST":
   DILARANG KERAS membuat tabel database, migrasi ORM, atau server functions rumit pada Fase 1 dan Fase 2! Selesaikan seluruh layar antarmuka dengan data tiruan terlebih dahulu agar pengguna dapat menguji tampilan di browser.

3. SIKLUS LOOP TASK (T-01 s/d T-24):
   Kerjakan task satu per satu secara berurutan:
   - Ambil task pertama yang belum selesai (belum bertanda `[x]`).
   - Implementasikan HANYA checklist pada task tersebut sesuai file blueprint di PRD.md.
   - Jalankan verifikasi penerimaan (misal `npm run type-check` atau verifikasi logika).
   - Setelah lolos, ubah status checklist task tersebut di `TASKS.md` menjadi `[x]`.
   - Lanjutkan otomatis ke task berikutnya tanpa berhenti meminta izin per task.

4. CHECKPOINT VERIFIKASI FASE:
   Ketika Fase 1 & 2 selesai, jalankan dev server (`npm run dev`) dan laporkan:
   "✅ Fase 1 & 2 selesai. Seluruh layar antarmuka sudah dapat diklik di browser. Silakan inspeksi UI sebelum saya lanjut ke Fase 3 (Database & API)."

5. PRINSIP PONYTAIL (KODE MINIMAL):
   Tulis kode sesedikit mungkin yang bekerja dengan benar ("boring over clever"). Gunakan native Web API dan pustaka standar. Jangan menambahkan komentar basa-basi AI slop.

Mulai sekarang: baca seluruh berkas spesifikasi di folder ini, konfirmasi pemahamanmu secara ringkas, dan LANGSUNG MULAI kerjakan Task T-01!"""

