# Task Backlog: KosHunt

> **Total Task:** 24 Micro-Tasks Terstruktur  
> **Metodologi:** 4 Fase Pengerjaan (Fase 1 Mockup UI -> Fase 2 State Interaktif -> Fase 3 Database & API -> Fase 4 Integrasi & Polish)

Panduan AI Coding Agent: Kerjakan task secara berurutan. Berhenti di checkpoint akhir setiap fase untuk konfirmasi pengguna.

---


## FASE 1 — FONDASI, LAYOUT, & MOCKUP UI STATIS (Layer: Frontend)
*Tujuan: Membangun seluruh tampilan visual dengan data tiruan agar dapat langsung diklik-klik di browser.*
### [T-01] Setup Repository, Standarisasi TypeScript, dan Konfigurasi Tailwind Tokens
- **Layer:** `frontend` | **Fase:** `1`
- **Objektif:** Inisialisasi repo dengan konfigurasi TypeScript ketat, Tailwind CSS design tokens (warna primer, neutral, card, border), dan linter rules.
- **File Terkait:** `package.json`, `tailwind.config.ts`, `tsconfig.json`, `src/styles/globals.css`
- **Checklist Eksekusi:**
  - [ ] Inisialisasi project sesuai tech stack pilihan
  - [ ] Konfigurasi tailwind.config.ts dengan palet warna dan font 'Plus Jakarta Sans'
  - [ ] Tambahkan skrip lint, type-check, dan format di package.json
  - [ ] Verifikasi build awal berjalan lancar tanpa error type
- **Verifikasi Penerimaan (Acceptance Test):** Jalankan `npm run build` dan `npm run lint`. Keduanya berhasil 100% tanpa warning/error.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-01 (Setup Repository, Standarisasi TypeScript, dan Konfigurasi Tailwind Tokens) untuk proyek KosHunt.
Layer: frontend | Fase: 1

Objektif:
Inisialisasi repo dengan konfigurasi TypeScript ketat, Tailwind CSS design tokens (warna primer, neutral, card, border), dan linter rules.

Checklist Pengerjaan:
- Inisialisasi project sesuai tech stack pilihan
- Konfigurasi tailwind.config.ts dengan palet warna dan font 'Plus Jakarta Sans'
- Tambahkan skrip lint, type-check, dan format di package.json
- Verifikasi build awal berjalan lancar tanpa error type

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Jalankan `npm run build` dan `npm run lint`. Keduanya berhasil 100% tanpa warning/error.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-02] Layout Shell Responsif: Navbar, Sidebar, dan Dark/Light Mode Switcher
- **Layer:** `frontend` | **Fase:** `1`
- **Objektif:** Bangun tata letak aplikasi dengan navigasi responsif (desktop bar & mobile drawer) serta toggle tema dengan penyimpanan localStorage.
- **File Terkait:** `src/components/layout/Header.tsx`, `src/components/layout/ThemeToggle.tsx`, `src/components/layout/AppShell.tsx`
- **Checklist Eksekusi:**
  - [ ] Buat komponen Header dengan logo SVG dan menu navigasi
  - [ ] Buat navigasi mobile drawer yang mulus saat dibuka pada layar kecil
  - [ ] Implementasikan dark mode switcher dengan deteksi prefers-color-scheme sistem
  - [ ] Pasang layout wrapper utama yang membatasi max-width konten 1200px
- **Verifikasi Penerimaan (Acceptance Test):** Buka browser pada resolusi desktop dan mobile (F12 mobile view). Tampilan proporsional, tema tersimpan saat refresh.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-02 (Layout Shell Responsif: Navbar, Sidebar, dan Dark/Light Mode Switcher) untuk proyek KosHunt.
Layer: frontend | Fase: 1

Objektif:
Bangun tata letak aplikasi dengan navigasi responsif (desktop bar & mobile drawer) serta toggle tema dengan penyimpanan localStorage.

Checklist Pengerjaan:
- Buat komponen Header dengan logo SVG dan menu navigasi
- Buat navigasi mobile drawer yang mulus saat dibuka pada layar kecil
- Implementasikan dark mode switcher dengan deteksi prefers-color-scheme sistem
- Pasang layout wrapper utama yang membatasi max-width konten 1200px

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Buka browser pada resolusi desktop dan mobile (F12 mobile view). Tampilan proporsional, tema tersimpan saat refresh.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-03] Pembuatan Fixture Mock Data & State Tiruan untuk Katalog Interaktif, Pencarian Fuzzy & Filtering Lanjutan
- **Layer:** `frontend` | **Fase:** `1`
- **Objektif:** Tulis data tiruan realistis dalam file terisolasi untuk merepresentasikan entitas utama tanpa ketergantungan koneksi backend.
- **File Terkait:** `src/types/domain.ts`, `src/data/mockFixtures.ts`
- **Checklist Eksekusi:**
  - [ ] Definisikan TypeScript interface untuk entitas utama
  - [ ] Buat minimal 8 baris mock data realistis mencakup berbagai variasi status
  - [ ] Buat helper fungsi tiruan pencarian dan filter lokal di memori
