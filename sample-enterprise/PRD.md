# Product Requirement Document (PRD)
## KosHunt — Spesifikasi Rekayasa Sistem

> **Versi:** 1.0.0 (Production-Grade Enriched)  
> **Status Dokumen:** Approved for Autonomous Agent Implementation  
> **Kategori:** Marketplace, Rental & Booking Engine  
> **Target Pengguna:** Mahasiswa & Pengguna Umum  
> **Arsitektur Acuan:** TanStack Start + Drizzle ORM + PostgreSQL  

---

## 1. Ringkasan Eksekutif & Problem Statement

### 1.1 Latar Belakang Masalah
Kebutuhan pengguna yang mendasari proyek ini:
> "Aplikasi pencarian kosan mahasiswa dekat UNSIL dengan filter radius 10km dan WhatsApp owner"

Banyak pengguna dalam kategori **Mahasiswa & Pengguna Umum** menghadapi kendala alur kerja manual, fragmentasi informasi, dan antarmuka lambat yang menyita waktu produktif. Aplikasi **KosHunt** dirancang sebagai solusi terpadu yang memadukan kecepatan muat, antarmuka minimalis tanpa friksi, dan arsitektur *type-safe* dari database hingga komponen layar.

### 1.2 Tujuan Utama Proyek (Key Performance Indicators)
1. **Kecepatan Akses & Interaksi:** Waktu muat awal (First Contentful Paint) < 1.2 detik dan penyelesaian alur kerja utama pengguna dalam kurang dari 3 kali klik.
2. **Keandalan & Zero Data Loss:** Semua formulir dan interaksi penting memiliki validasi batas ganda (*client-side* dan *server-side*) serta proteksi draf lokal di browser.
3. **Optimasi AI Coding Agent:** Struktur kode dirancang modular dan berbasis konvensi baku (*boring over clever*), meminimalkan konsumsi context token saat dikembangkan oleh agen seperti Claude Code, Hermes, atau Cursor.

---

## 2. Profil Pengguna & User Personas

#### Persona 1: Primary User (Mahasiswa & Pengguna Umum)
- **Tujuan Utama:** Menyelesaikan kebutuhan terkait KosHunt dengan cepat tanpa hambatan teknis.
- **Tingkat Kemahiran Digital:** Menengah (terbiasa dengan browser mobile/desktop modern).
- **Kendala Utama (Pain Points):**
    - Antarmuka yang rumit dan lambat dimuat di koneksi seluler.
    - Kehilangan progres input saat browser di-refresh atau koneksi terputus.
    - Ketidakjelasan status proses/transaksi saat melakukan aksi.

#### Persona 2: System Administrator / Operator
- **Tujuan Utama:** Memantau kesehatan aplikasi, mengaudit entri data, dan mengelola hak akses pengguna.
- **Tingkat Kemahiran Digital:** Tinggi (familiar dengan dashboard admin dan metrik sistem).
- **Kendala Utama (Pain Points):**
    - Kesulitan melacak error log dan transaksi yang menggantung (orphaned records).
    - Ketiadaan sistem audit log untuk aksi-aksi sensitif.



---

## 3. Arsitektur Teknis & Tech Stack

| Lapisan Sistem | Teknologi Pilihan | Alasan Pemilihan & Manfaat Teknis |
| :--- | :--- | :--- |
| **Framework Utama** | TanStack Start (Vite + SSR/Hydration) + Tailwind CSS v3.4 + Radix UI Primitives + Lucide Icons | Rendering cepat berbasis SSR/Hydration, ekosistem standar industri, dan navigasi instan. |
| **Server Engine** | TanStack Server Functions (Nitro Engine) / Node.js 20 LTS | Menangani Server Functions & endpoint API berlatensi rendah dengan konsumsi memori efisien. |
| **Database & ORM** | PostgreSQL 16 (Neon Serverless / Supabase) + Drizzle ORM + Drizzle Kit | Skema *type-safe* penuh dari query hingga TypeScript, migrasi terkontrol, dan koneksi serverless. |
| **Autentikasi** | Better Auth (Google OAuth 2.0 + Email/Password) dengan HTTP-Only SameSite Cookies | Pengelolaan session aman dengan proteksi HttpOnly SameSite cookie dan proteksi CSRF bawaan. |
| **State Management** | TanStack Query v5 + nuqs (URL Search Params State Manager) | Menjaga sinkronisasi data server tanpa re-render berlebih serta persistensi state di URL query. |
| **Validasi Skema** | Zod v3.23 (Client & Server Boundary Validation) | Validasi terpadu pada batas kepercayaan (*trust boundary*) baik di formulir UI maupun body API. |
| **Testing Harness** | Vitest + Playwright + MSW (Mock Service Worker) | Pengujian unit dan integrasi otomatis untuk mencegah regresi logika. |

