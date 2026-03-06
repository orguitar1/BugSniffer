BugSniffer Development Workflow (Quick Guide)

This document summarizes how the BugSniffer project is developed and maintained.

The goal is to keep development organized, resumable, and architecturally consistent.

1. Development Tools

BugSniffer development uses the following tools:

Editor
• Visual Studio Code

Architecture and planning
• ChatGPT

Implementation and repository inspection
• Claude Code

Version control
• GitHub

Backend framework
• FastAPI

2. AI Tool Roles
ChatGPT — Architecture & Planning

Used for:

• system architecture
• feature planning
• API design
• scanner architecture
• AI agent pipeline design
• reviewing implementation strategies
• updating the BugSniffer Continuity Summary

ChatGPT acts as the architecture advisor and development planner.

Claude Code — Implementation & Repository Analysis

Used for:

• writing code
• debugging
• refactoring
• inspecting the repository
• explaining code behavior
• summarizing project structure

Claude Code may also assist with:

• architecture review
• tradeoff analysis
• verifying that designs fit the current codebase

Claude Code acts primarily as the implementation engineer.

3. Design-First Development

Complex features should be designed before implementation.

Design documents are stored in:

docs/plans/

Examples:

docs/plans/api_design.md
docs/plans/finding_schema.md
docs/plans/scanner_architecture.md

These plans describe:

• module responsibilities
• file structure
• data models
• request flow
• edge cases

Implementation begins only after the design is reviewed.

Major architectural decisions are recorded in:

docs/adr/
4. Typical Development Session

A normal development session follows this flow:

Discuss or design a feature with ChatGPT.

If the feature is complex, create a design plan in:

docs/plans/

Implement the feature using Claude Code.

Test the implementation locally.

Commit and push changes to GitHub.

Example Git workflow:

git add backend/main.py
git add backend/services/scan_service.py
git commit -m "implement scan service"
git push

Avoid using:

git add .

to reduce the risk of accidentally committing sensitive files such as .env.

5. Testing

Features must be tested locally before committing.

Testing may include:

Manual API testing using tools like:

• curl
• Postman

Automated smoke tests using:

pytest

Tests are stored in:

tests/
6. End-of-Session Procedure

At the end of every development session:

Ask ChatGPT:

Update the BugSniffer continuity summary.

ChatGPT generates the updated summary.

Replace the previous summary inside Project Sources.

This summary serves as the authoritative record of the project state.

7. Conversation Reset

To prevent extremely long conversations:

• Start a new ChatGPT conversation every Monday

However, if a conversation becomes very large or degraded earlier in the week, a reset can happen sooner.

Because the project automatically loads:

• Project Instructions
• Latest Continuity Summary

development can resume immediately.

8. Project Memory Structure

BugSniffer maintains three independent sources of project memory.

Source Code

Stored in the GitHub repository.

Architecture and Design History

Stored in:

docs/
docs/plans/
docs/adr/
Project State Memory

Stored in the BugSniffer Continuity Summary in Project Sources.

This guarantees the project can always be resumed.

9. Engineering Principles

BugSniffer development prioritizes:

• modular architecture
• separation of concerns
• design-first development
• documented architecture decisions
• incremental feature building