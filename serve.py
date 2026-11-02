#!/usr/bin/env python3
"""
BikinPlan Web & Instant Mock Server
Melayani UI BikinPlan dan Mock API Server terintegrasi (Frontend Mock First).
"""

import os
import sys
import argparse
from mock_server import start_mock_server, find_plan_file

PORT = 3333
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def main():
    parser = argparse.ArgumentParser(description="BikinPlan Web & Instant Mock API Server")
    parser.add_argument("--port", type=int, default=PORT, help="Port server (default: 3333)")
    parser.add_argument("--plan", default=None, help="Path ke berkas plan.json (opsional)")
    parser.add_argument("--no-browser", action="store_true", help="Jangan otomatis membuka browser")
    parser.add_argument("--mock-only", action="store_true", help="Jalankan khusus mock API server")

    args = parser.parse_args()

    # Cari file plan.json
    plan_path = find_plan_file(args.plan)
    if not plan_path:
        # Jika belum ada plan di folder aktif, arahkan ke sample-enterprise/plan.json jika ada
        sample_plan = os.path.join(DIRECTORY, "sample-enterprise", "plan.json")
        if os.path.isfile(sample_plan):
            plan_path = sample_plan

    start_mock_server(
        plan_path=plan_path,
        port=args.port,
        static_dir=DIRECTORY,
        open_browser=not args.no_browser
    )

if __name__ == "__main__":
    main()