---

## 4. Matriks State Komponen Antarmuka (UI State Matrix)

| Layar / Komponen | Empty State | Loading State | Error State | Success State |
| :--- | :--- | :--- | :--- | :--- |
| **Halaman Utama & Katalog / Dashboard** | Tampilkan kartu ilustrasi kosong dengan tombol ajakan utama (CTA) untuk membuat entri data perdana. | Gunakan shimmer skeleton layout yang mencerminkan bentuk kartu/tabel sebenarnya (bukan sekadar spinner putar). | Tampilkan banner error dengan tombol 'Coba Lagi' dan kode pelacak insiden. | Animasi fade-in halus 300ms saat data berhasil ditarik dari server. |
| **Modal Form Input & Editor** | Form terisi nilai default yang masuk akal (tanggal hari ini, kategori teratas). | Tombol simpan menampilkan spinner mini dan teks 'Menyimpan...', semua input dinonaktifkan sementara. | Pesan error validasi berwarna merah tepat di bawah field input yang bermasalah (inline error). | Modal menutup otomatis, form reset, dan memunculkan toast notifikasi sukses berwarna hijau di kanan bawah. |


---

## 5. Spesifikasi Rinci Modul & Fitur

### [F-01] Katalog Interaktif, Pencarian Fuzzy & Filtering Lanjutan
- **Ringkasan Fungsi:** Tampilan katalog produk/item dengan debounce search, filter kategori multi-pilihan, sorting harga/jarak, dan pagination responsif.
- **User Story:** Sebagai Mahasiswa & Pengguna Umum, saya ingin mencari dan memfilter item berdasarkan harga, lokasi, dan ketersediaan agar menemukan opsi paling sesuai dalam hitungan detik.
- **Kriteria Penerimaan (Acceptance Criteria):**
  - [ ] Pencarian merespons real-time dengan debounce 300ms tanpa flicker UI.
  - [ ] Filter status dan kategori tersinkronisasi dua arah ke URL query params (nuqs).
  - [ ] Menampilkan skeleton loading placeholder saat fetching data dan empty state ilustratif jika hasil 0.
- **Penanganan Kondisi Khusus & Error:**
  - ⚠️ *Edge Case:* Koneksi offline: tampilkan banner reconnect dan gunakan cache data lokal terakhir.
  - ⚠️ *Edge Case:* Input karakter query berbahaya: sanitasi XSS otomatis pada input string.

### [F-02] Halaman Detail Item, Galeri Gambar & Kalender Ketersediaan
- **Ringkasan Fungsi:** Detail spesifikasi lengkap, carousel galeri gambar terkompresi, status stok aktual, dan picker rentang tanggal peminjaman/booking.
- **User Story:** Sebagai Mahasiswa & Pengguna Umum, saya ingin melihat foto detail, fasilitas, dan ketersediaan jadwal agar dapat memutuskan pemesanan dengan yakin.
- **Kriteria Penerimaan (Acceptance Criteria):**
  - [ ] Gambar menggunakan lazy loading dengan placeholder blur hash.
  - [ ] Validasi rentang tanggal: tanggal mulai tidak boleh di masa lalu dan tanggal akhir >= tanggal mulai.
  - [ ] Kalkulator biaya otomatis menghitung subtotal durasi sewa, biaya admin, dan total deposit.
- **Penanganan Kondisi Khusus & Error:**
  - ⚠️ *Edge Case:* Item sudah dibooking orang lain: tampilkan badge 'Tidak Tersedia' dan nonaktifkan tombol checkout.