- **Verifikasi Penerimaan (Acceptance Test):** Impor fixture ke unit test atau console: data tervalidasi sesuai tipe TypeScript.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-03 (Pembuatan Fixture Mock Data & State Tiruan untuk Katalog Interaktif, Pencarian Fuzzy & Filtering Lanjutan) untuk proyek KosHunt.
Layer: frontend | Fase: 1

Objektif:
Tulis data tiruan realistis dalam file terisolasi untuk merepresentasikan entitas utama tanpa ketergantungan koneksi backend.

Checklist Pengerjaan:
- Definisikan TypeScript interface untuk entitas utama
- Buat minimal 8 baris mock data realistis mencakup berbagai variasi status
- Buat helper fungsi tiruan pencarian dan filter lokal di memori

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Impor fixture ke unit test atau console: data tervalidasi sesuai tipe TypeScript.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-04] Tampilan Halaman Utama Katalog Interaktif, Pencarian Fuzzy & Filtering Lanjutan Berbasis Data Mock
- **Layer:** `frontend` | **Fase:** `1`
- **Objektif:** Buat komponen presentasi kartu/tabel dengan search input, filter pill kategori, dan status indikator menggunakan mock data.
- **File Terkait:** `src/pages/CatalogPage.tsx`, `src/components/catalog/ItemCard.tsx`, `src/components/catalog/ItemSkeleton.tsx`
- **Checklist Eksekusi:**
  - [ ] Buat komponen Card / Grid item yang menarik dan responsif
  - [ ] Pasang input pencarian dengan debounce 300ms
  - [ ] Tambahkan tombol filter kategori visual
  - [ ] Pasang komponen Shimmer Skeleton placeholder saat transisi
- **Verifikasi Penerimaan (Acceptance Test):** Buka halaman di browser: kartu produk/item muncul instan. Mengetik di search bar memfilter item secara langsung.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-04 (Tampilan Halaman Utama Katalog Interaktif, Pencarian Fuzzy & Filtering Lanjutan Berbasis Data Mock) untuk proyek KosHunt.
Layer: frontend | Fase: 1

Objektif:
Buat komponen presentasi kartu/tabel dengan search input, filter pill kategori, dan status indikator menggunakan mock data.

Checklist Pengerjaan:
- Buat komponen Card / Grid item yang menarik dan responsif
- Pasang input pencarian dengan debounce 300ms
- Tambahkan tombol filter kategori visual
- Pasang komponen Shimmer Skeleton placeholder saat transisi

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Buka halaman di browser: kartu produk/item muncul instan. Mengetik di search bar memfilter item secara langsung.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-05] Tampilan Halaman Rincian untuk Halaman Detail Item, Galeri Gambar & Kalender Ketersediaan (Detail View)
- **Layer:** `frontend` | **Fase:** `1`
- **Objektif:** Bangun halaman detail item dengan galeri preview, rincian spesifikasi, kalkulasi ringkas biaya, dan tombol aksi pemesanan.
- **File Terkait:** `src/pages/ItemDetailPage.tsx`, `src/components/detail/PriceSummaryCard.tsx`
- **Checklist Eksekusi:**
  - [ ] Buat halaman detail dinamis dengan routing slug/id
  - [ ] Tampilkan spesifikasi, fasilitas, dan status ketersediaan
  - [ ] Buat komponen ringkasan harga dan tombol call-to-action (CTA)
- **Verifikasi Penerimaan (Acceptance Test):** Klik salah satu item dari halaman utama: browser berpindah ke halaman detail dengan konten yang sesuai.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-05 (Tampilan Halaman Rincian untuk Halaman Detail Item, Galeri Gambar & Kalender Ketersediaan (Detail View)) untuk proyek KosHunt.
Layer: frontend | Fase: 1

Objektif:
Bangun halaman detail item dengan galeri preview, rincian spesifikasi, kalkulasi ringkas biaya, dan tombol aksi pemesanan.

