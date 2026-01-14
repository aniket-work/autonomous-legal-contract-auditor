import time
import random

class ContractAuditor:
    def __init__(self):
        pass

    def audit_clause(self, clause_text: str, policy: dict):
        """
        Simulates LLM reasoning to audit a clause against a policy.
        """
        print(f"    [Auditor] Comparing clause to {policy['id']}...")
        time.sleep(0.5)
        
        score = 0
        risk_level = "LOW"
        finding = ""
        
        clause_lower = clause_text.lower()
        
        # Simulated Logic
        if policy["id"] == "RISK-001": # Indemnification
            if "mutual" in clause_lower or ("vendor" in clause_lower and "company" in clause_lower):
                score = 10
                risk_level = "LOW"
                finding = "Clause is mutual. Compliant."
            else:
                score = 85
                risk_level = "HIGH"
                finding = "One-sided indemnification detected. Violation of Policy."
                
        elif policy["id"] == "RISK-002": # Jurisdiction
            if "new york" in clause_lower or "delaware" in clause_lower:
                score = 0
                risk_level = "LOW"
                finding = "Jurisdiction is compliant."
            else:
                score = 60
                risk_level = "MEDIUM"
                finding = "Non-standard jurisdiction. Requires legal review."

        elif policy["id"] == "RISK-003": # Payment
            if "net 45" in clause_lower or "net 60" in clause_lower:
                score = 0
                risk_level = "LOW"
                finding = "Payment terms compliant."
            elif "upon receipt" in clause_lower:
                score = 95
                risk_level = "CRITICAL"
                finding = "Immediate payment terms rejected."
            else:
                score = 25
                risk_level = "LOW"
                finding = "Standard Net 30 acceptable."

        # Add some AI "variability"
        time.sleep(0.2)
        
        return {
            "risk_score": score,
            "risk_level": risk_level,
            "finding": finding
        }
