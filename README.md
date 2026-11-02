# ⚡ BikinPlan — Enterprise PRD & Layered Task Generator

<p align="center">
  <b>Generator Dokumen PRD dan Backlog Task Berfase untuk AI Coding Agent</b><br>
  <i>Terinspirasi dari alur kerja NgodingPakeAI (Frontend Mock First → Layered Checkpoint)</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Release-v1.2.0-FF5C20?style=flat&logo=github" alt="Release">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Stack-Pure_HTML5_%2B_Tailwind-FF5C20?style=flat" alt="Stack">
  <img src="https://img.shields.io/badge/Target-Claude_Code_|_Hermes_|_Cursor-10B981?style=flat" alt="Target Agent">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat" alt="License">
</p>

---

## 📌 Mengapa BikinPlan?

AI coding agent (seperti **Claude Code**, **Hermes Agent**, **Antigravity**, atau **Cursor**) sering kali mengalami masalah saat diberi instruksi umum:
1. **Halusinasi Skema:** Membuat tabel database dan endpoint tanpa kontrak yang jelas.
2. **Melompati Arsitektur:** Langsung mencoba membuat backend rumit sebelum tampilan layar divalidasi.
3. **Context Overflow & Regresi:** Kehilangan fokus karena memproses backlog ratusan baris sekaligus.

**BikinPlan** menyelesaikan masalah ini dengan mengadopsi formula **4-Fase & Layered Checkpoint**:
- **Fase 1 (Frontend Stubs):** Membangun UI dan layout dengan *data mock/tiruan* terlebih dahulu. Developer bisa langsung klik-klik tampilan di browser sebelum menyentuh database.
- **Fase 2 (Client State):** Menghubungkan formulir, validasi Zod, dan manajemen state lokal di browser.
- **Fase 3 (Database & API):** Menyusun skema DDL SQL PostgreSQL resmi, migrasi ORM, autentikasi session, dan endpoint RESTful.
- **Fase 4 (Integrasi & Polish):** Menyambungkan frontend ke API nyata, audit keamanan, SEO, dan verifikasi production build.

---

## ✨ Fitur Utama

- 🚀 **Zero Dependency Hell:** Berjalan 100% menggunakan Python bawaan dan browser modern tanpa perlu `npm install` ratusan megabyte.
- ⚡ **Instant API Mock Server (Baru di v1.2):** Jalankan server mock RESTful lokal instan (`python cli.py mock` atau `python serve.py`) dengan dukungan CORS penuh (`Access-Control-Allow-Origin: *`) dan Dashboard Web Interaktif (`http://localhost:3333/__mock`). Frontend mock kamu bisa langsung memanggil `fetch('/api/...')` sebelum menyentuh database!
- 🏃 **Live Task Runner CLI (Baru di v1.2):** Jalankan task pengerjaan berurutan langsung dari terminal dengan `bikinplan next`. Otomatis menyalin prompt task aktif ke clipboard sistem (Windows `clip.exe`, macOS `pbcopy`, Linux) dan tandai selesai dengan `bikinplan complete T-01`.
- 📊 **Visual Diagram & ERD Client-Side (Baru di v1.2):** Tab khusus visualisasi ERD relasional tabel database dan flowchart arsitektur 4-fase berbasis Mermaid.js interaktif. Kode Mermaid siap disalin ke GitHub Markdown, Notion, atau Eraser.io.
- 🤖 **Ekosistem Multi-Agent Lengkap (Baru di v1.2):** Hasilkan konfigurasi aturan kerja siap pakai untuk berbagai coding agent:
  - `CLAUDE.md` — Khusus Anthropic Claude Code CLI.
  - `.cursorrules` & `.cursor/rules/architecture.mdc` — Khusus Cursor IDE Composer & Cursor Rules 2.0.
  - `AGENTS.md` — Untuk Hermes Agent, Antigravity, dan AI otonom lainnya.
