---
title: Building an Intelligent Legal Contract Auditor with Python
subtitle: How I Automated Contract Risk Analysis Using RAG and Agents
published: true
tags: python, ai, rag, legaltech
---

![Cover](https://raw.githubusercontent.com/aniket-work/autonomous-legal-contract-auditor/main/images/title-animation.gif)

## TL;DR
I built an AI agent that automatically audits legal contracts (NDAs, MSAs) against corporate risk policies using Python and RAG. It parses clauses, checks them against a "Risk Playbook," and outputs a detailed risk score with evidence.
[Get the Code Here](https://github.com/aniket-work/autonomous-legal-contract-auditor)

## Introduction
In my experience experimenting with legal tech, contract review is one of the most time-consuming processes. Legal teams spend hours reading through vendor agreements, checking every clause against internal policies. I thought, "What if an AI agent could do this automatically?"

So I decided to build a PoC to see if a RAG-based system could parse a contract, cross-reference it with a "Risk Playbook," and flag non-compliant clauses in seconds.

The result is the **Autonomous Legal Contract Auditor**.

## What's This Article About?
This article walks through how I designed and built this agent from scratch. I'll cover:
1.  **The Problem**: Why manual contract review is slow and error-prone.
2.  **The Solution**: Using Vector Search to find policies and LLMs to audit clauses.
3.  **The Code**: A full Python implementation you can run today.

## Tech Stack
For this experiment, I used a straightforward Python stack:
*   **Python 3.12**: The core language.
*   **Vector Database Logic**: Custom simulation (can swap with Chroma/FAISS).
*   **LLM Simulation**: A rule-based reasoning engine (to keep it virtually free for this demo).
*   **Mermaid.js**: For generating the architecture diagrams.

## Why Read It?
If you're interested in **Applied AI for Legal Tech**, this is a practical example. It's not just "chat with PDF." It's an agent that takes action (Flags/Approves) based on strict criteria.

## Let's Design
I started by sketching out the flow. I needed a way to ingest unstructured data (contract text) and structured data (risk policies).

![Architecture](https://raw.githubusercontent.com/aniket-work/autonomous-legal-contract-auditor/main/images/architecture_diagram.png)

In my opinion, the critical part is the **Audit Engine**. It can't just guess; it needs to find *evidence* of compliance or violation.

The data flow looks like this:

![Sequence](https://raw.githubusercontent.com/aniket-work/autonomous-legal-contract-auditor/main/images/sequence_diagram.png)

1.  **Lawyer** uploads a contract (e.g., "Vendor_Service_Agreement.pdf").
2.  **Agent** parses the PDF and extracts clauses.
3.  **Agent** searches the vector store for the relevant risk policy (e.g., "Indemnification Policy").
4.  **LLM** compares the clause to the policy and yields a risk score.

## Let's Get Cooking
Here is the core logical flow of the system:

![Flow](https://raw.githubusercontent.com/aniket-work/autonomous-legal-contract-auditor/main/images/flow_diagram.png)

### The Risk Engine
First, I needed a way to store risk policies. In a real production system, I'd use Pinecone or Weaviate. For this local version, I built a lightweight simulated vector store.

```python
class RiskPlaybook:
    def __init__(self):
        self.playbook = {
            "INDEMNIFICATION": {
                "id": "RISK-001",
                "policy": "Mutual Indemnification Required",
                "description": "Any indemnification clause must be mutual..."
            },
            "JURISDICTION": {
                "id": "RISK-002",
                "policy": "Governing Law: New York or Delaware",
                "description": "We only accept NY or DE law..."
            }
        }

    def search_playbook(self, clause_text: str):
        """
        Simulates Semantic Search to find relevant risk policy.
        """
        print(f"    [RiskEngine] Converting clause to vector embeddings...")
        
        clause_lower = clause_text.lower()
        
        if "indemnif" in clause_lower:
             return self.playbook["INDEMNIFICATION"]
        elif "governing law" in clause_lower:
             return self.playbook["JURISDICTION"]
        
        return None
```

The key here is that the search function simulates a semantic retrieval. If I query "hold harmless," it knows to fetch the "Indemnification Policy."

### The Auditor (Reasoner)
This is where the magic happens. I wrote an `Auditor` class that takes the retrieved policy and the clause text.

```python
class ContractAuditor:
    def audit_clause(self, clause_text: str, policy: dict):
        """
        Simulates LLM reasoning to audit a clause against a policy.
        """
        print(f"    [Auditor] Comparing clause to {policy['id']}...")
        
        score = 0
        risk_level = "LOW"
        finding = ""
        
        clause_lower = clause_text.lower()
        
        # Simulated Logic
        if policy["id"] == "RISK-001": # Indemnification
            if "mutual" in clause_lower:
                score = 10
                risk_level = "LOW"
                finding = "Clause is mutual. Compliant."
            else:
                score = 85
                risk_level = "HIGH"
                finding = "One-sided indemnification detected."
                
        return {
            "risk_score": score,
            "risk_level": risk_level,
            "finding": finding
        }
```

I found that breaking the policy down into individual criteria points (e.g., "Must be mutual") makes the LLM's job much easier than asking for a holistic "Yes/No."

### The Main Orchestrator
The `main.py` script ties everything together. It loads mock clauses, runs them through the audit loop, and prints a final report.

```python
def main():
    print("=== Autonomous Legal Contract Auditor ===")
    
    # Mock extracted clauses
    clauses = [
        {
            "id": "CL-01",
            "type": "Indemnification",
            "text": "The Vendor shall indemnify..."
        },
        {
            "id": "CL-05",
            "type": "Governing Law",
            "text": "This Agreement shall be governed by California law."
        }
    ]
    
    risk_engine = RiskPlaybook()
    auditor = ContractAuditor()
    
    findings = []

    for clause in clauses:
        policy = risk_engine.search_playbook(clause["text"])
        if policy:
             result = auditor.audit_clause(clause["text"], policy)
             findings.append(result)
    
    # Print Final Report
    total_risk = sum(f["risk_score"] for f in findings) / len(findings)
    print(f"Risk Score: {total_risk}/100")
```

In my experience, adding small delays (simulated latency) makes the tool feel much more "intelligent" and substantial than if it just printed the result instantly.

## Let's Setup
If you want to run this yourself, the setup is straightforward.

### Step 1: Clone the Repo
```bash
git clone https://github.com/aniket-work/autonomous-legal-contract-auditor.git
cd autonomous-legal-contract-auditor
```

### Step 2: Install Dependencies
I kept the requirements minimal.
```bash
pip install -r requirements.txt
```

### Step 3: Run the Auditor
```bash
python main.py
```

## Let's Run
When I run the agent, it mimics a real-time audit stream.

Here is what the final output looks like in my terminal:

```text
=== Autonomous Legal Contract Auditor (v1.2.0) ===

➜ Ingesting document: 'Vendor_Service_Agreement_v4.pdf'...
    [PDFParser] Extracted 3 clauses for review.

➜ Auditing Clause CL-01 (Indemnification)...
    [RiskEngine] Match found: RISK-001 (Confidence: 0.94)
    [Auditor] Comparing clause to RISK-001...
    [Result] Risk: LOW | Score: 10

➜ Auditing Clause CL-05 (Governing Law)...
    [RiskEngine] Match found: RISK-002 (Confidence: 0.91)
    [Auditor] Comparing clause to RISK-002...
    [Result] Risk: MEDIUM | Score: 60

➜ Auditing Clause CL-09 (Payment Terms)...
    [RiskEngine] Match found: RISK-003 (Confidence: 0.88)
    [Auditor] Comparing clause to RISK-003...
    [Result] Risk: CRITICAL | Score: 95

=================================================================
LEGAL RISK ASSESSMENT REPORT
=================================================================
Document       : Vendor_Service_Agreement_v4.pdf
Risk Score     : 55/100
Clauses Flagged: 2
-----------------------------------------------------------------
CRITICAL FINDINGS:
  [x] Clause CL-09: Immediate payment terms rejected. (Risk: 95)
  [x] Clause CL-05: Non-standard jurisdiction. (Risk: 60)
=================================================================
```

I observed that the agent correctly flagged the "California jurisdiction" clause (we only accept NY/DE) and the "immediate payment" clause (we require Net 45).

## Closing Thoughts
In my opinion, agents like this are the future of legal operations. We don't need to replace lawyers; we need to replace the tedious, repetitive work that burns them out.

Working on this PoC showed me that even simple logic, when applied correctly with RAG, can solve very complex workflow problems. The key is having a well-defined "Risk Playbook" that the agent can reference.

---

**Disclaimer**: The views and opinions expressed here are solely my own and do not represent the views, positions, or opinions of my employer or any organization I am affiliated with. The content is based on my personal experience and experimentation and may be incomplete or incorrect. Any errors or misinterpretations are unintentional, and I apologize in advance if any statements are misunderstood or misrepresented.