### [F-03] Alur Checkout, Form Pemesan & Integrasi Payment Gateway
- **Ringkasan Fungsi:** Form pemesanan terstruktur dengan validasi ketat, pemilihan metode pembayaran (QRIS / Virtual Account), dan penanganan webhook status.
- **User Story:** Sebagai Mahasiswa & Pengguna Umum, saya ingin melakukan checkout aman dan menerima instruksi pembayaran instan agar pesanan segera terkonfirmasi.
- **Kriteria Penerimaan (Acceptance Criteria):**
  - [ ] Validasi formulir kontak pemesan (nama minimal 3 karakter, nomor WhatsApp valid format Indonesia +62/08).
  - [ ] Idempotency key pada request pembuatan transaksi untuk mencegah double charging.
  - [ ] Menampilkan popup Snap / QRIS modal serta timer countdown kedaluwarsa pembayaran.
- **Penanganan Kondisi Khusus & Error:**
  - ⚠️ *Edge Case:* Transaksi kedaluwarsa: status order otomatis diubah menjadi 'EXPIRED' dan stok dikembalikan.

### [F-04] Dashboard Pelacakan Pesanan & Riwayat Transaksi
- **Ringkasan Fungsi:** Halaman pemantauan pesanan pengguna dengan badge status real-time, nota digital yang dapat diunduh, dan kontak darurat WhatsApp pemilik.
- **User Story:** Sebagai Mahasiswa & Pengguna Umum, saya ingin memantau status persetujuan pesanan dan mengunduh invoice digital sebagai bukti transaksi yang sah.
- **Kriteria Penerimaan (Acceptance Criteria):**
  - [ ] Status pesanan ter-update otomatis (Pending, Paid, Active, Completed, Cancelled).
  - [ ] Tombol sekali klik menuju chat WhatsApp pengelola dengan pesan template otomatis terisi nomor order.
  - [ ] Fitur ekspor invoice/bukti pemesanan format PDF atau cetak bersih.
- **Penanganan Kondisi Khusus & Error:**
  - ⚠️ *Edge Case:* Pengguna mencoba mengakses pesanan milik user lain: kembalikan 403 Forbidden dengan pesan error yang aman.



---

## 6. Skema Database Lengkap (Data Dictionary & DDL)

Berikut adalah DDL SQL PostgreSQL resmi yang mendefinisikan tabel, tipe enum, relasi foreign key dengan aturan integritas referensial, serta indeks pencarian performa:

```sql
-- =====================================================================
-- DDL POSTGRESQL SCHEMA: MARKETPLACE / RENTAL & BOOKING
-- =====================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE user_role AS ENUM ('customer', 'partner', 'admin');
CREATE TYPE booking_status AS ENUM ('pending_payment', 'paid', 'confirmed', 'active', 'completed', 'cancelled', 'expired');
CREATE TYPE payment_method AS ENUM ('qris', 'bank_transfer', 'e_wallet', 'cash');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(120) NOT NULL,
    phone VARCHAR(30),
    role user_role DEFAULT 'customer' NOT NULL,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(80) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    icon_name VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category_id UUID NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(250) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    price_per_day NUMERIC(12, 2) NOT NULL CHECK (price_per_day >= 0),
    deposit_amount NUMERIC(12, 2) DEFAULT 0.00 NOT NULL,
    location_address TEXT NOT NULL,
    location_latitude NUMERIC(10, 7),
    location_longitude NUMERIC(10, 7),
    total_stock INT DEFAULT 1 NOT NULL CHECK (total_stock >= 0),
    available_stock INT DEFAULT 1 NOT NULL CHECK (available_stock >= 0),
    images TEXT[] DEFAULT '{}' NOT NULL,
    facilities TEXT[] DEFAULT '{}' NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_items_category ON items(category_id);
CREATE INDEX idx_items_price ON items(price_per_day);
CREATE INDEX idx_items_is_active ON items(is_active);
CREATE INDEX idx_items_owner ON items(owner_id);

CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_number VARCHAR(32) UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    item_id UUID NOT NULL REFERENCES items(id) ON DELETE RESTRICT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    duration_days INT NOT NULL CHECK (duration_days > 0),
    quantity INT DEFAULT 1 NOT NULL CHECK (quantity > 0),
    subtotal NUMERIC(12, 2) NOT NULL,
    admin_fee NUMERIC(12, 2) DEFAULT 0.00 NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,
    status booking_status DEFAULT 'pending_payment' NOT NULL,
    payment_channel payment_method,
    payment_token VARCHAR(255),
    payment_expires_at TIMESTAMPTZ,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT check_booking_dates CHECK (end_date >= start_date)
);

CREATE INDEX idx_bookings_user ON bookings(user_id);
CREATE INDEX idx_bookings_item ON bookings(item_id);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_bookings_order_num ON bookings(order_number);

```

