#!/usr/bin/env python3
"""
BikinPlan CLI - Enterprise-Grade PRD & Layered Task Breakdown Generator
Mengadopsi standar komprehensif NgodingPakeAI (Skeleton -> PRD -> DDL -> API Contracts -> Layered Tasks)
Prinsip: Ponytail (minimal code, zero-slop, type-safe, runnable verification)
"""

import sys
import os
import json
import argparse
import re
from typing import Dict, Any, List
from agent_config_generator import (
    parse_ddl_to_mermaid,
    generate_mermaid_flowchart,
    generate_claude_markdown,
    generate_cursor_rules,
    generate_cursor_mdc
)

PRESETS = {
    "toko": {
        "name": "TokoOnline Store",
        "target": "Pelanggan & Pembeli Umum",
        "stack": "tanstack",
        "idea": "Website katalog toko online modern dan responsif untuk memamerkan produk dan memproses pesanan belanja dengan checkout WhatsApp, filter stok, dan varian."
    },
    "portfolio": {
        "name": "Portofolio Profesional",
        "target": "Klien, Recruiter & Kolaborator",
        "stack": "tanstack",
        "idea": "Website portofolio pribadi modern dan interaktif untuk personal branding, showcase galeri proyek tech stack, resume CV download, dan formulir kontak."
    },
    "campus": {
        "name": "Sahabat Kampus PWA",
        "target": "Mahasiswa & Sivitas Akademika",
        "stack": "tanstack",
        "idea": "Superapp pendamping mahasiswa PWA offline-first dengan pencarian kosan akurat radius 10km GPS kampus, kalkulator target IPK & SKS offline IndexedDB, kalender deadline tugas kuliah, dan adapter mobile WebView."
    },
    "saas": {
        "name": "MicroSaaS Hub",
        "target": "Indie Creator, Freelancer & Pelanggan",
        "stack": "tanstack",
        "idea": "Platform SaaS langganan digital mikro dengan sistem multi-tier billing, manajemen lisensi aset digital terenkripsi, webhook payment gateway Midtrans/Xendit, dan creator/subscriber RBAC."
    },
    "dashboard": {
        "name": "OmniDash Operations",
        "target": "Tim Operasional, Finance & Administrator Bisnis",
        "stack": "tanstack",
        "idea": "Portal dashboard operasional internal enterprise dengan analisis metrik keuangan, manajemen inventaris, audit logging ketat, dan role-based access control."
    }
}