Checklist Pengerjaan:
- Buat halaman detail dinamis dengan routing slug/id
- Tampilkan spesifikasi, fasilitas, dan status ketersediaan
- Buat komponen ringkasan harga dan tombol call-to-action (CTA)

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Klik salah satu item dari halaman utama: browser berpindah ke halaman detail dengan konten yang sesuai.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-06] Komponen Modal Dialog & Formulir Input Interaktif dengan Validasi Zod
- **Layer:** `frontend` | **Fase:** `1`
- **Objektif:** Bangun dialog modal responsif untuk pembuatan entri baru atau booking, dilengkapi pesan kesalahan validasi ramah pengguna.
- **File Terkait:** `src/components/ui/Modal.tsx`, `src/components/forms/EntryFormModal.tsx`, `src/schemas/formSchema.ts`
- **Checklist Eksekusi:**
  - [ ] Buat reusable Modal Dialog berbasis Radix UI Primitives
  - [ ] Definisikan skema validasi form dengan Zod
  - [ ] Tampilkan pesan error validasi inline di bawah input yang tidak valid
  - [ ] Simulasikan submit berhasil dengan memunculkan toast notifikasi
- **Verifikasi Penerimaan (Acceptance Test):** Buka modal, tekan submit saat kosong -> muncul pesan error. Isi data valid -> modal tertutup dan toast sukses muncul.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-06 (Komponen Modal Dialog & Formulir Input Interaktif dengan Validasi Zod) untuk proyek KosHunt.
Layer: frontend | Fase: 1

Objektif:
Bangun dialog modal responsif untuk pembuatan entri baru atau booking, dilengkapi pesan kesalahan validasi ramah pengguna.

Checklist Pengerjaan:
- Buat reusable Modal Dialog berbasis Radix UI Primitives
- Definisikan skema validasi form dengan Zod
- Tampilkan pesan error validasi inline di bawah input yang tidak valid
- Simulasikan submit berhasil dengan memunculkan toast notifikasi

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Buka modal, tekan submit saat kosong -> muncul pesan error. Isi data valid -> modal tertutup dan toast sukses muncul.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---

## FASE 2 — STATE MANAGEMENT & INTERAKSI KLIEN (Layer: Frontend)
*Tujuan: Menyambungkan form input, validasi Zod, dan manipulasi data di memori/localStorage.*
### [T-07] Sinkronisasi State URL Query Parameters (Filter, Search & Pagination)
- **Layer:** `frontend` | **Fase:** `2`
- **Objektif:** Gunakan URL search params sebagai single source of truth untuk filter dan pagination agar halaman mudah dibagikan (shareable).
- **File Terkait:** `src/hooks/useCatalogFilters.ts`, `src/pages/CatalogPage.tsx`
- **Checklist Eksekusi:**
  - [ ] Integrasikan nuqs atau custom useSearchParams hook
  - [ ] Sinkronkan nilai search, category, dan page ke parameter query URL
  - [ ] Pastikan tombol navigasi browser 'Back' dan 'Forward' mengembalikan state filter dengan benar
- **Verifikasi Penerimaan (Acceptance Test):** Salin URL setelah memfilter data, buka di tab baru: filter dan hasil pencarian yang sama langsung terbuka.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-07 (Sinkronisasi State URL Query Parameters (Filter, Search & Pagination)) untuk proyek KosHunt.
Layer: frontend | Fase: 2

Objektif:
Gunakan URL search params sebagai single source of truth untuk filter dan pagination agar halaman mudah dibagikan (shareable).

Checklist Pengerjaan:
- Integrasikan nuqs atau custom useSearchParams hook
- Sinkronkan nilai search, category, dan page ke parameter query URL
- Pastikan tombol navigasi browser 'Back' dan 'Forward' mengembalikan state filter dengan benar

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Salin URL setelah memfilter data, buka di tab baru: filter dan hasil pencarian yang sama langsung terbuka.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-08] Local Store Management & CRUD Client-Side di Memori
- **Layer:** `frontend` | **Fase:** `2`
- **Objektif:** Implementasikan state store lokal (Zustand / Context) sehingga aksi tambah, ubah, dan hapus data langsung tercermin di UI.
- **File Terkait:** `src/store/useAppStore.ts`
- **Checklist Eksekusi:**
  - [ ] Inisialisasi app store untuk menampung entri data di client
  - [ ] Tambahkan fungsi Create, Update, dan Delete di memori
  - [ ] Simpan perubahan ke localStorage agar data tidak hilang saat refresh
- **Verifikasi Penerimaan (Acceptance Test):** Buat entri baru via form modal: entri langsung muncul di daftar. Refresh halaman: data baru tetap ada.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-08 (Local Store Management & CRUD Client-Side di Memori) untuk proyek KosHunt.
Layer: frontend | Fase: 2

Objektif:
Implementasikan state store lokal (Zustand / Context) sehingga aksi tambah, ubah, dan hapus data langsung tercermin di UI.

