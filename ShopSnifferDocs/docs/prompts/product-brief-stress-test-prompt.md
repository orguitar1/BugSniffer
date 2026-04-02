# Product Brief / Design Document Stress Test Prompt

Use this prompt to pressure-test any major design document before implementation begins. Paste into a fresh agent or an existing agent that can take an adversarial perspective.

---

You are stress-testing a design document for the ShopSniffer project. Your job is to find gaps, contradictions, unstated assumptions, and failure modes that the authors may have missed.

Read the document carefully, then evaluate against these categories:

**1. Missing Failure Modes** — What happens when things go wrong? Are error states, timeouts, partial failures, and degraded operation addressed? For each major feature or workflow described, ask: "What if this fails halfway through?"

**2. Contradictions** — Does the document contradict itself? Are there places where two sections make incompatible promises or assumptions?

**3. Unstated Assumptions** — What is the document assuming without saying so? Platform capabilities, user behavior, API availability, data volumes, cost constraints?

**4. Missing Edge Cases** — What happens at the boundaries? Zero items, maximum items, concurrent operations, rapid repeated actions, unexpected input types?

**5. Scalability Concerns** — Will this design work at 10x the expected load? 100x? Where are the bottlenecks? What breaks first?

**6. Security and Privacy Gaps** — Are there data handling, access control, or compliance issues not addressed? For ShopSniffer specifically: Shopify GDPR requirements, tenant isolation, API credential storage, webhook verification.

**7. User Experience Gaps** — Are there user-facing scenarios that the document doesn't address? Onboarding, error messaging, upgrade/downgrade transitions, account deletion?

**8. Implementation Feasibility** — Are there features described that may be significantly harder to build than the document implies? External dependencies that may not work as assumed?

**Output format:**

For each finding:
- **Category** — which of the 8 categories above
- **Issue** — specific gap or concern
- **Severity** — blocking (must fix before implementation), important (should fix), minor (note for later)
- **Suggestion** — how to address it

End with an overall assessment: is this document ready to guide implementation? What are the top 3 things to fix first?
