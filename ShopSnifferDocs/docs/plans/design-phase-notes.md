# ShopSniffer — Design Phase Notes

Status: Open — to be addressed during architecture and design document creation.
Date: 2026-04-01

These are technical questions, implementation considerations, and edge cases surfaced during the product brief stress-test. They don't belong in the product brief itself, but they must be answered during architecture and design work. Nothing here should be lost or forgotten.

---

## 1. Shopify API Mechanics

- **Theme duplication:** How does the Theme API handle duplication? What are the rate limits? How long does a theme duplication take for a large theme with many assets? What's the maximum number of themes a store can have (Shopify limits this to ~20)?
- **Theme cleanup:** If the merchant never publishes an AI-created preview theme, when does the system delete it? What happens if the store hits the theme limit?
- **Rate limits:** Shopify's API has per-app rate limits (typically 2 calls/second for REST, 50 points/second for GraphQL). How does this affect scan frequency, AI code editing, and concurrent operations?
- **API versioning:** Shopify deprecates API versions quarterly. The system must track which API version it targets and handle version migrations. Design for this from the start.
- **Webhook reliability:** Shopify webhooks are not guaranteed to deliver. The system needs idempotent webhook handlers and a reconciliation mechanism for missed events.

---

## 2. Scanning Architecture

- **Password-protected stores:** Lighthouse can't scan a password-protected storefront. How does the system detect this and communicate it to the merchant? Does it offer to scan with stored credentials, or does it require the merchant to temporarily remove the password?
- **Store size variance:** A store with 5 products and a store with 10,000+ products have very different scanning profiles. Page selection for scanning, crawl depth, and timeout handling need to account for this range.
- **Scan queuing and concurrency:** When multiple merchants request on-demand scans simultaneously, how are they queued? What's the maximum concurrent headless Chrome instances? How does this affect response time?
- **Lighthouse in production:** Memory management for headless Chrome at scale. Container resource limits, timeout handling, and graceful degradation when Chrome crashes mid-scan.
- **Scan result caching:** How long are scan results considered fresh? If a merchant asks the AI about their performance 5 minutes after a scan, does it use cached results or trigger a new scan?

---

## 3. AI Architecture

- **Token context windows:** Scan results, conversation history, and code context all compete for the LLM's context window. How is context managed when a merchant has a long conversation with multiple scan results and code changes? What gets summarized vs. kept verbatim?
- **Concurrent AI sessions:** Can a merchant have multiple AI conversations open? What happens if the AI is editing a preview theme in one conversation while the merchant starts a new conversation about a different issue?
- **Liquid template handling:** The AI needs to understand Shopify's Liquid templating language to make code edits. How deep does this understanding need to be? What's the boundary between "safe edits" and "risky edits"?
- **Code edit validation:** Before presenting a preview theme to the merchant, how does the system verify the AI's code changes don't contain syntax errors? Liquid syntax checking, JSON schema validation for settings, asset reference integrity.
- **LLM model selection:** Which model(s) for which tasks? The analysis agent might need a more capable (expensive) model than the verification agent. Caching and model routing strategy.
- **Fallback behavior:** If the LLM API is down or rate-limited, what does the merchant see? The dashboard and scan results should remain accessible even when the AI chat is unavailable.

---

## 4. Data Model Considerations

- **Interaction record schema:** The Helpscout-style records need a well-defined schema that captures: conversations, scans, code changes, publish decisions, rollbacks, escalations, and their relationships.
- **Historical data storage:** Scan results over time could accumulate significant data per merchant. Retention policies, archival strategy, and query performance for trend analysis.
- **Multi-store support:** For agency users managing multiple stores, the data model needs to support a one-to-many relationship between accounts and stores efficiently.
- **Tier upgrade/downgrade effects:** When a merchant changes tiers (up or down), what happens to their data and access? Does a downgraded merchant lose access to historical AI conversations? Are code-editing preview themes cleaned up if they drop below the tier that includes editing? Do scan frequency changes take effect immediately or at the next billing cycle? These transitions need explicit rules in the data model.

---

## 5. Security and Permissions

- **Scope validation results:** The outcome of the early API scope validation (Section 14 of the product brief) determines the entire security feature's design. Two paths need to be designed:
  - Full path: Admin API access to read installed apps and their permissions.
  - Fallback path: Storefront-only observation (script tags, network requests, observable behavior).
- **Merchant data isolation:** Scan results, AI conversations, and code changes for one merchant must never be accessible to another merchant. Tenant isolation strategy.
- **AI-generated code security:** The AI must not introduce security vulnerabilities in its code edits. How is this enforced? Static analysis on generated code? Restricted operations?
- **Shopify platform compliance webhooks:** The product brief (Section 16.2) defines the three mandatory GDPR webhooks (`customers/redact`, `shop/redact`, `customers/data_request`). The design must specify exactly what data each webhook deletes or returns, how deletion cascades through related records, and how the system confirms compliance. This is a hard requirement for Shopify App Store approval — not optional.

---

## 6. App-to-Script Mapping Database

- **Initial dataset:** Start with the top 50–100 most popular Shopify apps. How is the initial mapping built? Manual research, automated script fingerprinting, or both?
- **Maintenance:** Apps update their scripts. How frequently is the mapping refreshed? How are new apps added?
- **Unknown scripts:** When a script can't be attributed to any known app, what does the system report? How does it handle custom scripts the merchant wrote themselves?
- **Crowdsourcing potential:** Can anonymized data from ShopSniffer users help build the mapping database faster? Privacy implications of this approach.

---

## 7. Multilingual Support

- **AI responses:** When does multilingual AI support become necessary? Is English-only acceptable for launch? What about the growing non-English Shopify merchant base?
- **Scan result interpretation:** Some scan findings reference locale-specific content. How does the system handle stores with multiple languages?

---

## 8. Notification System

- **Channel selection:** Email, Shopify admin notifications, or both? What's the priority and fallback order?
- **Alert fatigue:** How to avoid overwhelming merchants with notifications. Batching strategy, severity thresholds, quiet hours.
- **Regression detection sensitivity:** What constitutes a "regression"? A 1-point drop in performance score? A 10-point drop? This threshold needs tuning and probably per-merchant configuration.

---

## 9. Support Team Tooling

- **Internal dashboard:** The support team needs a view into merchant records, AI conversations, and scan results. This is a separate interface from the merchant-facing app.
- **Escalation workflow:** When the AI escalates to human support, how is the handoff managed? Real-time? Ticket-based? How does the support person continue the conversation the AI started?
- **AI monitoring:** The support team reviews AI interactions for quality. What does this review interface look like? How are flagged interactions fed back into AI improvement?

---

## 10. Infrastructure and Deployment

- **Hosting considerations:** FastAPI backend, headless Chrome for scanning, LLM API calls, real-time chat — these have different scaling profiles. Containerization strategy.
- **Cost monitoring:** LLM costs, compute costs for scanning, storage costs for historical data — all need per-merchant visibility for the internal business analytics layer.
- **Staging environment:** How do we test against real Shopify stores during development? Test stores, partner accounts, mock data.

---

This document will be referenced and expanded during the architecture design phase. Each section should eventually map to a design document in `docs/plans/` with specific answers and implementation details.