Checklist Pengerjaan:
- Inisialisasi app store untuk menampung entri data di client
- Tambahkan fungsi Create, Update, dan Delete di memori
- Simpan perubahan ke localStorage agar data tidak hilang saat refresh

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Buat entri baru via form modal: entri langsung muncul di daftar. Refresh halaman: data baru tetap ada.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-09] Komponen Empty State, Error Boundary, dan Toast System
- **Layer:** `frontend` | **Fase:** `2`
- **Objektif:** Lengkapi aplikasi dengan sistem toast notifikasi mandiri, kartu penanganan data kosong, dan batas penangkap error runtime.
- **File Terkait:** `src/components/ui/Toast.tsx`, `src/components/ui/EmptyState.tsx`, `src/components/ErrorBoundary.tsx`
- **Checklist Eksekusi:**
  - [ ] Buat Toast Provider dan helper `showToast(title, type)`
  - [ ] Buat komponen EmptyState dengan tombol CTA terarah
  - [ ] Pasang React ErrorBoundary untuk mencegah layar putih saat terjadi crash
- **Verifikasi Penerimaan (Acceptance Test):** Filter data dengan kata kunci ngawur: muncul Empty State yang rapi dengan tombol 'Reset Filter'.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-09 (Komponen Empty State, Error Boundary, dan Toast System) untuk proyek KosHunt.
Layer: frontend | Fase: 2

Objektif:
Lengkapi aplikasi dengan sistem toast notifikasi mandiri, kartu penanganan data kosong, dan batas penangkap error runtime.

Checklist Pengerjaan:
- Buat Toast Provider dan helper `showToast(title, type)`
- Buat komponen EmptyState dengan tombol CTA terarah
- Pasang React ErrorBoundary untuk mencegah layar putih saat terjadi crash

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Filter data dengan kata kunci ngawur: muncul Empty State yang rapi dengan tombol 'Reset Filter'.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-10] Sistem Verifikasi Checkpoint Fase 1 & 2 (Frontend Review)
- **Layer:** `frontend` | **Fase:** `2`
- **Objektif:** Audit menyeluruh terhadap seluruh antarmuka sebelum berpindah ke layer backend dan database.
- **File Terkait:** `src/tests/ui-flow.test.ts`
- **Checklist Eksekusi:**
  - [ ] Uji coba seluruh alur navigasi dari awal hingga akhir
  - [ ] Periksa responsivitas pada layar ponsel (360px) dan laptop
  - [ ] Pastikan tidak ada error console JavaScript atau warning missing keys
- **Verifikasi Penerimaan (Acceptance Test):** Semua fungsionalitas UI dapat diuji secara interaktif tanpa backend dan siap disambungkan ke API.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-10 (Sistem Verifikasi Checkpoint Fase 1 & 2 (Frontend Review)) untuk proyek KosHunt.
Layer: frontend | Fase: 2

Objektif:
Audit menyeluruh terhadap seluruh antarmuka sebelum berpindah ke layer backend dan database.

Checklist Pengerjaan:
- Uji coba seluruh alur navigasi dari awal hingga akhir
- Periksa responsivitas pada layar ponsel (360px) dan laptop
- Pastikan tidak ada error console JavaScript atau warning missing keys

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Semua fungsionalitas UI dapat diuji secara interaktif tanpa backend dan siap disambungkan ke API.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---

## FASE 3 — SKEMA DATABASE, AUTENTIKASI, & API BACKEND (Layer: Database & Backend)
*Tujuan: Membuat skema tabel DDL, migrasi DB, autentikasi session, dan endpoint RESTful API.*
### [T-11] Penyusunan Skema Database Drizzle / Prisma & Konfigurasi Koneksi
- **Layer:** `database` | **Fase:** `3`
- **Objektif:** Tulis definisi tabel database resmi lengkap dengan foreign key, index pencarian, dan konfigurasi connection pool.
- **File Terkait:** `src/db/schema.ts`, `src/db/index.ts`, `drizzle.config.ts`
- **Checklist Eksekusi:**
  - [ ] Buat file skema database sesuai DDL yang dirancang di PRD
  - [ ] Konfigurasi connection pool ke database PostgreSQL
  - [ ] Setup script migration di package.json (`npm run db:push` / `npm run db:migrate`)
- **Verifikasi Penerimaan (Acceptance Test):** Jalankan perintah migrasi: koneksi database sukses dan tabel terbuat lengkap dengan tipe datanya.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-11 (Penyusunan Skema Database Drizzle / Prisma & Konfigurasi Koneksi) untuk proyek KosHunt.
Layer: database | Fase: 3

Objektif:
Tulis definisi tabel database resmi lengkap dengan foreign key, index pencarian, dan konfigurasi connection pool.

