# BugSniffer Architecture

BugSniffer is an AI-assisted cybersecurity analysis platform designed to detect vulnerabilities in source code.

The system uses a modular layered architecture that separates responsibilities into independent components.

This design allows scanners, AI agents, and services to be expanded without modifying the core system.

---

# High-Level System Architecture

The system consists of five primary layers:

Frontend
API Layer
Services Layer
Scanner Layer
AI Agent Layer

The interaction flow follows this general pattern:

User → Frontend → API → Services → Scanners → AI Agents → Response

---

# Frontend Layer

Responsibilities:

• Code submission interface
• Scan status display
• Vulnerability results visualization

Technology:

React  
Next.js

The frontend communicates with the backend through REST APIs.

---

# API Layer

Location:

backend/api/

Responsibilities:

• HTTP request handling
• Request validation
• Routing to services
• Response formatting

Technology:

FastAPI

Example endpoints:

POST /scan
GET /scan/{id}
GET /health

The API layer must remain lightweight and should not contain business logic.

---

# Services Layer

Location:

backend/services/

Responsibilities:

• Orchestrating scans
• Managing scanner execution
• Aggregating vulnerability results
• Passing results to AI agents

The services layer contains the core application logic.

Example services:

scan_service.py
analysis_service.py
vulnerability_service.py

---

# Scanner Layer

Location:

scanners/

Responsibilities:

• Execute vulnerability detection tools
• Parse scanner results
• Return normalized vulnerability data

Each scanner should follow a common interface so new scanners can be easily added.

Example future scanners:

smart_contract_scanner
dependency_scanner
static_analysis_scanner

Scanners should not contain AI logic.

---

# AI Agent Layer

Location:

agents/

Responsibilities:

• Interpret scanner results
• Generate vulnerability explanations
• Provide remediation suggestions
• Assign severity classification

Agents operate on structured vulnerability data produced by scanners.

Agents use prompt templates stored in:

prompts/

---

# Data Flow

Typical vulnerability analysis flow:

1. User submits code
2. API receives request
3. Scan service orchestrates scanner execution
4. Scanners detect vulnerabilities
5. Results are normalized into a standard format
6. AI agents analyze the vulnerabilities
7. System returns structured vulnerability report

---

# Modularity Goals

The architecture is designed so that:

• new scanners can be added easily
• new AI agents can be added
• scanners can run independently
• AI analysis can be expanded

This ensures BugSniffer can evolve into a broader security analysis platform.

---

# Future Architecture Considerations

Potential future improvements:

• distributed scanner workers
• scan job queue
• persistent vulnerability database
• user authentication
• multi-project scanning