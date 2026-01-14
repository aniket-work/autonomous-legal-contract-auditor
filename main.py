import sys
import time
import json
from simple_chalk import chalk, green, red, yellow, cyan, bold
from risk_engine import RiskPlaybook
from auditor import ContractAuditor

def simulate_typing(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    print(chalk.bold.blue("\n=== Autonomous Legal Contract Auditor (v1.2.0) ===\n"))
    time.sleep(0.5)

    # 1. Ingest
    simulate_typing(f"{chalk.green('➜')} Ingesting document: 'Vendor_Service_Agreement_v4.pdf'...", 0.05)
    
    # Mock extracted clauses
    clauses = [
        {
            "id": "CL-01",
            "type": "Indemnification",
            "text": "The Vendor shall indemnify, verify, and hold harmless the Client against all claims..."
        },
        {
            "id": "CL-05",
            "type": "Governing Law",
            "text": "This Agreement shall be governed by the laws of the State of California."
        },
        {
            "id": "CL-09",
            "type": "Payment Terms",
            "text": "Invoices are payable immediately upon receipt."
        }
    ]
    
    time.sleep(1)
    print(f"    [PDFParser] Extracted {len(clauses)} clauses for review.")
    time.sleep(0.5)

    risk_engine = RiskPlaybook()
    auditor = ContractAuditor()
    
    findings = []

    # 2. Audit Loop
    for clause in clauses:
        print(f"\n{chalk.yellow('➜')} Auditing Clause {clause['id']} ({clause['type']})...")
        time.sleep(0.3)
        print(f"    [Text] \"{clause['text'][:50]}...\"")
        
        policy = risk_engine.search_playbook(clause["text"])
        if policy:
             result = auditor.audit_clause(clause["text"], policy)
             result["clause_id"] = clause["id"]
             findings.append(result)
             
             color = green if result["risk_level"] == "LOW" else red
             print(f"    [Result] Risk: {color(result['risk_level'])} | Score: {result['risk_score']}")

    # 3. Final Report
    print("\n" + "="*65)
    print(f"{bold('LEGAL RISK ASSESSMENT REPORT')}")
    print("="*65)
    
    total_risk = sum(f["risk_score"] for f in findings) / len(findings)
    risk_color = green
    if total_risk > 30: risk_color = yellow
    if total_risk > 70: risk_color = red
    
    print(f"Document       : Vendor_Service_Agreement_v4.pdf")
    print(f"Risk Score     : {risk_color(str(int(total_risk)) + '/100')}")
    print(f"Clauses Flagged: {len([f for f in findings if f['risk_score'] > 0])}")
    print("-" * 65)
    print("CRITICAL FINDINGS:")
    
    for f in findings:
        if f["risk_score"] > 50:
            print(f"  [x] Clause {f['clause_id']}: {f['finding']} ({red('Risk: ' + str(f['risk_score']))})")
            
    print("="*65 + "\n")

if __name__ == "__main__":
    main()
