# ⚡ NgodingYuk — Enterprise PRD & Layered Task Generator

<p align="center">
  <b>Generator Dokumen PRD dan Backlog Task Berfase untuk AI Coding Agent</b><br>
  <i>Terinspirasi dari alur kerja NgodingPakeAI (Frontend Mock First → Layered Checkpoint)</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Stack-Pure_HTML5_%2B_Tailwind-FF5C20?style=flat" alt="Stack">
  <img src="https://img.shields.io/badge/Target-Claude_Code_|_Hermes_|_Cursor-10B981?style=flat" alt="Target Agent">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat" alt="License">
</p>

---

## 📌 Mengapa NgodingYuk?

AI coding agent (seperti **Claude Code**, **Hermes Agent**, **Antigravity**, atau **Cursor**) sering kali mengalami masalah saat diberi instruksi umum:
1. **Halusinasi Skema:** Membuat tabel database dan endpoint tanpa kontrak yang jelas.
2. **Melompati Arsitektur:** Langsung mencoba membuat backend rumit sebelum tampilan layar divalidasi.
3. **Context Overflow & Regresi:** Kehilangan fokus karena memproses backlog ratusan baris sekaligus.

**NgodingYuk** menyelesaikan masalah ini dengan mengadopsi formula **4-Fase & Layered Checkpoint**:
- **Fase 1 (Frontend Stubs):** Membangun UI dan layout dengan *data mock/tiruan* terlebih dahulu. Developer bisa langsung klik-klik tampilan di browser sebelum menyentuh database.
- **Fase 2 (Client State):** Menghubungkan formulir, validasi Zod, dan manajemen state lokal di browser.
- **Fase 3 (Database & API):** Menyusun skema DDL SQL PostgreSQL resmi, migrasi ORM, autentikasi session, dan endpoint RESTful.
- **Fase 4 (Integrasi & Polish):** Menyambungkan frontend ke API nyata, audit keamanan, SEO, dan verifikasi production build.

---

## ✨ Fitur Utama

- 🚀 **Zero Dependency Hell:** Berjalan 100% menggunakan Python bawaan dan browser modern tanpa perlu `npm install` ratusan megabyte.
- 🎨 **Web App Interaktif:** Antarmuka modern (Dark Theme, font Plus Jakarta Sans) dengan 5 tab spesifikasi:
  - **Dokumen PRD Enriched:** Executive Summary, User Personas, Arsitektur 7 Lapisan, UI State Matrix, dan NFR.
  - **Skema Database & DDL:** Skema SQL PostgreSQL 16 lengkap dengan `UUID`, `ENUM`, `FOREIGN KEY ON DELETE CASCADE`, dan `INDEX`.
  - **Kontrak Spesifikasi API:** Tabel RESTful endpoints lengkap dengan query params, contoh JSON Request Body, dan Response 200 OK.
  - **Roadmap & Task Board:** 24 micro-tasks terstruktur dengan filter layer, penanda progres, dan tombol sekali klik **"Copy Prompt Agent"**.
  - **Petunjuk Agent (`AGENTS.md`):** Pedoman otonom dan aturan emas *anti-slop* untuk coding agent.
- 💻 **CLI Terminal Generator:** Perintah mandiri untuk menghasilkan file `PRD.md`, `TASKS.md`, `AGENTS.md`, dan `plan.json` ke folder proyek mana pun dalam 1 detik.
- ⚡ **Prinsip Ponytail (Minimal Code):** Menghasilkan panduan kode yang ringkas, mengutamakan native Web API dan pustaka standar (*boring over clever*).

---

## 🛠️ Prasyarat Sistem

- **Python:** Versi 3.8 atau lebih baru (`python --version`)
- **Web Browser:** Chrome, Edge, Firefox, Brave, atau Safari modern
- **Git:** Terpasang di sistem (`git --version`)

---

## 📦 Panduan Instalasi

Clone repository ini ke komputer lokal:

```bash
# 1. Clone repository
git clone https://github.com/NnoeeL/ngodingyuk.git

# 2. Masuk ke direktori
cd ngodingyuk
```

---

## 🎯 Cara Penggunaan

### Cara 1: Menggunakan Web App Interaktif (Paling Praktis)

Jalankan server lokal ringan (otomatis membuka browser di `http://localhost:3333`):

```bash
python serve.py
```

> **Tips:** Kamu juga bisa langsung membuka file `index.html` dengan klik ganda di File Explorer tanpa server.