- 🎨 **Web App Interaktif:** Antarmuka modern (Dark Theme, font Plus Jakarta Sans) dengan 6 tab spesifikasi:
  - **Dokumen PRD Enriched:** Executive Summary, User Personas, Arsitektur 7 Lapisan, UI State Matrix, dan NFR.
  - **Visual Diagram & ERD:** Diagram relasi entitas visual dan flowchart 4-fase.
  - **Skema Database & DDL:** Skema SQL PostgreSQL 16 lengkap dengan `UUID`, `ENUM`, `FOREIGN KEY ON DELETE CASCADE`, dan `INDEX`.
  - **Kontrak Spesifikasi API:** Tabel RESTful endpoints lengkap dengan query params, contoh JSON Request Body, dan Response 200 OK.
  - **Roadmap & Task Board:** 24 micro-tasks terstruktur dengan filter layer, penanda progres, dan tombol sekali klik **"Copy Prompt Agent"**.
  - **Rules Multi-Agent:** Tab konfigurasi multi-agent (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `architecture.mdc`).
- 💻 **CLI Terminal Generator:** Perintah mandiri untuk menghasilkan seluruh berkas spesifikasi dan rules ke folder proyek mana pun dalam 1 detik.
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
git clone https://github.com/NnoeeL/BikinPlan.git

# 2. Masuk ke direktori
cd BikinPlan
```

---

## 🎯 Cara Penggunaan

### Cara 1: Menggunakan Web App Interaktif (Paling Praktis)

Jalankan server lokal ringan (otomatis membuka browser di `http://localhost:3333`):

```bash
python serve.py
```

> **Tips:** Kamu juga bisa langsung membuka file `index.html` dengan klik ganda di File Explorer tanpa server.

**Alur Cerdas di Web App:**
1. **Langkah 1 (Ide, Preset & AI Refine):**
   - Pilih dari **5 Blueprint Presets:** 🛍️ *Katalog Toko*, 💼 *Portofolio*, 🎓 *PWA Kampus*, ⚡ *MicroSaaS*, atau 📊 *Admin Dashboard*.
   - **Mode "Refine with AI":** Klik tombol *🚀 Analisis Sekarang* untuk mendeteksi potensi edge cases, validasi celah input, dan skenario gagal sebelum generate dokumen. Mendukung Google Gemini Flash, Groq Llama 3.3 (gratis tanpa kartu kredit), serta built-in offline rule engine.
   - Klik *Lanjut: Analisis Stack & Rekomendasi*.
2. **Langkah 2 (Rekomendasi Arsitektur):** Sistem otomatis menganalisis ide dan menampilkan rekomendasi **Tech Stack** & **Sistem Autentikasi** terbaik lengkap dengan kotak penjelasan teknis (*"Mengapa ini direkomendasikan untuk idemu?"*). Kamu dapat menyetujui rekomendasi atau memilih opsi alternatif.
3. **Hasil (PRD, ERD Diagram & 24 Tasks Board):** Klik *Setuju & Generate* — seluruh dokumen siap disalin atau diunduh dalam format **Bundle .ZIP** (otomatis memuat `PRD.md`, `TASKS.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules/architecture.mdc`, dan `plan.json`).

---

### Cara 2: Menggunakan CLI Generator dari Terminal

Kamu bisa membuat seluruh dokumen spesifikasi langsung ke folder proyek target mana pun:

```bash
# Contoh menggunakan blueprint preset kampus:
python cli.py --preset campus --output ./docs

# Atau dengan ide bebas + auto-refine edge cases:
python cli.py "KosHunt" \
  --idea "Aplikasi pencarian kosan mahasiswa dekat kampus dengan filter radius 10km dan WhatsApp owner" \
  --refine \
  --stack tanstack \
  --output ./docs
```

**Pilihan Argumen CLI:**
- `name`: Nama aplikasi atau proyek (contoh: `"KosHunt"`, `"DuitTrack"`).
- `--preset`: Pilihan blueprint siap pakai (`toko`, `portfolio`, `campus`, `saas`, `dashboard`).
- `--refine`: Otomatis menganalisis dan melampirkan aturan edge cases arsitektur.
- `--idea`: Deskripsi masalah dan kebutuhan aplikasi.
- `--stack`: Pilihan tech stack (`tanstack` [default], `nextjs`, `vite-spa`).
- `--target`: Target audiens (default: `"Mahasiswa & Pengguna Umum"`).
- `--output`: Direktori tujuan penyimpanan file dokumen (default: `.` direktori aktif).

---

### Cara 3: Menggunakan Fitur Cepat (One-Prompt Autonomous Mode) ⚡

Cara paling praktis: biarkan AI Agent membaca semua berkas dan mengeksekusi seluruh 24 task berfase secara mandiri dari awal sampai selesai:

