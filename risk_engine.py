import time

class RiskPlaybook:
    def __init__(self):
        self.playbook = {
            "INDEMNIFICATION": {
                "id": "RISK-001",
                "policy": "Mutual Indemnification Required",
                "description": "Any indemnification clause must be mutual. One-sided indemnification in favor of the vendor is heavily penalized."
            },
            "JURISDICTION": {
                "id": "RISK-002",
                "policy": "Governing Law: New York or Delaware",
                "description": "We only accept NY or DE law. Foreign jurisdictions or California law require General Counsel approval."
            },
            "PAYMENT_TERMS": {
                 "id": "RISK-003",
                 "policy": "Net 45 or Net 60",
                 "description": "Standard payment terms are Net 45. Net 30 is acceptable for software under $50k. Immediate payment upon receipt is rejected."
            }
        }

    def search_playbook(self, clause_text: str):
        """
        Simulates Semantic Search to find relevant risk policy.
        """
        print(f"    [RiskEngine] Converting clause to vector embeddings...")
        time.sleep(0.3)
        
        clause_lower = clause_text.lower()
        
        if "indemnif" in clause_lower or "hold harmless" in clause_lower:
             print(f"    [RiskEngine] Match found: RISK-001 (Confidence: 0.94)")
             return self.playbook["INDEMNIFICATION"]
        elif "governing law" in clause_lower or "jurisdiction" in clause_lower:
             print(f"    [RiskEngine] Match found: RISK-002 (Confidence: 0.91)")
             return self.playbook["JURISDICTION"]
        elif "payment" in clause_lower or "invoice" in clause_lower:
             print(f"    [RiskEngine] Match found: RISK-003 (Confidence: 0.88)")
             return self.playbook["PAYMENT_TERMS"]
        
        return None