**Langkah di Web App:**
1. Pilih salah satu **Preset Ide** (Kosan Finder, SaaS Finansial, Rental Outdoor, Forum Kampus) atau ketik ide aplikasimu sendiri.
2. Tentukan **Tech Stack** pilihan (TanStack Start + Drizzle, Next.js 15 + Prisma, atau Vite React + Express).
3. Klik tombol **"Generate PRD Komprehensif (24 Tasks)"**.
4. Buka tab **Roadmap & Task Board**, klik **"Copy Prompt Agent"** pada task yang ingin dikerjakan, dan tempelkan ke terminal AI coding agent kamu!
5. Unduh bundel dokumen lengkap dengan tombol **"Download PRD + Tasks (.md)"**.

---

### Cara 2: Menggunakan CLI Generator dari Terminal

Kamu bisa membuat seluruh dokumen spesifikasi langsung ke folder proyek target mana pun:

```bash
# Contoh untuk aplikasi pencarian kosan:
python cli.py "KosHunt" \
  --idea "Aplikasi pencarian kosan mahasiswa dekat kampus dengan filter radius 10km dan WhatsApp owner" \
  --stack tanstack \
  --output ./docs
```

**Pilihan Argumen CLI:**
- `name`: Nama aplikasi atau proyek (contoh: `"KosHunt"`, `"DuitTrack"`).
- `--idea`: Deskripsi masalah dan kebutuhan aplikasi.
- `--stack`: Pilihan tech stack (`tanstack` [default], `nextjs`, `vite-spa`).
- `--target`: Target audiens (default: `"Mahasiswa & Pengguna Umum"`).
- `--output`: Direktori tujuan penyimpanan file dokumen (default: `.` direktori aktif).

**File yang Dihasilkan:**
```text
output_dir/
├── PRD.md         # Dokumen spesifikasi rekayasa sistem (~300 baris)
├── TASKS.md       # 24 Micro-tasks berfase lengkap dengan prompt (~820 baris)
├── AGENTS.md      # Pedoman instruksi kerja untuk AI coding agent
└── plan.json      # Struktur skema data mentah JSON
```

---

## 🤖 Cara Kerja Bersama AI Coding Agent

Berikut cara terbaik memanfaatkan hasil generate **NgodingYuk** bersama agent (**Claude Code**, **Hermes**, **Antigravity**, atau **Cursor**):

1. **Letakkan Dokumen di Root Proyek:**
   Simpan `PRD.md`, `TASKS.md`, dan `AGENTS.md` di folder repository yang sedang kamu kembangkan.
2. **Instruksikan Agen Mengikuti AGENTS.md:**
   Agen diwajibkan membaca `AGENTS.md` untuk memahami protokol pengerjaan satu per satu dan larangan regresi.
3. **Eksekusi Bertahap (One Task at a Time):**
   Salin prompt task dari `TASKS.md` (misalnya `T-01` untuk inisialisasi layout). Minta agen mengerjakan hanya task tersebut:
   ```markdown
   Kamu akan mengerjakan task T-01 (Setup Repository & Layout Shell) untuk proyek ini.
   Layer: frontend | Fase: 1
   Selesaikan HANYA task ini dan lakukan verifikasi pengujian sebelum melapor selesai.
   ```
4. **Verifikasi Manusia di Akhir Tiap Fase:**
   Setelah Fase 1 selesai, buka browser dan coba navigasi aplikasinya. Jika tampilan sudah memuaskan, baru perintahkan agen lanjut ke Fase 2 dan Fase 3.

---

## 📂 Struktur Direktori Repository

```text
ngodingyuk/
├── index.html        # Aplikasi Web interaktif mandiri (UI generator & task board)
├── cli.py            # Generator CLI Python (Enterprise synthesis engine)
├── serve.py          # Server HTTP lokal otomatis membuka browser
├── preview.html      # Widget preview interaktif untuk chat agent
├── sample-enterprise # Contoh output dokumen PRD & TASKS lengkap
└── README.md         # Dokumentasi panduan ini
```

---

## 📄 Lisensi

Didistribusikan di bawah Lisensi **MIT**. Bebas digunakan untuk proyek personal, akademik, maupun komersial.

---

<p align="center">
  Dibuat dengan ❤️ untuk ekosistem AI Coding Agent oleh <a href="https://github.com/NnoeeL"><b>Muhammad Farrel (Noel)</b></a>
</p>