```bash
# Otomatis salin One-Prompt Otonom ke clipboard:
python cli.py prompt
# atau:
./bikinplan prompt
```
1. Buat folder proyek (`mkdir my-app && cd my-app`) dan pindahkan berkas bundle ZIP ke dalamnya.
2. Buka Claude Code, Hermes Agent, Antigravity, atau Cursor di terminal folder tersebut.
3. Tekan **Ctrl+V** untuk menempelkan One-Prompt Otonom. Agent akan langsung membaca `PRD.md`, `TASKS.md`, `AGENTS.md`, dan mengeksekusi project sampai tuntas!

---

### Cara 4: Menjalankan Task Runner Bertahap (`bikinplan next`)

Gunakan jika kamu ingin mengevaluasi hasil pengerjaan agent satu per satu:

```bash
# 1. Ambil task aktif berikutnya & otomatis salin prompt ke clipboard:
python cli.py next
# atau:
./bikinplan next

# 2. Cek ringkasan progres 24 task dan 4 fase:
./bikinplan status

# 3. Tandai task selesai setelah agent lulus kriteria pengujian:
./bikinplan complete T-01
```

---

### Cara 5: Menjalankan Instant API Mock Server (`bikinplan mock`)

Frontend Mock First: Jalankan mock server lokal tanpa perlu membuat tabel database atau server backend:

```bash
# Jalankan mock server membaca plan.json aktif:
python cli.py mock
# atau:
python serve.py
```
- 🌐 **Dashboard Mock Interaktif:** Buka `http://localhost:3333/__mock` untuk melihat rute dan mencoba request API langsung dari browser.
- 🔗 **CORS Siap Pakai:** Frontend kamu di `http://localhost:5173` (Vite) atau `http://localhost:3000` (Next.js) bisa langsung memanggil `fetch('http://localhost:3333/api/...')` tanpa kendala CORS.

---

### Cara 6: Ekspor Aturan Multi-Agent (`bikinplan export-rules`)

Ekspor instan seluruh berkas konfigurasi agent ke proyek mana pun:

```bash
# Ekspor AGENTS.md, CLAUDE.md, .cursorrules, dan architecture.mdc:
python cli.py export-rules ./my-project
# atau:
./bikinplan export-rules ./my-project
```

**File Lengkap yang Dihasilkan:**
```text
output_dir/
├── PRD.md                       # Dokumen spesifikasi rekayasa sistem + Mermaid ERD
├── TASKS.md                     # 24 Micro-tasks berfase lengkap dengan prompt (~820 baris)
├── AGENTS.md                    # Pedoman instruksi kerja umum & Hermes Agent
├── CLAUDE.md                    # Panduan kerja resmi Anthropic Claude Code CLI
├── .cursorrules                 # Aturan kerja Cursor IDE Composer
├── .cursor/rules/
│   └── architecture.mdc         # Konfigurasi Cursor Rules 2.0 (MDC Engine)
├── plan.json                    # Struktur skema data mentah JSON
└── <proyek>-specs.zip           # Bundle ZIP multi-agent lengkap siap ekstrak
```

---

## 🧭 Tutorial Langkah Awal: Cara & Kapan Mengirim File ke AI Agent

Banyak pemula bingung: *kapan harus mengirim PRD? Kapan harus menyuruh agent coding?* Ikuti 4 langkah terstruktur ini agar coding agent bekerja rapi tanpa merusak arsitektur kodemu:

### 1. Langkah Paling Awal: Siapkan Folder Proyek
Sebelum membuka AI Agent apa pun, buat folder kosong baru di komputermu:
```bash
mkdir toko-online && cd toko-online
```
Setelah men-generate dokumen di BikinPlan (lewat Web App atau CLI), pindahkan 3 file hasil generate ke dalam root folder proyek tersebut:
- `PRD.md` — Spesifikasi lengkap arsitektur, DDL database, dan kontrak API.
- `TASKS.md` — Daftar 24 micro-tasks berfase yang memandu pengerjaan harian.
- `AGENTS.md` — Instruksi dan aturan main agar agent tidak membuat kode berantakan (*anti-slop*).

---

### 2. Kapan Mengirim File PRD dan AGENTS.md? (First Handshake)
> ⏱️ **Kapan?** **DI PERCAKAPAN PERTAMA KALI**, tepat saat kamu baru membuka Claude Code, Hermes Agent, Antigravity, atau Cursor di terminal folder tersebut.

