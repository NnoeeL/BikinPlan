#!/usr/bin/env python3
"""
BikinPlan Task Runner - Live CLI Execution Engine for Layered Tasks
Prinsip Ponytail: Minimal code, stdlib only, cross-platform clipboard.
"""

import os
import sys
import re
import subprocess
from typing import Dict, Any, List, Optional, Tuple

def copy_to_clipboard(text: str) -> bool:
    """Menyalin teks ke clipboard sistem secara cross-platform menggunakan utilitas bawaan OS."""
    try:
        if sys.platform == "win32":
            # Pada Windows modern, clip.exe menerima utf-8
            subprocess.run(["clip.exe"], input=text.encode("utf-8"), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        elif sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        else:
            for cmd in [["xclip", "-selection", "clipboard"], ["wl-copy"], ["xsel", "--clipboard", "--input"]]:
                try:
                    subprocess.run(cmd, input=text.encode("utf-8"), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return True
                except FileNotFoundError:
                    continue
    except Exception:
        pass
    return False

def find_tasks_file(target_path: Optional[str] = None) -> Optional[str]:
    """Mencari berkas TASKS.md di path yang diberikan atau direktori kerja aktif."""
    candidates = []
    if target_path:
        if os.path.isfile(target_path):
            return os.path.abspath(target_path)
        if os.path.isdir(target_path):
            candidates.append(os.path.join(target_path, "TASKS.md"))

    # Cek direktori aktif saat ini
    cwd = os.getcwd()
    candidates.append(os.path.join(cwd, "TASKS.md"))

    # Cek subdirektori sample jika ada di cwd
    for sample_dir in ["sample-enterprise", "sample-toko", "sample-portfolio", "sample-saas", "sample-rental", "sample-test"]:
        candidates.append(os.path.join(cwd, sample_dir, "TASKS.md"))

    # Cek di direktori skrip ini berada
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.join(script_dir, "TASKS.md"))
    for sample_dir in ["sample-enterprise", "sample-toko", "sample-portfolio", "sample-saas", "sample-rental", "sample-test"]:
        candidates.append(os.path.join(script_dir, sample_dir, "TASKS.md"))

    for c in candidates:
        if os.path.isfile(c):
            return os.path.abspath(c)
    return None

def parse_tasks(content: str) -> List[Dict[str, Any]]:
    """Mem-parse struktur berkas TASKS.md menjadi daftar task terstruktur."""
    tasks = []
    # Pola untuk mencocokkan header task: ### [T-01] atau ### [x] [T-01] atau ### [T-01] Judul
    # Kita split berdasarkan baris pemisah task: \n--- atau header task
    lines = content.splitlines()
    
    current_task = None
    in_prompt_block = False
    prompt_lines = []
    current_phase = 1
    
    phase_regex = re.compile(r'##\s*FASE\s*(\d+)', re.IGNORECASE)
    task_header_regex = re.compile(r'^###\s*(\[x\]\s*)?\[?(T-\d+)\]?[\s:-]*(.*)$', re.IGNORECASE)
    layer_phase_regex = re.compile(r'-\s*\*\*Layer:\*\*\s*`([^`]+)`\s*\|\s*\*\*Fase:\*\*\s*`?(\d+)`?', re.IGNORECASE)
    obj_regex = re.compile(r'-\s*\*\*Objektif:\*\*\s*(.*)$', re.IGNORECASE)
    accept_regex = re.compile(r'-\s*\*\*Verifikasi Penerimaan.*?\*\*:\s*(.*)$', re.IGNORECASE)
    files_regex = re.compile(r'-\s*\*\*File Terkait:\*\*\s*(.*)$', re.IGNORECASE)
    checklist_regex = re.compile(r'^\s*-\s*\[([ xX])\]\s*(.*)$')

    for line in lines:
        phase_match = phase_regex.search(line)
        if phase_match:
            try:
                current_phase = int(phase_match.group(1))
            except ValueError:
                pass

        task_match = task_header_regex.match(line)
        if task_match:
            if current_task:
                if prompt_lines:
                    current_task["prompt"] = "\n".join(prompt_lines).strip()
                tasks.append(current_task)
                prompt_lines = []
                in_prompt_block = False

            is_header_checked = bool(task_match.group(1))
            ref = task_match.group(2).upper()
            title = task_match.group(3).strip()

            current_task = {
                "ref": ref,
                "title": title,
                "is_header_checked": is_header_checked,
                "phase": current_phase,
                "layer": "frontend",
                "desc": "",
                "files": "",
                "acceptance": "",
                "checklist": [], # list of {"done": bool, "text": str}
                "prompt": ""
            }
            continue

        if not current_task:
            continue

        # Check prompt block markdown
        if line.strip().startswith("```markdown"):
            in_prompt_block = True
            continue
        elif in_prompt_block and line.strip() == "```":
            in_prompt_block = False
            continue
        elif in_prompt_block:
            prompt_lines.append(line)
            continue

        layer_match = layer_phase_regex.search(line)
        if layer_match:
            current_task["layer"] = layer_match.group(1).strip()
            try:
                current_task["phase"] = int(layer_match.group(2).strip())
            except ValueError:
                pass
            continue

        obj_match = obj_regex.search(line)
        if obj_match:
            current_task["desc"] = obj_match.group(1).strip()
            continue

        files_match = files_regex.search(line)
        if files_match:
            current_task["files"] = files_match.group(1).strip()
            continue

        accept_match = accept_regex.search(line)
        if accept_match:
            current_task["acceptance"] = accept_match.group(1).strip()
            continue

        chk_match = checklist_regex.match(line)
        if chk_match:
            is_done = chk_match.group(1).lower() == 'x'
            current_task["checklist"].append({
                "done": is_done,
                "text": chk_match.group(2).strip()
            })
            continue

    if current_task:
        if prompt_lines:
            current_task["prompt"] = "\n".join(prompt_lines).strip()
        tasks.append(current_task)

    # Hitung status penyelesaian tiap task
    for t in tasks:
        all_chk_done = len(t["checklist"]) > 0 and all(c["done"] for c in t["checklist"])
        t["is_completed"] = t["is_header_checked"] or all_chk_done

    return tasks

def build_progress_bar(completed: int, total: int, width: int = 20) -> str:
    """Membuat visual progress bar terminal bergaya modern."""
    if total <= 0:
        return "[--------------------] 0.0%"
    pct = (completed / total) * 100
    filled = int(round(width * completed / total))
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {completed}/{total} ({pct:.1f}%)"

def run_next_task(tasks_path: Optional[str] = None) -> Tuple[bool, str]:
    """Mengambil task aktif berikutnya, menyalin prompt ke clipboard, dan mencetak panduan."""
    actual_path = find_tasks_file(tasks_path)
    if not actual_path:
        return False, "❌ Berkas TASKS.md tidak ditemukan. Jalankan perintah di folder proyek atau tentukan path: python cli.py next ./path/to/TASKS.md"

    with open(actual_path, "r", encoding="utf-8") as f:
        content = f.read()

    tasks = parse_tasks(content)
    if not tasks:
        return False, f"❌ Tidak ada task yang terdeteksi di {actual_path}."

    total_count = len(tasks)
    completed_count = sum(1 for t in tasks if t["is_completed"])

    # Cari task pertama yang belum selesai
    active_task = next((t for t in tasks if not t["is_completed"]), None)

    if not active_task:
        msg = []
        msg.append("=" * 72)
        msg.append("🎉 LUAR BIASA! SEMUA TASK TELAH SELESAI!")
        msg.append("=" * 72)
        msg.append(f"📊 Status: {completed_count}/{total_count} Task rampung 100%.")
        msg.append(f"📁 Berkas: {actual_path}")
        msg.append("\nSeluruh 4 Fase telah tuntas:")
        msg.append("  [x] Fase 1 — Frontend Mockup")
        msg.append("  [x] Fase 2 — State Management")
        msg.append("  [x] Fase 3 — Database & Backend API")
        msg.append("  [x] Fase 4 — Integrasi, Hardening & Production Polish")
        msg.append("\n🚀 Proyek siap dipublikasikan atau diaudit dengan: python cli.py status")
        msg.append("=" * 72)
        return True, "\n".join(msg)

    # Generate prompt jika blok prompt tidak tertangkap sempurna
    prompt_text = active_task.get("prompt")
    if not prompt_text:
        chk_lines = "\n".join([f"- {c['text']}" for c in active_task["checklist"]])
        prompt_text = f"""Kamu akan mengerjakan task {active_task['ref']} ({active_task['title']}).
Layer: {active_task['layer']} | Fase: {active_task['phase']}

Objektif:
{active_task['desc']}

Checklist Pengerjaan:
{chk_lines}

Kriteria Pengujian:
{active_task['acceptance']}

Aturan Eksekusi:
1. Kerjakan HANYA checklist di atas. Jangan merombak modul di luar cakupan task ini.
2. Tulis kode sesedikit mungkin yang bekerja dengan benar (Ponytail principle).
3. Setelah verifikasi berhasil, laporkan hasil pengujian ke user secara ringkas."""

    # Salin ke clipboard
    copied = copy_to_clipboard(prompt_text)

    # Susun output CLI
    phase_names = {
        1: "Fase 1 (Frontend Mockup UI)",
        2: "Fase 2 (Client State & Validation)",
        3: "Fase 3 (Database DDL & Backend API)",
        4: "Fase 4 (Integrasi & Production Polish)"
    }
    phase_label = phase_names.get(active_task["phase"], f"Fase {active_task['phase']}")

    lines = []
    lines.append("=" * 74)
    lines.append("⚡ BikinPlan Task Runner — Next Active Task")
    lines.append("=" * 74)
    lines.append(f"📊 Progres Saat Ini : {build_progress_bar(completed_count, total_count)}")
    lines.append(f"🎯 Task Aktif       : [{active_task['ref']}] {active_task['title']}")
    lines.append(f"🏷️  Layer / Fase     : `{active_task['layer']}` | {phase_label}")
    if active_task.get("files"):
        lines.append(f"📂 File Terkait     : {active_task['files']}")
    if active_task.get("checklist"):
        lines.append(f"📋 Total Checklist  : {len(active_task['checklist'])} butir pekerjaan")

    lines.append("")
    if copied:
        lines.append("✨ [PROMPT DISALIN KE CLIPBOARD] ✨")
        lines.append("👉 Buka terminal Claude Code / Hermes / Cursor, lalu tekan Ctrl+V / Cmd+V.")
    else:
        lines.append("👉 Salin prompt di bawah ini ke terminal AI Agent kamu:")

    lines.append("-" * 74)
    lines.append(prompt_text)
    lines.append("-" * 74)

    lines.append("\n💡 Langkah Berikutnya:")
    lines.append(f"   Setelah AI Agent selesai mengerjakan dan acceptance test lolos, tandai selesai:")
    lines.append(f"   👉 python cli.py complete {active_task['ref']}")
    lines.append(f"   (atau ketik: bikinplan complete {active_task['ref']})")
    lines.append("=" * 74)

    return True, "\n".join(lines)

def run_complete_task(task_ref: str, tasks_path: Optional[str] = None) -> Tuple[bool, str]:
    """Menandai suatu task sebagai selesai di berkas TASKS.md dan menampilkan task berikutnya."""
    actual_path = find_tasks_file(tasks_path)
    if not actual_path:
        return False, "❌ Berkas TASKS.md tidak ditemukan."

    with open(actual_path, "r", encoding="utf-8") as f:
        content = f.read()

    ref_clean = task_ref.strip().upper()
    if not ref_clean.startswith("T-"):
        # Jika user mengetik angka misal '1' atau '01', ubah jadi 'T-01'
        m = re.match(r'^\d+$', ref_clean)
        if m:
            ref_clean = f"T-{int(ref_clean):02d}"
        else:
            ref_clean = f"T-{ref_clean}"

    # Cari blok task yang sesuai dan tandai selesai
    # Pola: cari `### [ref_clean]` atau `### [x] [ref_clean]`
    pattern = re.compile(rf'(###\s*(?:\[[ xX]\]\s*)?\[?{re.escape(ref_clean)}\]?\s*[^\n]*)', re.IGNORECASE)
    match = pattern.search(content)
    if not match:
        return False, f"❌ Task dengan kode [{ref_clean}] tidak ditemukan di {actual_path}."

    # Lakukan update pada checklist di bawah task ini sampai batas task berikutnya (### atau ---)
    task_start = match.start()
    next_task_match = re.search(r'\n###\s+', content[match.end():])
    task_end = match.end() + next_task_match.start() if next_task_match else len(content)

    task_block = content[task_start:task_end]

    # 1. Update header task menjadi ### [x] [T-XX]
    original_header = match.group(1)
    new_header = re.sub(r'^###\s*(?:\[[ xX]\]\s*)?', '### [x] ', original_header)
    updated_block = task_block.replace(original_header, new_header, 1)

    # 2. Centang semua checklist `- [ ]` menjadi `- [x]` di dalam blok ini
    updated_block = re.sub(r'(\s*-\s*)\[\s*\]', r'\1[x]', updated_block)

    # Tulis kembali ke file
    new_content = content[:task_start] + updated_block + content[task_end:]
    with open(actual_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    # Parse ulang untuk menghitung progres terbaru dan menemukan task berikutnya
    tasks = parse_tasks(new_content)
    total_count = len(tasks)
    completed_count = sum(1 for t in tasks if t["is_completed"])
    next_task = next((t for t in tasks if not t["is_completed"]), None)

    lines = []
    lines.append("=" * 74)
    lines.append(f"✅ TASK [{ref_clean}] BERHASIL DITANDAI SELESAI!")
    lines.append("=" * 74)
    lines.append(f"📊 Progres Terbaru : {build_progress_bar(completed_count, total_count)}")
    lines.append(f"📁 Berkas Diperbarui: {actual_path}")

    if next_task:
        lines.append(f"\n🎯 Task Berikutnya  : [{next_task['ref']}] {next_task['title']}")
        lines.append(f"🏷️  Layer / Fase     : `{next_task['layer']}` | Fase {next_task['phase']}")
        lines.append(f"\n👉 Ambil prompt task berikutnya & salin ke clipboard dengan:")
        lines.append(f"   python cli.py next")
    else:
        lines.append("\n🎉 SELAMAT! Semua task dalam backlog telah tuntas dikerjakan!")

    lines.append("=" * 74)
    return True, "\n".join(lines)

def run_task_status(tasks_path: Optional[str] = None) -> Tuple[bool, str]:
    """Menampilkan ringkasan status backlog secara visual per fase."""
    actual_path = find_tasks_file(tasks_path)
    if not actual_path:
        return False, "❌ Berkas TASKS.md tidak ditemukan."

    with open(actual_path, "r", encoding="utf-8") as f:
        content = f.read()

    tasks = parse_tasks(content)
    if not tasks:
        return False, f"❌ Tidak ada task yang terdeteksi di {actual_path}."

    total_count = len(tasks)
    completed_count = sum(1 for t in tasks if t["is_completed"])

    phase_titles = {
        1: "FASE 1 — FONDASI, LAYOUT & MOCKUP UI STATIS",
        2: "FASE 2 — CLIENT STATE & INTERAKSI FORM",
        3: "FASE 3 — SKEMA DATABASE DDL & BACKEND API",
        4: "FASE 4 — INTEGRASI END-TO-END & POLISH"
    }

    lines = []
    lines.append("=" * 74)
    lines.append("📋 BikinPlan Task Backlog — Status Progres")
    lines.append("=" * 74)
    lines.append(f"📁 Berkas  : {actual_path}")
    lines.append(f"📊 Ringkasan: {build_progress_bar(completed_count, total_count)}")
    lines.append("-" * 74)

    for phase_num in [1, 2, 3, 4]:
        phase_tasks = [t for t in tasks if t["phase"] == phase_num]
        if not phase_tasks:
            continue

        p_done = sum(1 for t in phase_tasks if t["is_completed"])
        p_total = len(phase_tasks)
        p_status = "✅ SELESAI" if p_done == p_total else f"{p_done}/{p_total} Done"

        lines.append(f"\n📌 {phase_titles.get(phase_num, f'FASE {phase_num}')}  [{p_status}]")
        for t in phase_tasks:
            icon = "✅ [x]" if t["is_completed"] else "⏳ [ ]"
            lines.append(f"   {icon} {t['ref']}: {t['title']}")

    lines.append("\n" + "=" * 74)
    next_task = next((t for t in tasks if not t["is_completed"]), None)
    if next_task:
        lines.append(f"💡 Task aktif selanjutnya: [{next_task['ref']}] {next_task['title']}")
        lines.append("   Jalankan: python cli.py next")
    else:
        lines.append("🎉 Seluruh task selesai! Siap untuk rilis.")
    lines.append("=" * 74)

    return True, "\n".join(lines)