Checklist Pengerjaan:
- Buat file skema database sesuai DDL yang dirancang di PRD
- Konfigurasi connection pool ke database PostgreSQL
- Setup script migration di package.json (`npm run db:push` / `npm run db:migrate`)

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Jalankan perintah migrasi: koneksi database sukses dan tabel terbuat lengkap dengan tipe datanya.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-12] Script Seeding Database Awal untuk Lingkungan Development
- **Layer:** `database` | **Fase:** `3`
- **Objektif:** Tulis script seed otomatis untuk mengisi database dengan data kategori dan entri uji coba.
- **File Terkait:** `src/db/seed.ts`
- **Checklist Eksekusi:**
  - [ ] Tulis script seed.ts yang idempotent (tidak duplikat saat dijalankan ulang)
  - [ ] Isi data kategori dasar dan contoh entri realistis
  - [ ] Verifikasi hasil seed lewat database client atau query SELECT
- **Verifikasi Penerimaan (Acceptance Test):** Jalankan `npm run db:seed`: database terisi record uji coba yang siap dipakai.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-12 (Script Seeding Database Awal untuk Lingkungan Development) untuk proyek KosHunt.
Layer: database | Fase: 3

Objektif:
Tulis script seed otomatis untuk mengisi database dengan data kategori dan entri uji coba.

Checklist Pengerjaan:
- Tulis script seed.ts yang idempotent (tidak duplikat saat dijalankan ulang)
- Isi data kategori dasar dan contoh entri realistis
- Verifikasi hasil seed lewat database client atau query SELECT

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Jalankan `npm run db:seed`: database terisi record uji coba yang siap dipakai.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-13] Setup Autentikasi Pengguna & Session Cookie Handler
- **Layer:** `backend` | **Fase:** `3`
- **Objektif:** Implementasikan sistem autentikasi (Better Auth / NextAuth / JWT) dengan proteksi cookie HttpOnly.
- **File Terkait:** `src/auth.ts`, `src/routes/api/auth.ts`
- **Checklist Eksekusi:**
  - [ ] Konfigurasi auth provider dengan Google OAuth dan email password
  - [ ] Buat endpoint sign-in, sign-up, sign-out, dan get session
  - [ ] Simpan user baru secara otomatis ke tabel database saat pertama login
- **Verifikasi Penerimaan (Acceptance Test):** Uji login via form atau OAuth: session token tersimpan di cookie dan endpoint auth/session mengembalikan data profil.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-13 (Setup Autentikasi Pengguna & Session Cookie Handler) untuk proyek KosHunt.
Layer: backend | Fase: 3

Objektif:
Implementasikan sistem autentikasi (Better Auth / NextAuth / JWT) dengan proteksi cookie HttpOnly.

Checklist Pengerjaan:
- Konfigurasi auth provider dengan Google OAuth dan email password
- Buat endpoint sign-in, sign-up, sign-out, dan get session
- Simpan user baru secara otomatis ke tabel database saat pertama login

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Uji login via form atau OAuth: session token tersimpan di cookie dan endpoint auth/session mengembalikan data profil.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-14] Middleware Auth Guard & Verifikasi Role Hak Akses
- **Layer:** `backend` | **Fase:** `3`
- **Objektif:** Pasang middleware untuk memproteksi rute API sensitif dari akses tanpa token autentikasi.
- **File Terkait:** `src/middleware/authGuard.ts`
- **Checklist Eksekusi:**
  - [ ] Buat middleware guard yang membaca session dari header/cookie
  - [ ] Tolak request tanpa auth dengan HTTP 401 Unauthorized
  - [ ] Buat guard khusus role admin yang mengembalikan HTTP 403 Forbidden jika role tidak sesuai
- **Verifikasi Penerimaan (Acceptance Test):** Akses endpoint privat tanpa login -> tertolak 401. Akses dengan session valid -> request diteruskan.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-14 (Middleware Auth Guard & Verifikasi Role Hak Akses) untuk proyek KosHunt.
Layer: backend | Fase: 3

Objektif:
Pasang middleware untuk memproteksi rute API sensitif dari akses tanpa token autentikasi.

Checklist Pengerjaan:
- Buat middleware guard yang membaca session dari header/cookie
- Tolak request tanpa auth dengan HTTP 401 Unauthorized
- Buat guard khusus role admin yang mengembalikan HTTP 403 Forbidden jika role tidak sesuai

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Akses endpoint privat tanpa login -> tertolak 401. Akses dengan session valid -> request diteruskan.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-15] REST API: Endpoint GET List dengan Pagination, Search & Filter
- **Layer:** `backend` | **Fase:** `3`
- **Objektif:** Bangun endpoint GET untuk mengambil data dengan validasi query params Zod, pagination offset/limit, dan SQL index query.
- **File Terkait:** `src/routes/api/items.get.ts`, `src/controllers/itemController.ts`
- **Checklist Eksekusi:**
  - [ ] Validasi query parameter (search, category, page, limit) via Zod
  - [ ] Eksekusi query database dengan kalkulasi total halaman dan total record
  - [ ] Kembalikan response JSON terstandarisasi `{ success: true, data: [...], pagination: {...} }`
