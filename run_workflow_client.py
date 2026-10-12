#!/usr/bin/env python3
"""
SCM Disruption Orchestrator - Enterprise Test Runner Client
Executes an end-to-end supply chain disruption triage against the published Dify workflow API.

Usage:
    export DIFY_API_URL="http://your-dify-ip:3000/v1/workflows/run"
    export DIFY_APP_KEY="app-your-api-key"
    python run_workflow_client.py
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error

# Set stdout encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Configuration (read from environment or provide fallback placeholder)
DIFY_API_URL = os.environ.get("DIFY_API_URL", "http://localhost:3000/v1/workflows/run")
DIFY_APP_KEY = os.environ.get("DIFY_APP_KEY", "app-your-secret-api-key-here")

def run_disruption_triage(report: str, source: str = "webhook", region: str = "Western Europe", urgency: str = "CRITICAL"):
    print("=" * 70)
    print("🚨 SCM DISRUPTION ORCHESTRATOR - ENTERPRISE TRIAGE RUNNER")
    print("=" * 70)
    print(f"Target API Endpoint : {DIFY_API_URL}")
    print(f"Disruption Region   : {region}")
    print(f"Urgency Level       : {urgency}")
    print(f"Incident Report     : {report[:80]}...")
    print("-" * 70)

    if DIFY_APP_KEY == "app-your-secret-api-key-here":
        print("⚠️ Warning: DIFY_APP_KEY is set to placeholder.")
        print("   Set it via: export DIFY_APP_KEY='app-...' or pass DIFY_APP_KEY environment variable.\n")

    payload = {
        "inputs": {
            "disruption_report": report,
            "disruption_source": source,
            "affected_region": region,
            "urgency_hint": urgency
        },
        "response_mode": "blocking",
        "user": "enterprise-triage-client"
    }

    req_data = json.dumps(payload).encode('utf-8')
    headers = {
        "Authorization": f"Bearer {DIFY_APP_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "AutonomousAgent/1.0"
    }

    t0 = time.time()
    req = urllib.request.Request(DIFY_API_URL, data=req_data, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            elapsed = time.time() - t0
            result = json.loads(resp.read().decode('utf-8'))
            outputs = result.get("data", {}).get("outputs", {})

            print(f"✅ EXECUTION SUCCEEDED in {elapsed:.2f}s!")
            print(f"Workflow Run ID     : {result.get('workflow_run_id')}")
            print(f"Incident ID         : {outputs.get('incident_id')}")
            print(f"Adversarial Score   : {outputs.get('quality_score')} (Red-Team Verified)")
            print(f"Orchestration Status: {outputs.get('status')}")
            print("-" * 70)
            print("\n📋 C-SUITE EXECUTIVE BRIEF:")
            print(outputs.get("executive_brief", "N/A")[:500] + "...\n")
            print("-" * 70)
            print("\n🛠️ 48-HOUR OPERATIONS PLAYBOOK:")
            print(outputs.get("operations_playbook", "N/A")[:500] + "...\n")
            print("-" * 70)
            print("\n💵 FINANCIAL IMPACT & VAR MEMO:")
            print(outputs.get("financial_memo", "N/A")[:500] + "...\n")
            print("=" * 70)
            return outputs

    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8', errors='replace')
        print(f"❌ HTTP Error {e.code}: {err}")
        return None
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

if __name__ == "__main__":
    # Check if a sample dataset is available in local directory
    sample_file = os.path.join(os.path.dirname(__file__), "synthetic_disruptions_sample.json")
    if os.path.exists(sample_file):
        with open(sample_file, "r", encoding="utf-8") as f:
            records = json.load(f)
            sample = records[0]
            report = sample.get("disruption_report")
            source = sample.get("disruption_source", "webhook")
            region = sample.get("affected_region", "Western Europe")
            urgency = sample.get("urgency_hint", "CRITICAL")
    else:
        report = (
            "Port of Rotterdam dockworkers strike initiated midnight today. "
            "Terminal berths 4-8 completely halted, stranding container cargo. "
            "ASML tier-2 precision optics and semiconductor sub-assemblies facing severe backlog. "
            "Estimated duration 14-21 days if negotiations stall."
        )
        source = "webhook"
        region = "Rotterdam / Western Europe (NL)"
        urgency = "CRITICAL"

    run_disruption_triage(report, source, region, urgency)