**PENTING:** Jangan langsung menyuruh agent membuat kode atau database! Kirimkan prompt pembuka (*handshake*) berikut:
```markdown
Baca PRD.md dan AGENTS.md di folder ini sebagai acuan arsitektur dan batasan pengerjaan.
Pahami alur 4 fase (Fase 1 Frontend Mockup -> Fase 2 State -> Fase 3 Database & API -> Fase 4 Integrasi).
DILARANG membuat tabel database, API rumit, atau menulis kode fitur sebelum saya memberikan nomor task spesifik.
Apakah kamu sudah membaca dan paham arsitekturnya?
```
💡 *Tujuan:* Membangun peta arsitektur di memori AI terlebih dahulu sebelum ia mulai menyentuh kode.

---

### 3. Kapan & Bagaimana Mengirim Task? (Satu per Satu)
Setelah AI Agent menjawab *"Paham"*, mulailah siklus pengerjaan bertahap:
1. Buka tab **"Roadmap & 24 Tasks Board"** di BikinPlan (atau buka file `TASKS.md`).
2. Mulai dari task pertama yang belum selesai (`T-01`: Setup Repo & Layout Shell).
3. Klik tombol **"Copy Prompt Agent"** pada task tersebut, lalu tempelkan ke terminal agent:
   ```markdown
   Kamu akan mengerjakan task T-01 (Inisialisasi Project, Layout Shell, dan Token Tema) untuk proyek ini.
   Layer: frontend | Fase: 1
   Selesaikan HANYA task ini dan lakukan verifikasi pengujian sebelum melapor selesai.
   ```
4. Agent akan fokus mengerjakan checklist task tersebut dan melakukan tes verifikasi sebelum melapor selesai.

---

### 4. Checkpoint Verifikasi Manusia (Wajib Uji Tampilan di Browser!)
> ⛔ **Kapan harus berhenti?** **Setiap kali berganti fase atau layer!**

Sesuai formula *Frontend Mock First*, Fase 1 (T-01 s/d T-06) sengaja menggunakan data tiruan (*mock*):
1. Setelah Fase 1 selesai, jalankan dev server (`npm run dev`) dan **buka browser**.
2. Klik-klik tombol, navigasi, dan filter tampilan di browser.
3. **Jika tampilan sudah disetujui**, barulah perintahkan agent untuk lanjut ke Fase 2 (state) dan Fase 3 (database).
4. **Keuntungan:** Kamu tidak membuang kuota/token untuk backend yang salah arah, dan tampilan UI sudah terbukti berfungsi sejak awal!

### 5. Cara Instan: Master Prompt (Sekali Paste Langsung Jadi!)
Jika kamu **tidak ingin repot mengirim file AGENTS.md atau memecah file terpisah**, BikinPlan menyediakan **Master Prompt**:
1. Setelah dokumen selesai digenerate, klik tombol **"Salin Master Prompt Sekarang"**.
2. Buka AI Coding Agent kamu di folder proyek baru.
3. Tempelkan Master Prompt tersebut. Agent akan langsung memahami konteks arsitektur dan langsung mengeksekusi langkah awal secara mandiri!

---


---

## 📂 Struktur Direktori Repository

```text
BikinPlan/
├── index.html               # Aplikasi Web interaktif mandiri (UI generator, ERD & task board)
├── cli.py                   # Generator CLI & Task Runner (Enterprise synthesis engine)
├── agent_config_generator.py# Multi-agent rules (Claude, Cursor, Hermes) & Mermaid ERD
├── mock_server.py           # Zero-dependency Instant API Mock Server & Dashboard
├── task_runner.py           # Live task tracker & auto clipboard engine
├── serve.py                 # Server HTTP lokal dengan integrasi Web & Mock API
├── bikinplan                # Bash executable shortcut untuk Unix/Mac/Git Bash
├── bikinplan.bat            # Batch executable shortcut untuk Windows CMD/PowerShell
├── preview.html             # Widget preview interaktif untuk chat agent
├── sample-enterprise        # Contoh output dokumen PRD & TASKS lengkap
└── README.md                # Dokumentasi panduan ini
```

---

## 📄 Lisensi

Didistribusikan di bawah Lisensi **MIT**. Bebas digunakan untuk proyek personal, akademik, maupun komersial.

---

<p align="center">
  Dibuat dengan ❤️ untuk ekosistem AI Coding Agent oleh <a href="https://github.com/NnoeeL"><b>Muhammad Farrel (Noel)</b></a>
</p>