- **Verifikasi Penerimaan (Acceptance Test):** Uji via curl: `GET /api/v1/items?limit=5` mengembalikan tepat 5 record dan metadata pagination.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-15 (REST API: Endpoint GET List dengan Pagination, Search & Filter) untuk proyek KosHunt.
Layer: backend | Fase: 3

Objektif:
Bangun endpoint GET untuk mengambil data dengan validasi query params Zod, pagination offset/limit, dan SQL index query.

Checklist Pengerjaan:
- Validasi query parameter (search, category, page, limit) via Zod
- Eksekusi query database dengan kalkulasi total halaman dan total record
- Kembalikan response JSON terstandarisasi `{ success: true, data: [...], pagination: {...} }`

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Uji via curl: `GET /api/v1/items?limit=5` mengembalikan tepat 5 record dan metadata pagination.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-16] REST API: Endpoint GET Detail Berdasarkan ID / Slug
- **Layer:** `backend` | **Fase:** `3`
- **Objektif:** Endpoint untuk mengambil informasi spesifik satu entitas dengan penanganan 404 jika tidak ditemukan.
- **File Terkait:** `src/routes/api/items.detail.ts`
- **Checklist Eksekusi:**
  - [ ] Validasi parameter ID (UUID) atau slug
  - [ ] Query join dengan relasi kategori dan pemilik data
  - [ ] Kembalikan 404 Not Found dengan pesan jelas jika ID tidak ada di database
- **Verifikasi Penerimaan (Acceptance Test):** Request ID valid mengembalikan objek lengkap. Request ID acak mengembalikan status 404.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-16 (REST API: Endpoint GET Detail Berdasarkan ID / Slug) untuk proyek KosHunt.
Layer: backend | Fase: 3

Objektif:
Endpoint untuk mengambil informasi spesifik satu entitas dengan penanganan 404 jika tidak ditemukan.

Checklist Pengerjaan:
- Validasi parameter ID (UUID) atau slug
- Query join dengan relasi kategori dan pemilik data
- Kembalikan 404 Not Found dengan pesan jelas jika ID tidak ada di database

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Request ID valid mengembalikan objek lengkap. Request ID acak mengembalikan status 404.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-17] REST API: Endpoint POST Pembuatan Data Baru & Validasi Payload
- **Layer:** `backend` | **Fase:** `3`
- **Objektif:** Endpoint POST dengan validasi skema body Zod, sanitasi string dari injeksi, dan penyimpanan transaksi database.
- **File Terkait:** `src/routes/api/items.post.ts`
- **Checklist Eksekusi:**
  - [ ] Validasi body request menggunakan skema Zod ketat
  - [ ] Kaitkan data baru dengan ID user yang sedang login dari session
  - [ ] Kembalikan response HTTP 201 Created dengan data yang baru dibuat
- **Verifikasi Penerimaan (Acceptance Test):** Kirim payload tidak lengkap -> respons 422 Unprocessable Entity. Kirim payload valid -> data tersimpan di DB.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-17 (REST API: Endpoint POST Pembuatan Data Baru & Validasi Payload) untuk proyek KosHunt.
Layer: backend | Fase: 3

Objektif:
Endpoint POST dengan validasi skema body Zod, sanitasi string dari injeksi, dan penyimpanan transaksi database.

Checklist Pengerjaan:
- Validasi body request menggunakan skema Zod ketat
- Kaitkan data baru dengan ID user yang sedang login dari session
- Kembalikan response HTTP 201 Created dengan data yang baru dibuat

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Kirim payload tidak lengkap -> respons 422 Unprocessable Entity. Kirim payload valid -> data tersimpan di DB.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-18] REST API: Endpoint PATCH/PUT Update dan DELETE Soft-Delete
- **Layer:** `backend` | **Fase:** `3`
- **Objektif:** Endpoint pembaruan data dan penghapusan dengan verifikasi hak milik data (hanya pembuat/admin yang boleh mengubah).
- **File Terkait:** `src/routes/api/items.mutate.ts`
- **Checklist Eksekusi:**
  - [ ] Verifikasi bahwa user yang login adalah pemilik record atau role admin
  - [ ] Implementasikan pembaruan parsial (PATCH)
  - [ ] Implementasikan soft-delete atau penghapusan aman
- **Verifikasi Penerimaan (Acceptance Test):** User A mencoba mengubah data milik User B -> tertolak 403 Forbidden. User A mengubah data sendiri -> sukses 200 OK.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-18 (REST API: Endpoint PATCH/PUT Update dan DELETE Soft-Delete) untuk proyek KosHunt.
Layer: backend | Fase: 3

Objektif:
Endpoint pembaruan data dan penghapusan dengan verifikasi hak milik data (hanya pembuat/admin yang boleh mengubah).

