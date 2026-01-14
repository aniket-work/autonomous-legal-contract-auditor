import base64
import requests
import os

def generate_mermaid_diagram(name, code):
    graphbytes = code.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    url = "https://mermaid.ink/img/" + base64_string
    
    print(f"Generating {name}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"images/{name}.png", 'wb') as f:
                f.write(response.content)
            print(f" -> Saved images/{name}.png")
        else:
            print(f" -> Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f" -> Failed: {e}")

def main():
    if not os.path.exists("images"):
        os.makedirs("images")

    diagrams = {
        "title_diagram": """
        graph TB
            title[<br>Autonomous Legal Contract Auditor<br>]
            style title fill:#1d3557,stroke:#457b9d,stroke-width:2px,color:#f1faee,font-size:24px

            subgraph Audit_Engine [Audit Engine]
                direction TB
                PDF[Contract PDF] -->|OCR/Parse| Text[Clause Extractor]
                Playbook[(Risk Playbook DB)] -->|Retrieval| Auditor[LLM Auditor]
                Text -->|Clause Context| Auditor
                Auditor -->|Risk Score| Report[Audit Report]
            end
            
            style Audit_Engine fill:#f8f9fa,stroke:#dee2e6,color:#212529
            style PDF fill:#e63946,stroke:#1d3557,color:#fff
            style Playbook fill:#1d3557,stroke:#457b9d,color:#fff
            style Auditor fill:#a8dadc,stroke:#457b9d,color:#1d3557
            style Report fill:#457b9d,stroke:#1d3557,color:#fff
        """,
        
        "architecture_diagram": """
        graph LR
            User((Legal Team)) -->|Upload NDA| API[Ingestion API]
            API -->|Queue| Worker[Audit Agent]
            
            subgraph Reasoning_Core
                Worker -->|Fetch Policies| VectorDB[(Risk Playbook)]
                Worker -->|Analyze Clause| LLM[LLM Service]
                VectorDB <-->|Embeddings| LLM
            end
            
            Worker -->|Flag Risks| DB[(Audit DB)]
            DB -->|Dashboard| User
            
            style API fill:#ffb703,stroke:#023047
            style Worker fill:#fb8500,stroke:#023047
            style LLM fill:#219ebc,stroke:#023047
        """,
        
        "sequence_diagram": """
        sequenceDiagram
            participant Lawyer
            participant Agent
            participant Playbook
            participant LLM
            
            Lawyer->>Agent: Upload Contract (NDA)
            Agent->>Agent: Parse PDF -> Extract Clauses
            
            loop For Each Clause
                Agent->>Playbook: Search Relevant Risk Policy
                Playbook-->>Agent: Returns Policy (e.g., Jurisdiction)
                Agent->>LLM: Audit Clause vs Policy
                LLM-->>Agent: Risk Score + Finding
            end
            
            Agent->>Lawyer: Final Risk Report
        """,
        
        "flow_diagram": """
        stateDiagram-v2
            [*] --> IngestContract
            IngestContract --> ParseClauses
            
            state Audit_Loop {
                ParseClauses --> GetPolicy
                GetPolicy --> CheckCompliance
                CheckCompliance --> AssignRisk
            }
            
            AssignRisk --> ReportGeneration
            ReportGeneration --> [*]
        """
    }
    
    for name, code in diagrams.items():
        generate_mermaid_diagram(name, code)

if __name__ == "__main__":
    main()
