# AGENTS.md — Instruksi Kerja AI Coding Agent

Proyek: **KosHunt**  
Kategori: **Marketplace, Rental & Booking Engine**  
Tech Stack: **TanStack Start + Drizzle ORM + PostgreSQL**  

---

## 1. Aturan Emas Pengerjaan (Golden Rules)
1. **Satu Task Per Giliran:**
   Buka file `TASKS.md`. Cari task pertama yang belum bertanda `[x]`. Kerjakan HANYA task tersebut sampai lolos kriteria verifikasi penerimaan.
2. **Patuhi Fase & Lapisan (Layering Protocol):**
   - **Fase 1 (Frontend Stubs):** DILARANG membuat tabel database atau server functions rumit. Selesaikan layout dan komponen presentasi dengan mock data terlebih dahulu agar pengguna dapat menguji tampilan di browser.
   - **Fase 2 (Client State):** Sambungkan form dan state lokal (optimistic UI).
   - **Fase 3 (Database & Backend):** Tulis skema DDL, migration script, auth guard, dan controller API.
   - **Fase 4 (Integrasi):** Hubungkan frontend ke backend nyata dan pastikan production build lolos.
3. **Checkpoint Verifikasi:**
   Setiap kali berganti layer (misal dari `frontend` ke `backend`) atau berganti fase, kamu WAJIB berhenti dan meminta konfirmasi pengguna:
   > *"✅ Fase 1 (Frontend Mockup) selesai. Semua layar sudah dapat diklik di browser. Boleh lanjut ke Fase 2?"*
4. **Prinsip Ponytail (Minimal Code):**
   - Kode terbaik adalah kode yang tidak perlu ditulis.
   - Gunakan fitur native Web API dan pustaka standar bahasa.
   - Dilarang membuat boilerplate atau abstraksi yang tidak diminta secara eksplisit.
   - Dilarang menambahkan komentar AI generic (*slop*) dalam kode.

---

## 2. Struktur Proyek Acuan
```text
├── src/
│   ├── app/                # Halaman dan rute aplikasi
│   ├── components/         # Komponen UI modular (< 250 baris per file)
│   │   ├── layout/         # Header, Navbar, ThemeToggle
│   │   ├── ui/             # Modal, Toast, Button, Input
│   │   └── domain/         # Kartu dan komponen spesifik domain
│   ├── data/               # Fixture mock data (Fase 1)
│   ├── db/                 # Skema DDL Drizzle/Prisma & Seed script (Fase 3)
│   ├── hooks/              # Custom hooks & TanStack Query hooks
│   ├── routes/api/         # Controller & Endpoint API
│   ├── schemas/            # Skema validasi Zod
│   └── styles/             # Tailwind CSS tokens
├── AGENTS.md               # Instruksi ini
├── PRD.md                  # Spesifikasi lengkap produk
└── TASKS.md                # 24 Micro-tasks berfase
```