Checklist Pengerjaan:
- Verifikasi bahwa user yang login adalah pemilik record atau role admin
- Implementasikan pembaruan parsial (PATCH)
- Implementasikan soft-delete atau penghapusan aman

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
User A mencoba mengubah data milik User B -> tertolak 403 Forbidden. User A mengubah data sendiri -> sukses 200 OK.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---

## FASE 4 — INTEGRASI END-TO-END, HARDENING, & POLISH (Layer: Integration & Polish)
*Tujuan: Mengganti mock data dengan API nyata, audit keamanan, pengujian SEO, dan verifikasi production build.*
### [T-19] Setup API Client & TanStack Query Provider di Frontend
- **Layer:** `integration` | **Fase:** `4`
- **Objektif:** Buat wrapper HTTP client (fetch/axios) terpusat dengan penanganan kredensial cookie otomatis dan interceptor error.
- **File Terkait:** `src/api/client.ts`, `src/providers/QueryProvider.tsx`
- **Checklist Eksekusi:**
  - [ ] Konfigurasi Base URL dan default headers di API client
  - [ ] Pasang interceptor respons untuk menangani 401 (redirect ke login) secara global
  - [ ] Konfigurasi TanStack QueryClient dengan retry policy yang cerdas
- **Verifikasi Penerimaan (Acceptance Test):** QueryClient terpasang di root aplikasi tanpa error re-render ganda.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-19 (Setup API Client & TanStack Query Provider di Frontend) untuk proyek KosHunt.
Layer: integration | Fase: 4

Objektif:
Buat wrapper HTTP client (fetch/axios) terpusat dengan penanganan kredensial cookie otomatis dan interceptor error.

Checklist Pengerjaan:
- Konfigurasi Base URL dan default headers di API client
- Pasang interceptor respons untuk menangani 401 (redirect ke login) secara global
- Konfigurasi TanStack QueryClient dengan retry policy yang cerdas

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
QueryClient terpasang di root aplikasi tanpa error re-render ganda.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-20] Wiring Frontend: Gantikan Mock Data dengan Query API Riil
- **Layer:** `integration` | **Fase:** `4`
- **Objektif:** Sambungkan komponen katalog dan detail view ke custom hook `useQuery` yang menarik data asli dari database.
- **File Terkait:** `src/hooks/useItemsQuery.ts`, `src/pages/CatalogPage.tsx`
- **Checklist Eksekusi:**
  - [ ] Buat hook `useItemsQuery` dan `useItemDetailQuery`
  - [ ] Gantikan sumber data mock di halaman utama dengan hasil query API
  - [ ] Pastikan skeleton loader menyala selama fetching data dari server
- **Verifikasi Penerimaan (Acceptance Test):** Buka tab Network di browser: terlihat request `GET /api/v1/items` dan data dari PostgreSQL ter-render di UI.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-20 (Wiring Frontend: Gantikan Mock Data dengan Query API Riil) untuk proyek KosHunt.
Layer: integration | Fase: 4

Objektif:
Sambungkan komponen katalog dan detail view ke custom hook `useQuery` yang menarik data asli dari database.

Checklist Pengerjaan:
- Buat hook `useItemsQuery` dan `useItemDetailQuery`
- Gantikan sumber data mock di halaman utama dengan hasil query API
- Pastikan skeleton loader menyala selama fetching data dari server

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Buka tab Network di browser: terlihat request `GET /api/v1/items` dan data dari PostgreSQL ter-render di UI.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-21] Wiring Mutasi: Form Submit & Optimistic UI Update
- **Layer:** `integration` | **Fase:** `4`
- **Objektif:** Sambungkan form modal ke `useMutation` untuk menyimpan data langsung ke server dengan invalidasi cache otomatis.
- **File Terkait:** `src/hooks/useItemMutations.ts`, `src/components/forms/EntryFormModal.tsx`
- **Checklist Eksekusi:**
  - [ ] Buat hook `useCreateItemMutation`
  - [ ] Gantikan submit tiruan form dengan mutasi API nyata
  - [ ] Trigger `queryClient.invalidateQueries` setelah mutasi berhasil agar list ter-update otomatis
- **Verifikasi Penerimaan (Acceptance Test):** Submit form baru di browser: baris baru tersimpan di database dan langsung muncul di list tanpa perlu reload halaman.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-21 (Wiring Mutasi: Form Submit & Optimistic UI Update) untuk proyek KosHunt.
Layer: integration | Fase: 4

Objektif:
Sambungkan form modal ke `useMutation` untuk menyimpan data langsung ke server dengan invalidasi cache otomatis.