def refine_idea(name: str, idea: str) -> str:
    """Menganalisis ide dan mengekstrak edge cases teknis secara cerdas (online via BYOK atau rule-based offline)."""
    gemini_key = os.environ.get("GEMINI_API_KEY")
    groq_key = os.environ.get("GROQ_API_KEY")

    prompt = f"Analisis ide aplikasi '{name}': {idea}. Sebutkan 4-5 edge cases teknis, skenario gagal, dan aturan bisnis penting."

    if groq_key:
        try:
            import urllib.request
            req_data = json.dumps({
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are a software architect. Return concise technical edge cases in Indonesian."},
                    {"role": "user", "content": prompt}
                ]
            }).encode('utf-8')
            req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=req_data, headers={
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data["choices"][0]["message"]["content"]
        except Exception:
            pass

    if gemini_key:
        try:
            import urllib.request
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            req_data = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}]
            }).encode('utf-8')
            req = urllib.request.Request(url, data=req_data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            pass

    text = (name + " " + idea).lower()
    edge_cases = []
    if any(k in text for k in ["kos", "lokasi", "gps", "radius", "peta", "map"]):
        edge_cases.append("- **Geolokasi & Radius GPS:** Fallback ke koordinat default kampus jika izin lokasi ditolak; batasi radius pencarian max 10km.")
    if any(k in text for k in ["bayar", "checkout", "payment", "transaksi", "qris", "beli", "sewa", "saas", "billing"]):
        edge_cases.append("- **Integritas Pembayaran:** Gunakan Idempotency Key pada transaksi dan verifikasi signature token HMAC pada webhook gateway.")
    if any(k in text for k in ["offline", "pwa", "cache", "indexeddb", "webview", "kampus"]):
        edge_cases.append("- **Offline & Multi-Platform:** Hindari native alert()/prompt() di WebView; sediakan inline modal dan service worker cache fallback.")
    if any(k in text for k in ["upload", "gambar", "foto", "file", "cv", "pdf"]):
        edge_cases.append("- **File Upload Sanitasi:** Validasi tipe MIME di client & server; batasi ukuran file max 2MB dan kompres WebP di browser.")
    if any(k in text for k in ["auth", "login", "user", "role", "admin", "rbac"]):
        edge_cases.append("- **Keamanan Akses (RBAC):** Proteksi route dengan HttpOnly SameSite cookie dan verifikasi kepemilikan data (owner_id).")
    if any(k in text for k in ["tugas", "nilai", "ipk", "catat", "form"]):
        edge_cases.append("- **Proteksi Draf Lokal:** Auto-save draf formulir ke localStorage setiap 3 detik mencegah kehilangan input saat refresh.")

    if not edge_cases:
        edge_cases.append("- **Validasi Skema Terpadu:** Gunakan Zod v3 di boundary form input dan endpoint API.")
        edge_cases.append("- **Penanganan State Jaringan:** Sediakan komponen empty state, skeleton loading, dan error boundary.")

    return "\n".join(edge_cases)

def synthesize_plan(name: str, idea: str, stack: str = "tanstack", target_audience: str = "Mahasiswa & Umum") -> Dict[str, Any]:
    clean_name = name.strip() or "Aplikasi Baru"
    slug = re.sub(r'[^a-z0-9]+', '-', clean_name.lower()).strip('-')
    
    idea_lower = (idea + " " + clean_name).lower()
    is_portfolio = any(w in idea_lower for w in ["portofolio", "portfolio", "profil", "resume", "cv", "showcase", "personal", "tentang saya", "bio"])
    is_ecommerce = any(w in idea_lower for w in ["toko", "jual", "beli", "store", "commerce", "produk", "sewa", "rent", "kos", "kosan", "katalog", "shop", "barang"])
    is_community = any(w in idea_lower for w in ["komunitas", "forum", "sosial", "chat", "diskusi", "mahasiswa", "kampus", "unsil"])
    is_saas = any(w in idea_lower for w in ["saas", "dashboard", "analisis", "keuangan", "tracking", "catat", "manajemen", "finance", "duit"])

    cat_key = "portfolio" if is_portfolio else ("ecommerce" if is_ecommerce else ("saas" if is_saas else ("community" if is_community else "general")))
    cat_title = {
        "portfolio": "Personal Portfolio & Showcase Website",
        "ecommerce": "Katalog Toko Online & E-Commerce",
        "saas": "SaaS, Financial & Productivity Platform",
        "community": "Campus Community & Collaborative Network",
        "general": "Modern Cloud Web Application"
    }[cat_key]

    stack_configs = {
        "tanstack": {
            "name": "TanStack Start + Drizzle ORM + PostgreSQL",
            "frontend": "TanStack Start (Vite + SSR/Hydration) + Tailwind CSS v3.4 + Radix UI Primitives + Lucide Icons",
            "backend": "TanStack Server Functions (Nitro Engine) / Node.js 20 LTS",
            "database": "PostgreSQL 16 (Neon Serverless / Supabase) + Drizzle ORM + Drizzle Kit",
            "auth": "Better Auth (Google OAuth 2.0 + Email/Password) dengan HTTP-Only SameSite Cookies",
            "state": "TanStack Query v5 + nuqs (URL Search Params State Manager)",
            "validation": "Zod v3.23 (Client & Server Boundary Validation)",
            "testing": "Vitest + Playwright + MSW (Mock Service Worker)"
        },
        "nextjs": {
            "name": "Next.js 15 (App Router) + Prisma + PostgreSQL",
            "frontend": "Next.js 15 App Router (React 19) + Tailwind CSS + Shadcn UI + Lucide Icons",
            "backend": "Next.js Server Actions & Route Handlers (Edge & Node.js Runtime)",
            "database": "PostgreSQL 16 + Prisma ORM 5.x",
            "auth": "Auth.js (NextAuth v5) dengan JWT Session Token",
            "state": "React Server Components + TanStack Query v5",
            "validation": "Zod v3.23",
            "testing": "Vitest + Playwright"
        },
        "vite-spa": {
            "name": "Vite React SPA + Express.js API + SQLite/PostgreSQL",
            "frontend": "Vite 5 React + Tailwind CSS + Zustand + Lucide Icons",
            "backend": "Express.js 4.x (TypeScript) + CORS + Helmet + Rate Limit",
            "database": "PostgreSQL 16 / LibSQL SQLite + Drizzle ORM",
            "auth": "Custom JWT (Access Token 15m + Refresh Token 7d) via HTTP-Only Cookies",
            "state": "TanStack Query v5 + Zustand",
            "validation": "Zod v3.23",
            "testing": "Vitest + Supertest"
        }
    }
    stk = stack_configs.get(stack.lower(), stack_configs["tanstack"])

    personas = [
        {
            "role": f"Primary User ({target_audience})",
            "goal": f"Menyelesaikan kebutuhan terkait {clean_name} dengan cepat tanpa hambatan teknis.",
            "pain_points": [
                "Antarmuka yang rumit dan lambat dimuat di koneksi seluler.",
                "Kehilangan progres input saat browser di-refresh atau koneksi terputus.",
                "Ketidakjelasan status proses/transaksi saat melakukan aksi."
            ],
            "tech_level": "Menengah (terbiasa dengan browser mobile/desktop modern)."
        },
        {
            "role": "System Administrator / Operator",
            "goal": "Memantau kesehatan aplikasi, mengaudit entri data, dan mengelola hak akses pengguna.",
            "pain_points": [
                "Kesulitan melacak error log dan transaksi yang menggantung (orphaned records).",
                "Ketiadaan sistem audit log untuk aksi-aksi sensitif."
            ],
            "tech_level": "Tinggi (familiar dengan dashboard admin dan metrik sistem)."
        }
    ]

    if cat_key == "portfolio":
        features = [
            {
                "id": "F-01",
                "name": "Hero Section Interaktif & Profil Profesional",
                "desc": "Header profil personal dengan foto beranimasi halus, headline keahlian, status ketersediaan kerja (Open to Work), tombol Download CV (PDF), dan tautan sosial media (GitHub, LinkedIn, Instagram).",
                "user_story": f"Sebagai {target_audience}, saya ingin melihat ringkasan identitas, bio profesional, dan kontak agar dapat segera menilai kesesuaian profil kandidat.",
                "acceptance": [
                    "Animasi typing effect pada headline peran spesialisasi.",
                    "Tombol Download CV otomatis mengunduh resume PDF.",
                    "Tautan sosial media membuka tab baru dengan rel='noreferrer'."
                ],
                "error_cases": [
                    "File CV belum diunggah: tampilkan modal informasi kontak alternatif."
                ]
            },
            {
                "id": "F-02",
                "name": "Showcase Galeri Proyek & Filter Tech Stack",
                "desc": "Grid kartu portofolio proyek dengan filter tag kategori (Semua, Web, Mobile, AI/Backend), lightbox preview gambar, daftar badge teknologi, serta tautan Live Demo dan Source Code GitHub.",
                "user_story": f"Sebagai {target_audience}, saya ingin memfilter dan menginspeksi hasil karya nyata beserta teknologi yang digunakan.",
                "acceptance": [
                    "Filter instan kategori tanpa reload halaman.",
                    "Kartu proyek menampilkan thumbnail WebP responsif dan badge tech stack.",
                    "Tombol tautan 'Live Demo' dan 'GitHub' responsif dan valid."
                ],
                "error_cases": [
                    "Demo link tidak tersedia: nonaktifkan tombol dengan tooltip 'Private/NDA Proyek'."
                ]
            },
            {
                "id": "F-03",
                "name": "Matriks Keahlian Teknis (Skills) & Timeline Pengalaman",
                "desc": "Visualisasi tingkat penguasaan bahasa pemrograman / tools dengan persentase/level, daftar sertifikasi terverifikasi, dan garis waktu pengalaman kerja atau organisasi.",
                "user_story": f"Sebagai {target_audience}, saya ingin melihat kompetensi teknis dan rekam jejak pengalaman dalam format timeline yang mudah dipindai.",
                "acceptance": [
                    "Bar progress skill dengan animasi interaktif saat di-scroll ke viewport.",
                    "Timeline terstruktur urut kronologis terbalik (terbaru di posisi atas)."
                ],
                "error_cases": [
                    "Sertifikasi kadaluwarsa: tampilkan penanda status verifikasi kredensial."
                ]
            },
            {
                "id": "F-04",
                "name": "Formulir Kontak Pesan Cepat & Integrasi Notifikasi",
                "desc": "Formulir kirim pesan instan dengan validasi Zod (nama, email, subjek, pesan), notifikasi feedback toast, dan proteksi spam honeypot/rate limit.",
                "user_story": f"Sebagai {target_audience}, saya ingin mengirim pesan tawaran kerja atau kolaborasi langsung melalui website secara cepat.",
                "acceptance": [
                    "Validasi email dan panjang pesan minimal 10 karakter.",
                    "Feedback toast sukses instan dan form otomatis ter-reset.",
                    "Dukungan tombol direct WhatsApp sebagai alternatif cepat."
                ],
                "error_cases": [
                    "Pengiriman spam cepat: blokir submit dengan proteksi in-memory rate limit."
                ]
            }
        ]

        sql_ddl = """-- =====================================================================
-- DDL POSTGRESQL SCHEMA: PERSONAL PORTFOLIO & SHOWCASE PLATFORM
-- =====================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE profile (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(120) NOT NULL,
    headline VARCHAR(200) NOT NULL,
    bio TEXT NOT NULL,
    avatar_url TEXT,
    resume_url TEXT,
    location VARCHAR(100),
    is_available_for_hire BOOLEAN DEFAULT TRUE NOT NULL,
    social_links JSONB DEFAULT '{}' NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE project_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(80) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category_id UUID REFERENCES project_categories(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(250) UNIQUE NOT NULL,
    summary VARCHAR(300) NOT NULL,
    description TEXT NOT NULL,
    thumbnail_url TEXT NOT NULL,
    screenshots TEXT[] DEFAULT '{}' NOT NULL,
    tech_stack TEXT[] DEFAULT '{}' NOT NULL,
    demo_url TEXT,
    github_url TEXT,
    is_featured BOOLEAN DEFAULT FALSE NOT NULL,
    sort_order INT DEFAULT 0 NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(80) NOT NULL,
    category VARCHAR(60) NOT NULL,
    proficiency_level INT CHECK (proficiency_level BETWEEN 1 AND 100),
    icon_name VARCHAR(50)
);

CREATE TABLE contact_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_name VARCHAR(120) NOT NULL,
    sender_email VARCHAR(255) NOT NULL,
    subject VARCHAR(200),
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_projects_featured ON projects(is_featured);
CREATE INDEX idx_projects_category ON projects(category_id);
"""

        api_contracts = [
            {
                "method": "GET",
                "path": "/api/v1/projects",
                "auth": "Public",
                "desc": "Mengambil daftar portofolio proyek dengan filter kategori dan status featured.",
                "params": "category=web&featured=true",
                "response_200": {
                    "success": True,
                    "data": [
                        {
                            "id": "proj-1234-5678-90ab",
                            "title": "BikinPlan Platform",
                            "slug": "bikinplan-platform",
                            "summary": "Generator PRD & Task Backlog untuk AI coding agents",
                            "techStack": ["TanStack Start", "TypeScript", "Tailwind CSS", "PostgreSQL"],
                            "demoUrl": "https://bikinplan.com",
                            "githubUrl": "https://github.com/NnoeeL/BikinPlan"
                        }
                    ]
                }
            },
            {
                "method": "POST",
                "path": "/api/v1/contact",
                "auth": "Public (Rate-Limited)",
                "desc": "Mengirimkan formulir pesan kontak dari calon klien/recruiter.",
                "request_body": {
                    "senderName": "Sarah Jenkins",
                    "senderEmail": "sarah@techcorp.com",
                    "subject": "Invitation for Senior Frontend Opportunity",
                    "message": "Halo Farrel, kami terkesan dengan portofolio Anda dan ingin mendiskusikan peluang kolaborasi..."
                },
                "response_200": {
                    "success": True,
                    "message": "Pesan berhasil terkirim. Terima kasih!"
                }
            }
        ]

    elif cat_key == "ecommerce":
        features = [
            {
                "id": "F-01",
                "name": "Katalog Interaktif, Pencarian Fuzzy & Filtering Lanjutan",
                "desc": "Tampilan katalog produk/item dengan debounce search, filter kategori multi-pilihan, sorting harga/jarak, dan pagination responsif.",
                "user_story": f"Sebagai {target_audience}, saya ingin mencari dan memfilter item berdasarkan harga, lokasi, dan ketersediaan agar menemukan opsi paling sesuai dalam hitungan detik.",
                "acceptance": [
                    "Pencarian merespons real-time dengan debounce 300ms tanpa flicker UI.",
                    "Filter status dan kategori tersinkronisasi dua arah ke URL query params (nuqs).",
                    "Menampilkan skeleton loading placeholder saat fetching data dan empty state ilustratif jika hasil 0."
                ],
                "error_cases": [
                    "Koneksi offline: tampilkan banner reconnect dan gunakan cache data lokal terakhir.",
                    "Input karakter query berbahaya: sanitasi XSS otomatis pada input string."
                ]
            },
            {
                "id": "F-02",
                "name": "Halaman Detail Item, Galeri Gambar & Kalender Ketersediaan",
                "desc": "Detail spesifikasi lengkap, carousel galeri gambar terkompresi, status stok aktual, dan picker rentang tanggal peminjaman/booking.",
                "user_story": f"Sebagai {target_audience}, saya ingin melihat foto detail, fasilitas, dan ketersediaan jadwal agar dapat memutuskan pemesanan dengan yakin.",
                "acceptance": [
                    "Gambar menggunakan lazy loading dengan placeholder blur hash.",
                    "Validasi rentang tanggal: tanggal mulai tidak boleh di masa lalu dan tanggal akhir >= tanggal mulai.",
                    "Kalkulator biaya otomatis menghitung subtotal durasi sewa, biaya admin, dan total deposit."
                ],
                "error_cases": [
                    "Item sudah dibooking orang lain: tampilkan badge 'Tidak Tersedia' dan nonaktifkan tombol checkout."
                ]
            },
            {
                "id": "F-03",
                "name": "Alur Checkout, Form Pemesan & Integrasi Payment Gateway",
                "desc": "Form pemesanan terstruktur dengan validasi ketat, pemilihan metode pembayaran (QRIS / Virtual Account), dan penanganan webhook status.",
                "user_story": f"Sebagai {target_audience}, saya ingin melakukan checkout aman dan menerima instruksi pembayaran instan agar pesanan segera terkonfirmasi.",
                "acceptance": [
                    "Validasi formulir kontak pemesan (nama minimal 3 karakter, nomor WhatsApp valid format Indonesia +62/08).",
                    "Idempotency key pada request pembuatan transaksi untuk mencegah double charging.",
                    "Menampilkan popup Snap / QRIS modal serta timer countdown kedaluwarsa pembayaran."
                ],
                "error_cases": [
                    "Transaksi kedaluwarsa: status order otomatis diubah menjadi 'EXPIRED' dan stok dikembalikan."
                ]
            },
            {
                "id": "F-04",
                "name": "Dashboard Pelacakan Pesanan & Riwayat Transaksi",
                "desc": "Halaman pemantauan pesanan pengguna dengan badge status real-time, nota digital yang dapat diunduh, dan kontak darurat WhatsApp pemilik.",
                "user_story": f"Sebagai {target_audience}, saya ingin memantau status persetujuan pesanan dan mengunduh invoice digital sebagai bukti transaksi yang sah.",
                "acceptance": [
                    "Status pesanan ter-update otomatis (Pending, Paid, Active, Completed, Cancelled).",
                    "Tombol sekali klik menuju chat WhatsApp pengelola dengan pesan template otomatis terisi nomor order.",
                    "Fitur ekspor invoice/bukti pemesanan format PDF atau cetak bersih."
                ],
                "error_cases": [
                    "Pengguna mencoba mengakses pesanan milik user lain: kembalikan 403 Forbidden dengan pesan error yang aman."
                ]
            }
        ]

        sql_ddl = """-- =====================================================================
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
"""

        api_contracts = [
            {
                "method": "GET",
                "path": "/api/v1/items",
                "auth": "Public",
                "desc": "Mengambil daftar item dengan pagination, search query, dan filter multi-kategori.",
                "params": "page=1&limit=12&search=kemah&category=outdoor&minPrice=10000&maxPrice=150000&sort=price_asc",
                "response_200": {
                    "success": True,
                    "data": [
                        {
                            "id": "e4f8b910-1234-4567-89ab-cdef01234567",
                            "title": "Tenda Dome Kapasitas 4 Orang Waterproof",
                            "slug": "tenda-dome-kapasitas-4-orang",
                            "pricePerDay": 45000,
                            "availableStock": 3,
                            "category": "Tenda & Shelter",
                            "thumbnail": "https://example.com/images/tenda-1.jpg",
                            "facilities": ["Waterproof 3000mm", "Double Layer", "Alu Poles"]
                        }
                    ],
                    "pagination": { "page": 1, "limit": 12, "totalItems": 48, "totalPages": 4 }
                }
            },
            {
                "method": "POST",
                "path": "/api/v1/bookings",
                "auth": "Bearer Token / Session Cookie",
                "desc": "Membuat pesanan baru dan menerbitkan order token payment gateway.",
                "request_body": {
                    "itemId": "e4f8b910-1234-4567-89ab-cdef01234567",
                    "startDate": "2026-11-05",
                    "endDate": "2026-11-08",
                    "quantity": 1,
                    "customerNotes": "Diambil jam 9 pagi di sekretariat",
                    "paymentChannel": "qris"
                },
                "response_200": {
                    "success": True,
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
            }
        ]

    elif cat_key == "community":
        features = [
            {
                "id": "F-01",
                "name": "Feed Diskusi Interaktif & Filter Tagar/Fakultas",
                "desc": "Timeline feed real-time dengan tab Trending, Diskusi Terbaru, dan filter kategori mata kuliah atau fakultas.",
                "user_story": f"Sebagai {target_audience}, saya ingin melihat topik pembicaraan terhangat dan memfilter materi sesuai fakultas saya.",
                "acceptance": [
                    "Feed mendukung infinite scroll dengan virtualized list untuk performa 60 FPS.",
                    "Filter kategori langsung tercermin pada URL state tanpa full page reload.",
                    "Kartu postingan menampilkan badge waktu relatif ('5 menit yang lalu') dan penanda verified student."
                ],
                "error_cases": ["Gagal load post: tampilkan tombol 'Muat Ulang' dengan fallback cache lokal."]
            },
            {
                "id": "F-02",
                "name": "Editor Thread Markdown & Lampiran Dokumen/Gambar",
                "desc": "Rich text markdown editor dengan live preview split-view, upload lampiran aman, dan opsi posting anonim beretika.",
                "user_story": f"Sebagai {target_audience}, saya ingin menulis pertanyaan atau catatan kuliah lengkap dengan cuplikan kode dan gambar.",
                "acceptance": [
                    "Sanitasi markdown ketat (DOMPurify) untuk mencegah injeksi script berbahaya.",
                    "Kompresi gambar di browser pengguna sebelum upload (WebP, max 1.5MB).",
                    "Draf otomatis tersimpan di localStorage setiap 3 detik mencegah kehilangan tulisan."
                ],
                "error_cases": ["Upload melebihi kuota 5 file: tampilkan notifikasi validasi inline."]
            },
            {
                "id": "F-03",
                "name": "Sistem Komentar Beranak (Threaded), Reaksi & Upvoting",
                "desc": "Komentar bersarang (max 3 kedalaman), sistem upvote dengan proteksi anti-spam, dan penandaan solusi terbaik oleh pembuat thread.",
                "user_story": f"Sebagai {target_audience}, saya ingin berdiskusi di bawah komentar tertentu dan memberikan upvote pada jawaban yang benar.",
                "acceptance": [
                    "Optimistic UI update saat menekan tombol upvote (angka langsung naik tanpa menunggu server).",
                    "Pembuat pertanyaan dapat menyematkan satu komentar sebagai 'Jawaban Terbaik' (Best Solution).",
                    "Notifikasi badge real-time jika ada balasan baru pada thread yang diikuti."
                ],
                "error_cases": ["Pengguna mencoba upvote dua kali: mutasi toggle otomatis mengurangi nilai."]
            },
            {
                "id": "F-04",
                "name": "Manajemen Reputasi, Poin Kontributor & Moderasi Konten",
                "desc": "Perhitungan poin keaktifan, pelaporan konten bermasalah, dan dashboard audit moderasi untuk admin komunitas.",
                "user_story": f"Sebagai {target_audience}, saya ingin mendapatkan pengakuan reputasi dan melaporkan konten yang melanggar norma komunitas.",
                "acceptance": [
                    "Poin reputasi bertambah otomatis saat jawaban ditandai sebagai Best Answer (+15 pts).",
                    "Fitur 'Laporkan Konten' dengan pilihan alasan pelanggaran.",
                    "Admin dapat menyembunyikan thread dan membekukan user yang melanggar aturan."
                ],
                "error_cases": ["Post dilaporkan > 5 user berbeda: otomatis disembunyikan sementara menunggu review admin."]
            }
        ]

        sql_ddl = """-- =====================================================================
-- DDL POSTGRESQL SCHEMA: CAMPUS COMMUNITY & DISCUSSION PLATFORM
-- =====================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    student_id VARCHAR(50),
    faculty VARCHAR(100),
    reputation_score INT DEFAULT 0 NOT NULL,
    role VARCHAR(20) DEFAULT 'member' NOT NULL,
    avatar_url TEXT,
    bio VARCHAR(250),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE channels (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(80) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(40),
    is_private BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE TABLE threads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    channel_id UUID NOT NULL REFERENCES channels(id) ON DELETE CASCADE,
    author_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(250) NOT NULL,
    slug VARCHAR(300) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    is_anonymous BOOLEAN DEFAULT FALSE NOT NULL,
    is_pinned BOOLEAN DEFAULT FALSE NOT NULL,
    is_solved BOOLEAN DEFAULT FALSE NOT NULL,
    solved_comment_id UUID,
    upvotes_count INT DEFAULT 0 NOT NULL,
    comments_count INT DEFAULT 0 NOT NULL,
    views_count INT DEFAULT 0 NOT NULL,
    attachments TEXT[] DEFAULT '{}' NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_threads_channel ON threads(channel_id);
CREATE INDEX idx_threads_author ON threads(author_id);
CREATE INDEX idx_threads_upvotes ON threads(upvotes_count DESC);
CREATE INDEX idx_threads_created ON threads(created_at DESC);
"""

        api_contracts = [
            {
                "method": "GET",
                "path": "/api/v1/threads",
                "auth": "Public",
                "desc": "Mengambil feed thread diskusi dengan filter channel dan sorting.",
                "params": "channel=informatika&sort=trending&page=1&limit=20",
                "response_200": {
                    "success": True,
                    "data": [
                        {
                            "id": "c1f2a3b4-5566-7788-99aa-bbccddeeff00",
                            "title": "Tips Lolos Mata Kuliah Algoritma Pemrograman Semester 1",
                            "slug": "tips-lolos-mata-kuliah-algoritma-pemrograman",
                            "author": { "username": "farrel_code", "displayName": "Farrel Noel", "reputation": 140 },
                            "channel": "Informatika",
                            "upvotesCount": 42,
                            "commentsCount": 18,
                            "createdAt": "2026-10-25T14:20:00Z"
                        }
                    ]
                }
            }
        ]

    else:
        features = [
            {
                "id": "F-01",
                "name": "Dashboard Metrik Finansial & Grafik Analisis Tren",
                "desc": "Visualisasi metrik arus kas, ringkasan saldo neto, perbandingan pengeluaran bulanan, dan breakdown kategori via interactive chart.",
                "user_story": f"Sebagai {target_audience}, saya ingin melihat ringkasan keuangan dalam satu layar agar mengetahui kondisi finansial tanpa kalkulasi manual.",
                "acceptance": [
                    "KPI Card menampilkan Pemasukan, Pengeluaran, Saldo Bersih, dan persentase perubahan vs bulan lalu.",
                    "Grafik bar/line interaktif dengan tooltip detail harian yang cepat dimuat.",
                    "Selector filter tanggal (Bulan Ini, 3 Bulan Terakhir, Tahun Ini, Custom Range)."
                ],
                "error_cases": ["Data bulan baru kosong: tampilkan ilustrasi empty state dan ajakan 'Catat Transaksi Pertama'."]
            },
            {
                "id": "F-02",
                "name": "Pencatatan Transaksi Cepat & Modal Input Cerdas",
                "desc": "Formulir pencatatan pemasukan/pengeluaran cepat dengan shortcut keyboard, auto-suggest kategori, dan tagar pengelompokan.",
                "user_story": f"Sebagai {target_audience}, saya ingin mencatat pengeluaran dalam < 5 detik agar tidak menunda-nunda pencatatan harian.",
                "acceptance": [
                    "Modal input dapat dipicu dengan shortcut keyboard `Shift + N`.",
                    "Format angka otomatis menjadi mata uang IDR (`Rp 50.000`) saat pengguna mengetik angka.",
                    "Auto-kategori cerdas berdasarkan kata kunci (contoh: 'makan siang' -> Kategori: Makanan)."
                ],
                "error_cases": ["Nominal 0 atau negatif: cegah submit dan tampilkan instruksi 'Nominal harus lebih dari 0'."]
            },
            {
                "id": "F-03",
                "name": "Manajemen Anggaran (Budgeting) & Notifikasi Limit",
                "desc": "Alokasi anggaran maksimal per kategori pengeluaran dengan progress bar warna (Aman/Peringatan/Overbudget) dan peringatan dini.",
                "user_story": f"Sebagai {target_audience}, saya ingin menetapkan pagu anggaran bulanan per kategori agar tidak boros.",
                "acceptance": [
                    "Progress bar persentase konsumsi budget (Hijau < 70%, Kuning 70-90%, Merah > 90%).",
                    "Peringatan toast otomatis saat transaksi baru menyebabkan kategori melewati kuota anggaran.",
                    "Ringkasan sisa anggaran harian yang aman untuk dibelanjakan (daily burn rate)."
                ],
                "error_cases": ["Target budget tidak realistis: sistem memberikan kalkulasi rata-rata historis sebagai acuan."]
            },
            {
                "id": "F-04",
                "name": "Laporan Rekapitulasi & Ekspor Dokumen Multi-Format",
                "desc": "Penyusunan laporan pembukuan formal dengan filter rentang waktu dan ekspor bersih ke format PDF cetak, Excel XLSX, atau CSV.",
                "user_story": f"Sebagai {target_audience}, saya ingin mengekspor rekapan transaksi ke PDF dan Excel untuk keperluan pembukuan pribadi atau klaim reimburse.",
                "acceptance": [
                    "Ekspor PDF menghasilkan tata letak tabel formal, nomor halaman, dan header ringkasan total.",
                    "Ekspor CSV menggunakan delimiter standar dengan enkripsi UTF-8 aman.",
                    "Proses unduh berjalan asinkron di background tanpa memblokir antarmuka pengguna."
                ],
                "error_cases": ["Rentang tanggal > 365 hari: sediakan streaming download untuk menghemat memori."]
            }
        ]

        sql_ddl = """-- =====================================================================
-- DDL POSTGRESQL SCHEMA: SAAS & FINANCIAL TRACKING PLATFORM
-- =====================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE transaction_type AS ENUM ('income', 'expense', 'transfer');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(120) NOT NULL,
    avatar_url TEXT,
    currency VARCHAR(10) DEFAULT 'IDR' NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(120) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(80) NOT NULL,
    type transaction_type NOT NULL,
    icon_name VARCHAR(50) DEFAULT 'tag',
    color_hex VARCHAR(20) DEFAULT '#FF5C20',
    monthly_budget NUMERIC(14, 2) DEFAULT 0.00,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE (workspace_id, name, type)
);

CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    type transaction_type NOT NULL,
    amount NUMERIC(14, 2) NOT NULL CHECK (amount > 0),
    title VARCHAR(200) NOT NULL,
    notes TEXT,
    transaction_date DATE NOT NULL,
    receipt_url TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_transactions_workspace ON transactions(workspace_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_category ON transactions(category_id);
"""

        api_contracts = [
            {
                "method": "GET",
                "path": "/api/v1/analytics/summary",
                "auth": "Session Cookie / Bearer",
                "desc": "Mengambil agregasi total pemasukan, pengeluaran, saldo bersih, dan metrik budget periode tertentu.",
                "params": "workspaceId=ws-123&startDate=2026-10-01&endDate=2026-10-31",
                "response_200": {
                    "success": True,
                    "data": {
                        "totalIncome": 8500000,
                        "totalExpense": 4250000,
                        "netSavings": 4250000,
                        "savingsRatePercentage": 50.0,
                        "comparisonPreviousMonth": { "expenseChangePercentage": -12.4 }
                    }
                }
            }
        ]

    ui_state_matrix = [
        {
            "screen": "Halaman Utama & Katalog / Dashboard",
            "empty": "Tampilkan kartu ilustrasi kosong dengan tombol ajakan utama (CTA) untuk membuat entri data perdana.",
            "loading": "Gunakan shimmer skeleton layout yang mencerminkan bentuk kartu/tabel sebenarnya (bukan sekadar spinner putar).",
            "error": "Tampilkan banner error dengan tombol 'Coba Lagi' dan kode pelacak insiden.",
            "success": "Animasi fade-in halus 300ms saat data berhasil ditarik dari server."
        },
        {
            "screen": "Modal Form Input & Editor",
            "empty": "Form terisi nilai default yang masuk akal (tanggal hari ini, kategori teratas).",
            "loading": "Tombol simpan menampilkan spinner mini dan teks 'Menyimpan...', semua input dinonaktifkan sementara.",
            "error": "Pesan error validasi berwarna merah tepat di bawah field input yang bermasalah (inline error).",
            "success": "Modal menutup otomatis, form reset, dan memunculkan toast notifikasi sukses berwarna hijau di kanan bawah."
        }
    ]

    nfr_list = [
        "Performa: First Contentful Paint (FCP) < 1.2 detik dan Time to Interactive (TTI) < 2.0 detik pada koneksi 4G standar.",
        "Keamanan: Proteksi terhadap SQL Injection via parameterized queries di Drizzle/Prisma, sanitasi output XSS, dan cookie HttpOnly SameSite=Lax.",
        "Rate Limiting: Pembatasan 100 request / menit per IP untuk endpoint publik guna mencegah DDoS dan brute-force.",
        "Aksesibilitas (a11y): Kontras warna rasio minimal 4.5:1 (WCAG AA), navigasi penuh via tombol keyboard (Tab/Enter/Escape), dan label ARIA pada komponen interaktif.",
        "Irit Token & Modularitas: Komponen dipecah dalam modularitas file < 250 baris untuk mempermudah AI agent membaca dan menyunting kode."
    ]

    tasks = [
        {
            "ref": "T-01", "phase": 1, "layer": "frontend",
            "title": "Setup Repository, Standarisasi TypeScript, dan Konfigurasi Tailwind Tokens",
            "desc": "Inisialisasi repo dengan konfigurasi TypeScript ketat, Tailwind CSS design tokens (warna primer, neutral, card, border), dan linter rules.",
            "checklist": [
                "Inisialisasi project sesuai tech stack pilihan",
                "Konfigurasi tailwind.config.ts dengan palet warna dan font 'Plus Jakarta Sans'",
                "Tambahkan skrip lint, type-check, dan format di package.json",
                "Verifikasi build awal berjalan lancar tanpa error type"
            ],
            "files": ["package.json", "tailwind.config.ts", "tsconfig.json", "src/styles/globals.css"],
            "acceptance": "Jalankan `npm run build` dan `npm run lint`. Keduanya berhasil 100% tanpa warning/error."
        },
        {
            "ref": "T-02", "phase": 1, "layer": "frontend",
            "title": "Layout Shell Responsif: Navbar, Sidebar, dan Dark/Light Mode Switcher",
            "desc": "Bangun tata letak aplikasi dengan navigasi responsif (desktop bar & mobile drawer) serta toggle tema dengan penyimpanan localStorage.",
            "checklist": [
                "Buat komponen Header dengan logo SVG dan menu navigasi",
                "Buat navigasi mobile drawer yang mulus saat dibuka pada layar kecil",
                "Implementasikan dark mode switcher dengan deteksi prefers-color-scheme sistem",
                "Pasang layout wrapper utama yang membatasi max-width konten 1200px"
            ],
            "files": ["src/components/layout/Header.tsx", "src/components/layout/ThemeToggle.tsx", "src/components/layout/AppShell.tsx"],
            "acceptance": "Buka browser pada resolusi desktop dan mobile (F12 mobile view). Tampilan proporsional, tema tersimpan saat refresh."
        },
        {
            "ref": "T-03", "phase": 1, "layer": "frontend",
            "title": f"Pembuatan Fixture Mock Data & State Tiruan untuk {features[0]['name']}",
            "desc": "Tulis data tiruan realistis dalam file terisolasi untuk merepresentasikan entitas utama tanpa ketergantungan koneksi backend.",
            "checklist": [
                "Definisikan TypeScript interface untuk entitas utama",
                "Buat minimal 8 baris mock data realistis mencakup berbagai variasi status",
                "Buat helper fungsi tiruan pencarian dan filter lokal di memori"
            ],
            "files": ["src/types/domain.ts", "src/data/mockFixtures.ts"],
            "acceptance": "Impor fixture ke unit test atau console: data tervalidasi sesuai tipe TypeScript."
        },
        {
            "ref": "T-04", "phase": 1, "layer": "frontend",
            "title": f"Tampilan Halaman Utama {features[0]['name']} Berbasis Data Mock",
            "desc": "Buat komponen presentasi kartu/tabel dengan search input, filter pill kategori, dan status indikator menggunakan mock data.",
            "checklist": [
                "Buat komponen Card / Grid item yang menarik dan responsif",
                "Pasang input pencarian dengan debounce 300ms",
                "Tambahkan tombol filter kategori visual",
                "Pasang komponen Shimmer Skeleton placeholder saat transisi"
            ],
            "files": ["src/pages/CatalogPage.tsx", "src/components/catalog/ItemCard.tsx", "src/components/catalog/ItemSkeleton.tsx"],
            "acceptance": "Buka halaman di browser: kartu produk/item muncul instan. Mengetik di search bar memfilter item secara langsung."
        },
        {
            "ref": "T-05", "phase": 1, "layer": "frontend",
            "title": f"Tampilan Halaman Rincian untuk {features[1]['name']} (Detail View)",
            "desc": "Bangun halaman detail item dengan galeri preview, rincian spesifikasi, kalkulasi ringkas biaya, dan tombol aksi pemesanan.",
            "checklist": [
                "Buat halaman detail dinamis dengan routing slug/id",
                "Tampilkan spesifikasi, fasilitas, dan status ketersediaan",
                "Buat komponen ringkasan harga dan tombol call-to-action (CTA)"
            ],
            "files": ["src/pages/ItemDetailPage.tsx", "src/components/detail/PriceSummaryCard.tsx"],
            "acceptance": "Klik salah satu item dari halaman utama: browser berpindah ke halaman detail dengan konten yang sesuai."
        },
        {
            "ref": "T-06", "phase": 1, "layer": "frontend",
            "title": "Komponen Modal Dialog & Formulir Input Interaktif dengan Validasi Zod",
            "desc": "Bangun dialog modal responsif untuk pembuatan entri baru atau booking, dilengkapi pesan kesalahan validasi ramah pengguna.",
            "checklist": [
                "Buat reusable Modal Dialog berbasis Radix UI Primitives",
                "Definisikan skema validasi form dengan Zod",
                "Tampilkan pesan error validasi inline di bawah input yang tidak valid",
                "Simulasikan submit berhasil dengan memunculkan toast notifikasi"
            ],
            "files": ["src/components/ui/Modal.tsx", "src/components/forms/EntryFormModal.tsx", "src/schemas/formSchema.ts"],
            "acceptance": "Buka modal, tekan submit saat kosong -> muncul pesan error. Isi data valid -> modal tertutup dan toast sukses muncul."
        },
        {
            "ref": "T-07", "phase": 2, "layer": "frontend",
            "title": "Sinkronisasi State URL Query Parameters (Filter, Search & Pagination)",
            "desc": "Gunakan URL search params sebagai single source of truth untuk filter dan pagination agar halaman mudah dibagikan (shareable).",
            "checklist": [
                "Integrasikan nuqs atau custom useSearchParams hook",
                "Sinkronkan nilai search, category, dan page ke parameter query URL",
                "Pastikan tombol navigasi browser 'Back' dan 'Forward' mengembalikan state filter dengan benar"
            ],
            "files": ["src/hooks/useCatalogFilters.ts", "src/pages/CatalogPage.tsx"],
            "acceptance": "Salin URL setelah memfilter data, buka di tab baru: filter dan hasil pencarian yang sama langsung terbuka."
        },
        {
            "ref": "T-08", "phase": 2, "layer": "frontend",
            "title": "Local Store Management & CRUD Client-Side di Memori",
            "desc": "Implementasikan state store lokal (Zustand / Context) sehingga aksi tambah, ubah, dan hapus data langsung tercermin di UI.",
            "checklist": [
                "Inisialisasi app store untuk menampung entri data di client",
                "Tambahkan fungsi Create, Update, dan Delete di memori",
                "Simpan perubahan ke localStorage agar data tidak hilang saat refresh"
            ],
            "files": ["src/store/useAppStore.ts"],
            "acceptance": "Buat entri baru via form modal: entri langsung muncul di daftar. Refresh halaman: data baru tetap ada."
        },
        {
            "ref": "T-09", "phase": 2, "layer": "frontend",
            "title": "Komponen Empty State, Error Boundary, dan Toast System",
            "desc": "Lengkapi aplikasi dengan sistem toast notifikasi mandiri, kartu penanganan data kosong, dan batas penangkap error runtime.",
            "checklist": [
                "Buat Toast Provider dan helper `showToast(title, type)`",
                "Buat komponen EmptyState dengan tombol CTA terarah",
                "Pasang React ErrorBoundary untuk mencegah layar putih saat terjadi crash"
            ],
            "files": ["src/components/ui/Toast.tsx", "src/components/ui/EmptyState.tsx", "src/components/ErrorBoundary.tsx"],
            "acceptance": "Filter data dengan kata kunci ngawur: muncul Empty State yang rapi dengan tombol 'Reset Filter'."
        },
        {
            "ref": "T-10", "phase": 2, "layer": "frontend",
            "title": "Sistem Verifikasi Checkpoint Fase 1 & 2 (Frontend Review)",
            "desc": "Audit menyeluruh terhadap seluruh antarmuka sebelum berpindah ke layer backend dan database.",
            "checklist": [
                "Uji coba seluruh alur navigasi dari awal hingga akhir",
                "Periksa responsivitas pada layar ponsel (360px) dan laptop",
                "Pastikan tidak ada error console JavaScript atau warning missing keys"
            ],
            "files": ["src/tests/ui-flow.test.ts"],
            "acceptance": "Semua fungsionalitas UI dapat diuji secara interaktif tanpa backend dan siap disambungkan ke API."
        },
        {
            "ref": "T-11", "phase": 3, "layer": "database",
            "title": "Penyusunan Skema Database Drizzle / Prisma & Konfigurasi Koneksi",
            "desc": "Tulis definisi tabel database resmi lengkap dengan foreign key, index pencarian, dan konfigurasi connection pool.",
            "checklist": [
                "Buat file skema database sesuai DDL yang dirancang di PRD",
                "Konfigurasi connection pool ke database PostgreSQL",
                "Setup script migration di package.json (`npm run db:push` / `npm run db:migrate`)"
            ],
            "files": ["src/db/schema.ts", "src/db/index.ts", "drizzle.config.ts"],
            "acceptance": "Jalankan perintah migrasi: koneksi database sukses dan tabel terbuat lengkap dengan tipe datanya."
        },
        {
            "ref": "T-12", "phase": 3, "layer": "database",
            "title": "Script Seeding Database Awal untuk Lingkungan Development",
            "desc": "Tulis script seed otomatis untuk mengisi database dengan data kategori dan entri uji coba.",
            "checklist": [
                "Tulis script seed.ts yang idempotent (tidak duplikat saat dijalankan ulang)",
                "Isi data kategori dasar dan contoh entri realistis",
                "Verifikasi hasil seed lewat database client atau query SELECT"
            ],
            "files": ["src/db/seed.ts"],
            "acceptance": "Jalankan `npm run db:seed`: database terisi record uji coba yang siap dipakai."
        },
        {
            "ref": "T-13", "phase": 3, "layer": "backend",
            "title": "Setup Autentikasi Pengguna & Session Cookie Handler",
            "desc": "Implementasikan sistem autentikasi (Better Auth / NextAuth / JWT) dengan proteksi cookie HttpOnly.",
            "checklist": [
                "Konfigurasi auth provider dengan Google OAuth dan email password",
                "Buat endpoint sign-in, sign-up, sign-out, dan get session",
                "Simpan user baru secara otomatis ke tabel database saat pertama login"
            ],
            "files": ["src/auth.ts", "src/routes/api/auth.ts"],
            "acceptance": "Uji login via form atau OAuth: session token tersimpan di cookie dan endpoint auth/session mengembalikan data profil."
        },
        {
            "ref": "T-14", "phase": 3, "layer": "backend",
            "title": "Middleware Auth Guard & Verifikasi Role Hak Akses",
            "desc": "Pasang middleware untuk memproteksi rute API sensitif dari akses tanpa token autentikasi.",
            "checklist": [
                "Buat middleware guard yang membaca session dari header/cookie",
                "Tolak request tanpa auth dengan HTTP 401 Unauthorized",
                "Buat guard khusus role admin yang mengembalikan HTTP 403 Forbidden jika role tidak sesuai"
            ],
            "files": ["src/middleware/authGuard.ts"],
            "acceptance": "Akses endpoint privat tanpa login -> tertolak 401. Akses dengan session valid -> request diteruskan."
        },
        {
            "ref": "T-15", "phase": 3, "layer": "backend",
            "title": "REST API: Endpoint GET List dengan Pagination, Search & Filter",
            "desc": "Bangun endpoint GET untuk mengambil data dengan validasi query params Zod, pagination offset/limit, dan SQL index query.",
            "checklist": [
                "Validasi query parameter (search, category, page, limit) via Zod",
                "Eksekusi query database dengan kalkulasi total halaman dan total record",
                "Kembalikan response JSON terstandarisasi `{ success: true, data: [...], pagination: {...} }`"
            ],
            "files": ["src/routes/api/items.get.ts", "src/controllers/itemController.ts"],
            "acceptance": "Uji via curl: `GET /api/v1/items?limit=5` mengembalikan tepat 5 record dan metadata pagination."
        },
        {
            "ref": "T-16", "phase": 3, "layer": "backend",
            "title": "REST API: Endpoint GET Detail Berdasarkan ID / Slug",
            "desc": "Endpoint untuk mengambil informasi spesifik satu entitas dengan penanganan 404 jika tidak ditemukan.",
            "checklist": [
                "Validasi parameter ID (UUID) atau slug",
                "Query join dengan relasi kategori dan pemilik data",
                "Kembalikan 404 Not Found dengan pesan jelas jika ID tidak ada di database"
            ],
            "files": ["src/routes/api/items.detail.ts"],
            "acceptance": "Request ID valid mengembalikan objek lengkap. Request ID acak mengembalikan status 404."
        },
        {
            "ref": "T-17", "phase": 3, "layer": "backend",
            "title": "REST API: Endpoint POST Pembuatan Data Baru & Validasi Payload",
            "desc": "Endpoint POST dengan validasi skema body Zod, sanitasi string dari injeksi, dan penyimpanan transaksi database.",
            "checklist": [
                "Validasi body request menggunakan skema Zod ketat",
                "Kaitkan data baru dengan ID user yang sedang login dari session",
                "Kembalikan response HTTP 201 Created dengan data yang baru dibuat"
            ],
            "files": ["src/routes/api/items.post.ts"],
            "acceptance": "Kirim payload tidak lengkap -> respons 422 Unprocessable Entity. Kirim payload valid -> data tersimpan di DB."
        },
        {
            "ref": "T-18", "phase": 3, "layer": "backend",
            "title": "REST API: Endpoint PATCH/PUT Update dan DELETE Soft-Delete",
            "desc": "Endpoint pembaruan data dan penghapusan dengan verifikasi hak milik data (hanya pembuat/admin yang boleh mengubah).",
            "checklist": [
                "Verifikasi bahwa user yang login adalah pemilik record atau role admin",
                "Implementasikan pembaruan parsial (PATCH)",
                "Implementasikan soft-delete atau penghapusan aman"
            ],
            "files": ["src/routes/api/items.mutate.ts"],
            "acceptance": "User A mencoba mengubah data milik User B -> tertolak 403 Forbidden. User A mengubah data sendiri -> sukses 200 OK."
        },
        {
            "ref": "T-19", "phase": 4, "layer": "integration",
            "title": "Setup API Client & TanStack Query Provider di Frontend",
            "desc": "Buat wrapper HTTP client (fetch/axios) terpusat dengan penanganan kredensial cookie otomatis dan interceptor error.",
            "checklist": [
                "Konfigurasi Base URL dan default headers di API client",
                "Pasang interceptor respons untuk menangani 401 (redirect ke login) secara global",
                "Konfigurasi TanStack QueryClient dengan retry policy yang cerdas"
            ],
            "files": ["src/api/client.ts", "src/providers/QueryProvider.tsx"],
            "acceptance": "QueryClient terpasang di root aplikasi tanpa error re-render ganda."
        },
        {
            "ref": "T-20", "phase": 4, "layer": "integration",
            "title": "Wiring Frontend: Gantikan Mock Data dengan Query API Riil",
            "desc": "Sambungkan komponen katalog dan detail view ke custom hook `useQuery` yang menarik data asli dari database.",
            "checklist": [
                "Buat hook `useItemsQuery` dan `useItemDetailQuery`",
                "Gantikan sumber data mock di halaman utama dengan hasil query API",
                "Pastikan skeleton loader menyala selama fetching data dari server"
            ],
            "files": ["src/hooks/useItemsQuery.ts", "src/pages/CatalogPage.tsx"],
            "acceptance": "Buka tab Network di browser: terlihat request `GET /api/v1/items` dan data dari PostgreSQL ter-render di UI."
        },
        {
            "ref": "T-21", "phase": 4, "layer": "integration",
            "title": "Wiring Mutasi: Form Submit & Optimistic UI Update",
            "desc": "Sambungkan form modal ke `useMutation` untuk menyimpan data langsung ke server dengan invalidasi cache otomatis.",
            "checklist": [
                "Buat hook `useCreateItemMutation`",
                "Gantikan submit tiruan form dengan mutasi API nyata",
                "Trigger `queryClient.invalidateQueries` setelah mutasi berhasil agar list ter-update otomatis"
            ],
            "files": ["src/hooks/useItemMutations.ts", "src/components/forms/EntryFormModal.tsx"],
            "acceptance": "Submit form baru di browser: baris baru tersimpan di database dan langsung muncul di list tanpa perlu reload halaman."
        },
        {
            "ref": "T-22", "phase": 4, "layer": "polish",
            "title": "Audit Keamanan Trust Boundary, Sanitasi Input, dan Rate Limiting",
            "desc": "Audit keamanan aplikasi: periksa celah XSS, pastikan CORS hanya mengizinkan origin terpercaya, dan pasang rate limiting.",
            "checklist": [
                "Pasang security headers (Helmet / CSP)",
                "Uji coba input string berbahaya `<script>alert(1)</script>` untuk memastikan output tersanitasi aman",
                "Pasang in-memory rate limiting pada endpoint publik"
            ],
            "files": ["src/server/security.ts"],
            "acceptance": "Lakukan spam request > 100 kali berturut-turut: server mengembalikan HTTP 429 Too Many Requests."
        },
        {
            "ref": "T-23", "phase": 4, "layer": "polish",
            "title": "Optimasi SEO, OpenGraph Meta Tags, dan PWA Manifest",
            "desc": "Lengkapi metadata sosial media, gambar pratinjau OG image, dan konfigurasi Web App Manifest untuk instalasi mobile.",
            "checklist": [
                "Tambahkan OpenGraph (og:title, og:description, og:image) dan Twitter Cards",
                "Buat file manifest.json dan konfigurasi favicon beragam ukuran",
                "Pastikan canonical URL terpasang dengan benar di setiap rute"
            ],
            "files": ["src/app/metadata.ts", "public/manifest.json"],
            "acceptance": "Uji via pratinjau meta tag: thumbnail dan deskripsi situs muncul rapi saat dibagikan."
        },
        {
            "ref": "T-24", "phase": 4, "layer": "polish",
            "title": "Verifikasi Akhir Build Production & Smoke Test Mandiri",
            "desc": "Jalankan build produksi akhir, cek ukuran bundle JS, dan lakukan smoke test komprehensif seluruh alur aplikasi.",
            "checklist": [
                "Jalankan `npm run build` dan verifikasi bundle size budget (< 150KB initial JS)",
                "Jalankan smoke test: pendaftaran user -> login -> buat entri data -> filter/search -> logout",
                "Pastikan aplikasi 100% siap untuk deployment produksi"
            ],
            "files": ["package.json"],
            "acceptance": "Hasil build production lolos tanpa error type. Seluruh alur kerja teruji dan berfungsi sempurna."
        }
    ]

    return {
        "name": clean_name,
        "slug": slug,
        "idea": idea,
        "categoryKey": cat_key,
        "categoryTitle": cat_title,
        "targetAudience": target_audience,
        "stack": stk,
        "personas": personas,
        "features": features,
        "sqlDdl": sql_ddl,
        "apiContracts": api_contracts,
        "uiStateMatrix": ui_state_matrix,
        "nfrList": nfr_list,
        "tasks": tasks
    }

def generate_prd_markdown(plan: Dict[str, Any]) -> str:
    p = plan
    s = p["stack"]
    
    personas_md = ""
    for idx, per in enumerate(p["personas"], 1):
        pain_list = "\n".join([f"    - {pn}" for pn in per["pain_points"]])
        personas_md += f"""#### Persona {idx}: {per['role']}
- **Tujuan Utama:** {per['goal']}
- **Tingkat Kemahiran Digital:** {per['tech_level']}
- **Kendala Utama (Pain Points):**
{pain_list}

"""

    features_md = ""
    for f in p["features"]:
        acc_list = "\n".join([f"  - [ ] {a}" for a in f["acceptance"]])
        err_list = "\n".join([f"  - ⚠️ *Edge Case:* {e}" for e in f["error_cases"]])
        features_md += f"""### [{f['id']}] {f['name']}
- **Ringkasan Fungsi:** {f['desc']}
- **User Story:** {f['user_story']}
- **Kriteria Penerimaan (Acceptance Criteria):**
{acc_list}
- **Penanganan Kondisi Khusus & Error:**
{err_list}

"""

    ui_matrix_md = "| Layar / Komponen | Empty State | Loading State | Error State | Success State |\n| :--- | :--- | :--- | :--- | :--- |\n"
    for row in p["uiStateMatrix"]:
        ui_matrix_md += f"| **{row['screen']}** | {row['empty']} | {row['loading']} | {row['error']} | {row['success']} |\n"

    api_md = ""
    for api in p["apiContracts"]:
        req_body = json.dumps(api.get("request_body"), indent=2) if api.get("request_body") else "Tidak membutuhkan request body (GET)."
        res_body = json.dumps(api.get("response_200"), indent=2)
        params_str = f"`{api.get('params')}`" if api.get('params') else "None"
        api_md += f"""#### `{api['method']}` {api['path']}
- **Deskripsi:** {api['desc']}
- **Hak Akses:** `{api['auth']}`
- **Query Parameters:** {params_str}
- **Request Body (JSON):**
```json
{req_body}
```
- **Response Payload (HTTP 200 OK):**
```json
{res_body}
```

---
"""

    nfr_md = "\n".join([f"{idx}. {item}" for idx, item in enumerate(p["nfrList"], 1)])

    return f"""# Product Requirement Document (PRD)
## {p['name']} — Spesifikasi Rekayasa Sistem

> **Versi:** 1.2.0 (Production-Grade Enriched)  
> **Status Dokumen:** Approved for Autonomous Agent Implementation  
> **Kategori:** {p['categoryTitle']}  
> **Target Pengguna:** {p['targetAudience']}  
> **Arsitektur Acuan:** {s['name']}  

---

## 1. Ringkasan Eksekutif & Problem Statement

### 1.1 Latar Belakang Masalah
Kebutuhan pengguna yang mendasari proyek ini:
> "{p['idea']}"

Banyak pengguna dalam kategori **{p['targetAudience']}** menghadapi kendala alur kerja manual, fragmentasi informasi, dan antarmuka lambat yang menyita waktu produktif. Aplikasi **{p['name']}** dirancang sebagai solusi terpadu yang memadukan kecepatan muat, antarmuka minimalis tanpa friksi, dan arsitektur *type-safe* dari database hingga komponen layar.

### 1.2 Tujuan Utama Proyek (Key Performance Indicators)
1. **Kecepatan Akses & Interaksi:** Waktu muat awal (First Contentful Paint) < 1.2 detik dan penyelesaian alur kerja utama pengguna dalam kurang dari 3 kali klik.
2. **Keandalan & Zero Data Loss:** Semua formulir dan interaksi penting memiliki validasi batas ganda (*client-side* dan *server-side*) serta proteksi draf lokal di browser.
3. **Optimasi AI Coding Agent:** Struktur kode dirancang modular dan berbasis konvensi baku (*boring over clever*), meminimalkan konsumsi context token saat dikembangkan oleh agen seperti Claude Code, Hermes, atau Cursor.

---

## 2. Profil Pengguna & User Personas

{personas_md}

---

## 3. Arsitektur Teknis & Tech Stack

### 3.1 Alur Kerja 4-Fase Sistem (Architecture Flowchart)
```mermaid
{generate_mermaid_flowchart(p)}
```

### 3.2 Matriks Komponen Teknologi
| Lapisan Sistem | Teknologi Pilihan | Alasan Pemilihan & Manfaat Teknis |
| :--- | :--- | :--- |
| **Framework Utama** | {s['frontend']} | Rendering cepat berbasis SSR/Hydration, ekosistem standar industri, dan navigasi instan. |
| **Server Engine** | {s['backend']} | Menangani Server Functions & endpoint API berlatensi rendah dengan konsumsi memori efisien. |
| **Database & ORM** | {s['database']} | Skema *type-safe* penuh dari query hingga TypeScript, migrasi terkontrol, dan koneksi serverless. |
| **Autentikasi** | {s['auth']} | Pengelolaan session aman dengan proteksi HttpOnly SameSite cookie dan proteksi CSRF bawaan. |
| **State Management** | {s['state']} | Menjaga sinkronisasi data server tanpa re-render berlebih serta persistensi state di URL query. |
| **Validasi Skema** | {s['validation']} | Validasi terpadu pada batas kepercayaan (*trust boundary*) baik di formulir UI maupun body API. |
| **Testing Harness** | {s['testing']} | Pengujian unit dan integrasi otomatis untuk mencegah regresi logika. |

---

## 4. Matriks State Komponen Antarmuka (UI State Matrix)

{ui_matrix_md}

---

## 5. Spesifikasi Rinci Modul & Fitur

{features_md}

---

## 6. Skema Database Lengkap (Data Dictionary & DDL)

### 6.1 Entity Relationship Diagram (Visual ERD)
```mermaid
{parse_ddl_to_mermaid(p['sqlDdl'])}
```

### 6.2 PostgreSQL 16 DDL Script
Berikut adalah DDL SQL PostgreSQL resmi yang mendefinisikan tabel, tipe enum, relasi foreign key dengan aturan integritas referensial, serta indeks pencarian performa:

```sql
{p['sqlDdl']}
```

---

## 7. Kontrak Spesifikasi API (RESTful Endpoints)

{api_md}

---

## 8. Persyaratan Non-Fungsional (Non-Functional Requirements)

{nfr_md}

---

## 9. Aturan Emas Pengerjaan untuk AI Coding Agent
1. **Frontend Mock First:** Wajib menyelesaikan Fase 1 & 2 dengan mock data statis terlebih dahulu sebelum membuat tabel database atau server functions, agar user dapat langsung memvalidasi UI di browser.
2. **Single-Task Execution:** Kerjakan satu task per putaran prompt. Dilarang merombak modul di luar cakupan task yang sedang aktif.
3. **Ponytail Principle:** Tulis kode sesedikit mungkin yang bekerja dengan benar ("boring over clever"). Manfaatkan fitur native web API dan pustaka standar.
"""

def generate_tasks_markdown(plan: Dict[str, Any]) -> str:
    p = plan
    output = f"# Task Backlog: {p['name']}\n\n"
    output += f"> **Total Task:** {len(p['tasks'])} Micro-Tasks Terstruktur  \n"
    output += "> **Metodologi:** 4 Fase Pengerjaan (Fase 1 Mockup UI -> Fase 2 State Interaktif -> Fase 3 Database & API -> Fase 4 Integrasi & Polish)\n\n"
    output += "Panduan AI Coding Agent: Kerjakan task secara berurutan. Berhenti di checkpoint akhir setiap fase untuk konfirmasi pengguna.\n\n---\n\n"

    current_phase = 0
    phase_headers = {
        1: "## FASE 1 — FONDASI, LAYOUT, & MOCKUP UI STATIS (Layer: Frontend)\n*Tujuan: Membangun seluruh tampilan visual dengan data tiruan agar dapat langsung diklik-klik di browser.*\n",
        2: "## FASE 2 — STATE MANAGEMENT & INTERAKSI KLIEN (Layer: Frontend)\n*Tujuan: Menyambungkan form input, validasi Zod, dan manipulasi data di memori/localStorage.*\n",
        3: "## FASE 3 — SKEMA DATABASE, AUTENTIKASI, & API BACKEND (Layer: Database & Backend)\n*Tujuan: Membuat skema tabel DDL, migrasi DB, autentikasi session, dan endpoint RESTful API.*\n",
        4: "## FASE 4 — INTEGRASI END-TO-END, HARDENING, & POLISH (Layer: Integration & Polish)\n*Tujuan: Mengganti mock data dengan API nyata, audit keamanan, pengujian SEO, dan verifikasi production build.*\n"
    }

    for t in p["tasks"]:
        if t["phase"] != current_phase:
            current_phase = t["phase"]
            output += "\n" + phase_headers.get(current_phase, f"## FASE {current_phase}\n")

        checklist_str = "\n".join([f"  - [ ] {c}" for c in t["checklist"]])
        files_str = ", ".join([f"`{f}`" for f in t["files"]])
        
        output += f"""### [{t['ref']}] {t['title']}
- **Layer:** `{t['layer']}` | **Fase:** `{t['phase']}`
- **Objektif:** {t['desc']}
- **File Terkait:** {files_str}
- **Checklist Eksekusi:**
{checklist_str}
- **Verifikasi Penerimaan (Acceptance Test):** {t['acceptance']}

```markdown
# Salin Prompt Ini ke AI Agent:
Kamu akan mengerjakan task {t['ref']} ({t['title']}) untuk proyek {p['name']}.
Layer: {t['layer']} | Fase: {t['phase']}

Objektif:
{t['desc']}

Checklist Pengerjaan:
{chr(10).join(['- ' + c for c in t['checklist']])}

Kriteria Pengujian (Lakukan Verifikasi Ini Sebelum Melapor Selesai):
{t['acceptance']}

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan memodifikasi file di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi pengujian berhasil, lapor hasilnya ke user secara ringkas.
```

---
"""
    return output

def generate_agents_markdown(plan: Dict[str, Any]) -> str:
    p = plan
    return f"""# AGENTS.md — Instruksi Kerja AI Coding Agent

Proyek: **{p['name']}**  
Kategori: **{p['categoryTitle']}**  
Tech Stack: **{p['stack']['name']}**  

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
"""

def main():
    # Dispatch subcommands: next, complete, status, mock
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd in ["next", "step"]:
            from task_runner import run_next_task
            target_path = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("-") else None
            ok, msg = run_next_task(target_path)
            print(msg)
            sys.exit(0 if ok else 1)

        elif cmd in ["complete", "done", "check"]:
            if len(sys.argv) < 3 or sys.argv[2].startswith("-"):
                print("❌ Masukkan nomor/ref task yang ingin ditandai selesai.")
                print("Contoh: python cli.py complete T-01")
                sys.exit(1)
            from task_runner import run_complete_task
            task_ref = sys.argv[2]
            target_path = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("-") else None
            ok, msg = run_complete_task(task_ref, target_path)
            print(msg)
            sys.exit(0 if ok else 1)

        elif cmd in ["status", "tasks", "list"]:
            from task_runner import run_task_status
            target_path = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("-") else None
            ok, msg = run_task_status(target_path)
            print(msg)
            sys.exit(0 if ok else 1)

        elif cmd in ["export-rules", "rules"]:
            from mock_server import find_plan_file
            target_dir = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("-") else "."
            plan_arg = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("-") else None
            actual_plan = find_plan_file(plan_arg)
            if not actual_plan:
                print("❌ Berkas plan.json tidak ditemukan untuk ekspor rules.")
                print("Jalankan di folder proyek atau tentukan path: python cli.py export-rules ./output ./path/to/plan.json")
                sys.exit(1)
            with open(actual_plan, "r", encoding="utf-8") as f:
                plan_data = json.load(f)

            os.makedirs(target_dir, exist_ok=True)
            cursor_dir = os.path.join(target_dir, ".cursor", "rules")
            os.makedirs(cursor_dir, exist_ok=True)

            with open(os.path.join(target_dir, "AGENTS.md"), "w", encoding="utf-8") as f:
                f.write(generate_agents_markdown(plan_data))
            with open(os.path.join(target_dir, "CLAUDE.md"), "w", encoding="utf-8") as f:
                f.write(generate_claude_markdown(plan_data))
            with open(os.path.join(target_dir, ".cursorrules"), "w", encoding="utf-8") as f:
                f.write(generate_cursor_rules(plan_data))
            with open(os.path.join(cursor_dir, "architecture.mdc"), "w", encoding="utf-8") as f:
                f.write(generate_cursor_mdc(plan_data))

            print(f"✅ Berhasil mengekspor 4 konfigurasi Multi-Agent ke: {os.path.abspath(target_dir)}")
            print("  🤖 AGENTS.md                  (Hermes Agent & Autonomous AI)")
            print("  ⚡ CLAUDE.md                  (Anthropic Claude Code CLI)")
            print("  🎯 .cursorrules               (Cursor IDE Composer)")
            print("  📜 .cursor/rules/architecture.mdc (Cursor Rules 2.0 MDC)")
            sys.exit(0)

        elif cmd in ["refine", "analyze"]:
            from mock_server import find_plan_file
            target_arg = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("-") else None
            actual_plan = find_plan_file(target_arg)
            if actual_plan:
                with open(actual_plan, "r", encoding="utf-8") as f:
                    p_data = json.load(f)
                name = p_data.get("name", "Aplikasi")
                idea = p_data.get("idea", "")
            else:
                name = target_arg or "Aplikasi Baru"
                idea = " ".join([a for a in sys.argv[3:] if not a.startswith("-")]) or name

            print("=" * 74)
            print("⚡ BikinPlan AI Refine Engine (Edge Cases & Architecture Analysis)")
            print("=" * 74)
            analysis = refine_idea(name, idea)
            print(f"🎯 Target: {name}\n")
            print(analysis)
            print("=" * 74)
            sys.exit(0)

        elif cmd in ["mock", "serve-mock"]:
            from mock_server import start_mock_server
            plan_path = None
            port = 3333
            no_browser = "--no-browser" in sys.argv
            for idx, arg in enumerate(sys.argv[2:], start=2):
                if arg == "--port" and idx + 1 < len(sys.argv):
                    port = int(sys.argv[idx + 1])
                elif not arg.startswith("-") and not plan_path:
                    plan_path = arg
            start_mock_server(plan_path=plan_path, port=port, open_browser=not no_browser)
            sys.exit(0)

    parser = argparse.ArgumentParser(description="BikinPlan CLI - Enterprise PRD & Tasks Generator untuk AI Coding Agent")
    parser.add_argument("name", nargs="?", default="Aplikasi Web Keren", help="Nama proyek atau aplikasi")
    parser.add_argument("--idea", default="", help="Deskripsi lengkap ide aplikasi")
    parser.add_argument("--preset", choices=["toko", "portfolio", "campus", "saas", "dashboard"], default=None, help="Pilih blueprint preset siap pakai")
    parser.add_argument("--refine", action="store_true", help="Otomatis pertajam ide dengan analisis edge cases")
    parser.add_argument("--stack", default="tanstack", choices=["tanstack", "nextjs", "vite-spa"], help="Pilihan tech stack")
    parser.add_argument("--target", default="Mahasiswa & Pengguna Umum", help="Target audiens")
    parser.add_argument("--output", default=".", help="Folder output penyimpanan dokumen")

    args = parser.parse_args()

    # Terapkan preset jika dipilih
    if args.preset:
        preset_info = PRESETS[args.preset]
        if args.name == "Aplikasi Web Keren":
            args.name = preset_info["name"]
        if not args.idea:
            args.idea = preset_info["idea"]
        if args.target == "Mahasiswa & Pengguna Umum":
            args.target = preset_info["target"]

    idea = args.idea or f"Platform digital inovatif untuk menjawab kebutuhan efisiensi pengguna {args.name}."

    if args.refine:
        print("⚡ Menganalisis & mempertajam ide dengan edge cases...")
        edge_cases = refine_idea(args.name, idea)
        idea += f"\n\nAturan Edge Cases & Proteksi Arsitektur:\n{edge_cases}"

    print(f"\n🚀 Menyusun PRD Enriched Enterprise untuk: {args.name}...")
    plan = synthesize_plan(args.name, idea, args.stack, args.target)

    prd_content = generate_prd_markdown(plan)
    tasks_content = generate_tasks_markdown(plan)
    agents_content = generate_agents_markdown(plan)
    claude_content = generate_claude_markdown(plan)
    cursor_rules_content = generate_cursor_rules(plan)
    cursor_mdc_content = generate_cursor_mdc(plan)

    out_dir = os.path.abspath(args.output)
    os.makedirs(out_dir, exist_ok=True)
    cursor_rules_dir = os.path.join(out_dir, ".cursor", "rules")
    os.makedirs(cursor_rules_dir, exist_ok=True)

    prd_path = os.path.join(out_dir, "PRD.md")
    tasks_path = os.path.join(out_dir, "TASKS.md")
    agents_path = os.path.join(out_dir, "AGENTS.md")
    claude_path = os.path.join(out_dir, "CLAUDE.md")
    cursor_rules_path = os.path.join(out_dir, ".cursorrules")
    cursor_mdc_path = os.path.join(cursor_rules_dir, "architecture.mdc")
    plan_json_path = os.path.join(out_dir, "plan.json")

    with open(prd_path, "w", encoding="utf-8") as f:
        f.write(prd_content)
    with open(tasks_path, "w", encoding="utf-8") as f:
        f.write(tasks_content)
    with open(agents_path, "w", encoding="utf-8") as f:
        f.write(agents_content)
    with open(claude_path, "w", encoding="utf-8") as f:
        f.write(claude_content)
    with open(cursor_rules_path, "w", encoding="utf-8") as f:
        f.write(cursor_rules_content)
    with open(cursor_mdc_path, "w", encoding="utf-8") as f:
        f.write(cursor_mdc_content)
    with open(plan_json_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)

    import zipfile
    zip_path = os.path.join(out_dir, f"{plan['slug']}-specs.zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(prd_path, arcname="PRD.md")
        zf.write(agents_path, arcname="AGENTS.md")
        zf.write(tasks_path, arcname="TASKS.md")
        zf.write(claude_path, arcname="CLAUDE.md")
        zf.write(cursor_rules_path, arcname=".cursorrules")
        zf.write(cursor_mdc_path, arcname=".cursor/rules/architecture.mdc")
        zf.write(plan_json_path, arcname="plan.json")

    print(f"✅ Selesai! Dokumen komprehensif berhasil dibuat di {out_dir}:")
    print(f"  📄 {prd_path} ({len(prd_content.splitlines())} baris)")
    print(f"  📋 {tasks_path} ({len(tasks_content.splitlines())} baris - {len(plan['tasks'])} Tasks)")
    print(f"  🤖 {agents_path} (Pedoman Umum & Hermes)")
    print(f"  ⚡ {claude_path} (Claude Code CLI)")
    print(f"  🎯 {cursor_rules_path} & {cursor_mdc_path} (Cursor Rules 2.0)")
    print(f"  📦 {plan_json_path}")
    print(f"  🗜️  {zip_path} (Multi-Agent Bundle ZIP: PRD, TASKS, CLAUDE, Cursor, AGENTS)\n")

    print("=" * 74)
    print("🧭 PANDUAN PENGGUNAAN KE AI AGENT (Claude Code / Hermes / Cursor):")
    print("=" * 74)
    print("1. KAPAN MENGIRIM PRD & AGENTS.MD?")
    print("   -> Kirim DI PERCAKAPAN PERTAMA KALI saat baru membuka AI Agent di folder ini.")
    print("   -> Prompt Handshake Pembuka:")
    print('      \"Baca PRD.md dan AGENTS.md di folder ini. Pahami arsitekturnya.')
    print('       DILARANG menulis kode atau database sebelum saya beri task pertama.')
    print('       Apakah kamu sudah paham arsitekturnya?\"')
    print()
    print("2. CARA MENJALANKAN TASK (SATU PER SATU DENGAN TASK RUNNER):")
    print("   -> Ambil task pertama dan otomatis salin prompt ke clipboard:")
    print("      👉 python cli.py next")
    print("   -> Tempelkan (Ctrl+V) ke terminal AI Agent kamu.")
    print("   -> Setelah agent menyelesaikan task ini, tandai selesai:")
    print("      👉 python cli.py complete T-01")
    print()
    print("3. JALANKAN INSTANT API MOCK SERVER (FRONTEND MOCK FIRST):")
    print("   -> Jalankan mock API server lokal tanpa setup database:")
    print("      👉 python cli.py mock")
    print("   -> Buka http://localhost:3333/__mock untuk dashboard interaktif.")
    print("=" * 74 + "\n")

if __name__ == "__main__":
    main()