---

## 7. Kontrak Spesifikasi API (RESTful Endpoints)

#### `GET` /api/v1/items
- **Deskripsi:** Mengambil daftar item dengan pagination, search query, dan filter multi-kategori.
- **Hak Akses:** `Public`
- **Query Parameters:** `page=1&limit=12&search=kemah&category=outdoor&minPrice=10000&maxPrice=150000&sort=price_asc`
- **Request Body (JSON):**
```json
Tidak membutuhkan request body (GET).
```
- **Response Payload (HTTP 200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": "e4f8b910-1234-4567-89ab-cdef01234567",
      "title": "Tenda Dome Kapasitas 4 Orang Waterproof",
      "slug": "tenda-dome-kapasitas-4-orang",
      "pricePerDay": 45000,
      "availableStock": 3,
      "category": "Tenda & Shelter",
      "thumbnail": "https://example.com/images/tenda-1.jpg",
      "facilities": [
        "Waterproof 3000mm",
        "Double Layer",
        "Alu Poles"
      ]
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 12,
    "totalItems": 48,
    "totalPages": 4
  }
}
```

---
#### `POST` /api/v1/bookings
- **Deskripsi:** Membuat pesanan baru dan menerbitkan order token payment gateway.
- **Hak Akses:** `Bearer Token / Session Cookie`
- **Query Parameters:** None
- **Request Body (JSON):**
```json
{
  "itemId": "e4f8b910-1234-4567-89ab-cdef01234567",
  "startDate": "2026-11-05",
  "endDate": "2026-11-08",
  "quantity": 1,
  "customerNotes": "Diambil jam 9 pagi di sekretariat",
  "paymentChannel": "qris"
}
```
- **Response Payload (HTTP 200 OK):**
```json
{
  "success": true,
  "message": "Pesanan berhasil dibuat.",
  "data": {
    "bookingId": "b1a2c3d4-5678-90ab-cdef-112233445566",
    "orderNumber": "ORD-20261105-9482",
    "totalAmount": 140000,
    "status": "pending_payment",
    "paymentSnapUrl": "https://app.midtrans.com/snap/v2/vtweb/mock-token",
    "expiresAt": "2026-11-05T10:30:00.000Z"
  }
}
```

---


---

## 8. Persyaratan Non-Fungsional (Non-Functional Requirements)

1. Performa: First Contentful Paint (FCP) < 1.2 detik dan Time to Interactive (TTI) < 2.0 detik pada koneksi 4G standar.
2. Keamanan: Proteksi terhadap SQL Injection via parameterized queries di Drizzle/Prisma, sanitasi output XSS, dan cookie HttpOnly SameSite=Lax.
3. Rate Limiting: Pembatasan 100 request / menit per IP untuk endpoint publik guna mencegah DDoS dan brute-force.
4. Aksesibilitas (a11y): Kontras warna rasio minimal 4.5:1 (WCAG AA), navigasi penuh via tombol keyboard (Tab/Enter/Escape), dan label ARIA pada komponen interaktif.
5. Irit Token & Modularitas: Komponen dipecah dalam modularitas file < 250 baris untuk mempermudah AI agent membaca dan menyunting kode.

---

## 9. Aturan Emas Pengerjaan untuk AI Coding Agent
1. **Frontend Mock First:** Wajib menyelesaikan Fase 1 & 2 dengan mock data statis terlebih dahulu sebelum membuat tabel database atau server functions, agar user dapat langsung memvalidasi UI di browser.
2. **Single-Task Execution:** Kerjakan satu task per putaran prompt. Dilarang merombak modul di luar cakupan task yang sedang aktif.
3. **Ponytail Principle:** Tulis kode sesedikit mungkin yang bekerja dengan benar ("boring over clever"). Manfaatkan fitur native web API dan pustaka standar.