Checklist Pengerjaan:
- Buat hook `useCreateItemMutation`
- Gantikan submit tiruan form dengan mutasi API nyata
- Trigger `queryClient.invalidateQueries` setelah mutasi berhasil agar list ter-update otomatis

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Submit form baru di browser: baris baru tersimpan di database dan langsung muncul di list tanpa perlu reload halaman.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-22] Audit Keamanan Trust Boundary, Sanitasi Input, dan Rate Limiting
- **Layer:** `polish` | **Fase:** `4`
- **Objektif:** Audit keamanan aplikasi: periksa celah XSS, pastikan CORS hanya mengizinkan origin terpercaya, dan pasang rate limiting.
- **File Terkait:** `src/server/security.ts`
- **Checklist Eksekusi:**
  - [ ] Pasang security headers (Helmet / CSP)
  - [ ] Uji coba input string berbahaya `<script>alert(1)</script>` untuk memastikan output tersanitasi aman
  - [ ] Pasang in-memory rate limiting pada endpoint publik
- **Verifikasi Penerimaan (Acceptance Test):** Lakukan spam request > 100 kali berturut-turut: server mengembalikan HTTP 429 Too Many Requests.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-22 (Audit Keamanan Trust Boundary, Sanitasi Input, dan Rate Limiting) untuk proyek KosHunt.
Layer: polish | Fase: 4

Objektif:
Audit keamanan aplikasi: periksa celah XSS, pastikan CORS hanya mengizinkan origin terpercaya, dan pasang rate limiting.

Checklist Pengerjaan:
- Pasang security headers (Helmet / CSP)
- Uji coba input string berbahaya `<script>alert(1)</script>` untuk memastikan output tersanitasi aman
- Pasang in-memory rate limiting pada endpoint publik

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Lakukan spam request > 100 kali berturut-turut: server mengembalikan HTTP 429 Too Many Requests.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-23] Optimasi SEO, OpenGraph Meta Tags, dan PWA Manifest
- **Layer:** `polish` | **Fase:** `4`
- **Objektif:** Lengkapi metadata sosial media, gambar pratinjau OG image, dan konfigurasi Web App Manifest untuk instalasi mobile.
- **File Terkait:** `src/app/metadata.ts`, `public/manifest.json`
- **Checklist Eksekusi:**
  - [ ] Tambahkan OpenGraph (og:title, og:description, og:image) dan Twitter Cards
  - [ ] Buat file manifest.json dan konfigurasi favicon beragam ukuran
  - [ ] Pastikan canonical URL terpasang dengan benar di setiap rute
- **Verifikasi Penerimaan (Acceptance Test):** Uji via pratinjau meta tag: thumbnail dan deskripsi situs muncul rapi saat dibagikan.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-23 (Optimasi SEO, OpenGraph Meta Tags, dan PWA Manifest) untuk proyek KosHunt.
Layer: polish | Fase: 4

Objektif:
Lengkapi metadata sosial media, gambar pratinjau OG image, dan konfigurasi Web App Manifest untuk instalasi mobile.

Checklist Pengerjaan:
- Tambahkan OpenGraph (og:title, og:description, og:image) dan Twitter Cards
- Buat file manifest.json dan konfigurasi favicon beragam ukuran
- Pastikan canonical URL terpasang dengan benar di setiap rute

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Uji via pratinjau meta tag: thumbnail dan deskripsi situs muncul rapi saat dibagikan.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
### [T-24] Verifikasi Akhir Build Production & Smoke Test Mandiri
- **Layer:** `polish` | **Fase:** `4`
- **Objektif:** Jalankan build produksi akhir, cek ukuran bundle JS, dan lakukan smoke test komprehensif seluruh alur aplikasi.
- **File Terkait:** `package.json`
- **Checklist Eksekusi:**
  - [ ] Jalankan `npm run build` dan verifikasi bundle size budget (< 150KB initial JS)
  - [ ] Jalankan smoke test: pendaftaran user -> login -> buat entri data -> filter/search -> logout
  - [ ] Pastikan aplikasi 100% siap untuk deployment produksi
- **Verifikasi Penerimaan (Acceptance Test):** Hasil build production lolos tanpa error type. Seluruh alur kerja teruji dan berfungsi sempurna.

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task T-24 (Verifikasi Akhir Build Production & Smoke Test Mandiri) untuk proyek KosHunt.
Layer: polish | Fase: 4

Objektif:
Jalankan build produksi akhir, cek ukuran bundle JS, dan lakukan smoke test komprehensif seluruh alur aplikasi.

Checklist Pengerjaan:
- Jalankan `npm run build` dan verifikasi bundle size budget (< 150KB initial JS)
- Jalankan smoke test: pendaftaran user -> login -> buat entri data -> filter/search -> logout
- Pastikan aplikasi 100% siap untuk deployment produksi

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
Hasil build production lolos tanpa error type. Seluruh alur kerja teruji dan berfungsi sempurna.

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
