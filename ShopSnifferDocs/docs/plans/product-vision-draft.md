# ShopSniffer — Product Brief

Status: Reviewed and agreed — guides all subsequent design and architecture decisions.
Date: 2026-04-01

---

## 1. What Is ShopSniffer

A Shopify app that monitors your store's health and gives you an AI assistant that can explain problems, diagnose issues, fix your code, and tell you exactly what's going on — in plain language, instantly, instead of waiting on a developer.

The AI assistant is the product. The scanning and analysis is the engine underneath. The conversation is what merchants pay for.

---

## 2. Who Is It For

### Primary: Solo Shopify Store Owners

Non-technical merchants running their own stores with no developer on staff. They can't interpret PageSpeed reports, they can't edit Liquid templates, and they can't afford to pay a developer $150/hr to tell them things they don't understand. They need someone to tell them what's wrong and fix it for them.

### Secondary: Agencies and Freelance Developers

Professionals managing multiple Shopify stores for clients. They can do this work manually, but a tool that automates diagnostics, surfaces issues across client stores, and handles routine fixes saves them significant time. Think of it like Hyperspeed — used by solo owners who need it and by agencies who appreciate the efficiency.

---

## 3. The Merchant Experience

### 3.1 Installation and First Scan

The merchant installs the app from the Shopify App Store. An initial scan runs automatically. Within minutes, they have a complete picture of their store's health.

### 3.2 The Dashboard

The merchant opens the app and immediately sees their store's health status: a clear overview, the latest findings organized by category, what changed since the last scan, and any alerts. This is the at-a-glance view — no interpretation needed.

### 3.3 The AI Assistant

An AI chat is prominently placed in the interface — not buried in a corner, not hidden behind a tab. The merchant can browse findings on their own, or talk to the AI:

- *"Why is my store slow?"*
- *"Is this new app I installed safe?"*
- *"What should I fix first?"*
- *"Just fix it for me."*

The AI explains issues in plain language, can trigger scans on command, compares results to historical data, and — critically — can make code changes to fix problems.

### 3.4 AI Code Editing (Preview Theme System)

This is the core differentiator. When the AI identifies a fixable issue, it doesn't just tell the merchant what to do — it does it. The workflow:

- **The AI creates a duplicate theme** (never touches the live store directly).
- The AI makes the code changes in the duplicate theme.
- The merchant previews the result and sees exactly what changed, described in plain language.
- The merchant decides whether to publish. They are always in control.
- The previous theme remains available as an instant rollback.

**Post-publish health check:** After a merchant publishes an AI-generated theme, the system automatically runs a health check scan to verify the live store is functioning correctly. This catches issues that weren't visible during the merchant's preview (e.g., checkout problems that only trigger on specific product pages). If a regression is detected, the merchant is alerted immediately — not at the next scheduled scan.

**Shopify constraint:** Apps can no longer edit live theme code directly. A new theme must be published for changes to take effect. This constraint actually works in our favor — it enforces the preview-first safety model naturally.

### 3.5 Notifications and Alerts

For continuous monitoring to be valuable, the merchant needs to be told when something changes — not required to remember to check the app. Proactive alerts via email or Shopify admin notification when scans detect regressions, new issues, or significant changes.

### 3.6 Transparent Limitations

The AI never pretends to know something it doesn't. When it's uncertain, it says so. When a fix is beyond its capability, it redirects to the human support team. Ambiguous scan data produces hedged language, not false certainty.

When the AI has partial information — for example, it can identify that the store slowed down but can't pinpoint which of three recently installed apps caused it — it shares what it knows, clearly labels what it doesn't know, and suggests concrete next steps the merchant can take to narrow it down. The goal is to be useful even when incomplete, without ever crossing the line into guessing.

---

## 4. What It Analyzes

### 4.1 Performance

- Page speed and Core Web Vitals (LCP, FID, CLS)
- Script bloat and render-blocking resources
- Image optimization opportunities
- Mobile performance (simulated via Lighthouse; real-world CrUX data where available, with clear labeling of which is which)

### 4.2 Third-Party App Impact

- Which installed apps are hurting performance
- Per-app script size and load time contribution
- Correlation between app installs and performance changes over time

**Note:** Attributing scripts to specific apps requires building and maintaining an app-to-script mapping database. This starts with the top 50–100 popular apps and grows over time. This is a long-term data asset.

### 4.3 Security and App Permissions

- What data each third-party app has access to (customers, orders, payments, etc.)
- Whether app permissions are broader than necessary for the app's stated function
- Flagging potentially risky permission patterns

**Feasibility note:** This requires Shopify Admin API access with specific scopes. Shopify reviews these scopes before approving the app listing. If access is restricted, this feature falls back to what's observable from the storefront (script tags, network requests). Needs early validation.

### 4.4 SEO Health

- Meta tags, structured data, sitemaps
- Broken links
- Mobile responsiveness issues
- Content quality signals

### 4.5 Change Detection Over Time

- Periodic automated scans to track trends
- Detecting regressions (store got slower, new issues appeared)
- Correlating changes with specific events (app installed, theme updated)

---

## 5. AI Assistant Architecture

### 5.1 Capabilities

The AI is not a report reader. It is a conversational assistant that can:

- Explain any finding in plain, merchant-friendly language
- Trigger scans on command and compare results to historical data
- Correlate problems with specific causes (recently installed app, theme change)
- Prioritize recommendations based on impact
- Make code changes in preview themes to fix identified issues
- Answer follow-up questions conversationally
- Redirect to human support when it reaches its limits

### 5.2 Accuracy Safeguards (Multi-Agent Verification)

The AI must be right. A dashboard with a wrong number is annoying. An AI that confidently tells a merchant to remove an app that's critical to their checkout is a trust-destroying moment.

Multiple AI agents run behind the scenes:

- **Analysis agent:** generates the explanation and recommendations from scan data.
- **Verification agent:** fact-checks claims against the raw scan data. Does the data actually support what the analysis agent said?
- **Confidence calibration:** adjusts language based on data certainty. Ambiguous data produces hedged responses, not confident assertions.

**Core rule:** The AI never states something with more confidence than the underlying data supports.

**Build order:** The multi-agent verification layer is an R&D problem that requires iteration. The basic AI chat ships first; the verification layer gets tuned over time until accuracy is trustworthy. We do not launch publicly until the AI layer is reliable.

### 5.3 Plain Language Changelogs

When the AI edits code, the merchant sees a human-readable description of what changed and why, not a code diff. Example:

*"I moved your announcement bar below the navigation menu and reduced the hero image size from 2400px to 1200px. This should improve your load time by about 0.8 seconds."*

Technical diffs are available for developers and the support team, but the default view is always plain language.

---

## 6. Interaction Records and Support System

### 6.1 The Merchant Record

Every merchant has a complete interaction history, modeled after a Helpscout-style ticketing system:

- Every AI conversation is logged
- Every scan triggered (automatic or on-demand) is recorded
- Every code change is documented with: what was changed, why, what the merchant was told, and whether it was published
- The AI generates a structured summary after each interaction

This is not just a chat transcript. It is a structured timeline of events, actions, and outcomes.

### 6.2 Human Support Team

When the AI isn't sure about something, when the merchant is uncomfortable, or when something goes wrong — there's a human. 24/7 support, with full access to the merchant's interaction history.

A support team member opening a merchant's record sees everything: what the AI discussed, what scans were run, what code changes were made, what the outcomes were. They never start from zero.

This serves three purposes:

- **Trust backstop:** merchants know a human is available if needed.
- **Quality assurance:** the support team monitors AI interactions and flags cases where the AI was wrong or unhelpful, feeding back into improvement.
- **Accountability:** if a code change causes issues, the record shows exactly what happened, when, and why.

### 6.3 Post-Session Summaries

After every interaction where changes were made, the AI sends the merchant a brief recap. Example:

*"Here's what we did today: ran a performance scan, identified three issues, fixed one (image optimization on your homepage), and flagged two for your review. Your performance score went from 62 to 78."*

---

## 7. Trust and Safety Principles

These are non-negotiable product principles, not optional features:

- **Preview everything:** The AI never publishes changes to the live store without the merchant's explicit approval. Every code change happens in a duplicate theme first.
- **One-click rollback:** The previous theme is preserved. If a published change causes problems, the merchant can revert directly from within the app — not by navigating Shopify admin. The rollback must be accessible and obvious, especially during a crisis when a non-technical merchant is panicking.
- **No false confidence:** The AI hedges when the data is ambiguous. It says "I'm not sure" when it isn't sure. It redirects to human support when it reaches its limits.
- **Transparent actions:** Every action the AI takes is logged, explained in plain language, and available for review by the merchant and the support team.
- **Merchant stays in control:** The AI suggests, explains, and waits for permission. It is powerful but deferential.

---

## 8. Monetization

### Tier Structure (Directional)

**Free Tier:** A scan every X days. Basic health status and findings, plus a limited number of AI interactions per scan (e.g., 1–2 questions) so the merchant experiences the actual product, not just a dashboard. The free tier must demonstrate the AI's value — a list of technical findings that a non-technical merchant can't interpret is the exact problem this product solves, not a compelling free experience.

**Mid Tier:** Regular automated scans, historical tracking, change detection, full findings detail, plus AI assistant access with a monthly interaction limit. The AI is too central to the value proposition to gate it entirely behind the top tier.

**Top Tier:** The most generous AI interaction limits (still capped), on-demand scans from chat, AI code editing in preview themes, multiple scan types (performance, security, SEO), priority recommendations, full interaction history.

**All tiers have usage caps — including the top tier.** No unlimited plans. Clear messaging when a merchant approaches their limit, with the option to upgrade or wait for the next billing cycle. If demand exceeds the top tier's limits, that's an enterprise conversation or a usage-based overage model.

Exact pricing, tier boundaries, and specific caps to be determined. Competitive reference: the mid-market for Shopify tools is $10–40/month, with enterprise solutions at $300+/month.

---

## 9. Platform and Launch Strategy

### 9.1 Platform

Shopify only. Deep Shopify integration, Shopify-specific context and recommendations, Shopify App Store listing. Architecture should not preclude future platform expansion, but Shopify focus comes first and is not compromised for generality.

### 9.2 Launch Approach

We are in no rush. The product launches only when the AI layer is reliable and trustworthy. Shipping a buggy AI assistant that gives confident wrong answers would be worse than not shipping at all. The scanning pipeline gets built and validated first, the AI layer gets tuned and verified, and only when the full loop works reliably do we go public.

**Minimum viable version:** If AI code editing proves harder to stabilize than expected, the product is still shippable without it. Scanning + AI chat + explanations + recommendations is a complete product on its own. Code editing can launch later as a premium feature once confidence is high. Within code editing itself, the initial scope should be limited to low-risk, well-understood fixes (image optimization, meta tag corrections, render-blocking script deferral) before expanding to more complex theme modifications.

---

## 10. Competitive Position

The Shopify app ecosystem has dozens of tools for speed optimization, SEO auditing, and performance monitoring. None of them combine all of the following:

- **AI conversation as the primary interface** — not a dashboard with a chatbot bolted on, but a genuine assistant that understands your store.
- **AI code editing with preview safety** — the assistant doesn't just diagnose, it fixes. No other tool does this.
- **Cross-category analysis** — performance, SEO, security, and app impact in one product, not four separate tools.
- **Historical trend tracking** — how is your store's health changing over time, correlated with specific events.
- **Human support backstop** — real people available when the AI reaches its limits, scaling to 24/7 as the team grows.

The closest competitor is GrowthPilot AI (continuous monitoring + AI explanations), but it doesn't edit code or offer the preview safety model. The security/permissions audit angle is the most underserved area in the market.

---

## 11. Known Risks and Open Questions

- **Shopify API scope approval:** The app permissions audit feature requires specific Admin API scopes that Shopify reviews. If access is restricted, the security feature is limited to storefront observation. Needs early validation.
- **App-to-script attribution:** Correlating performance impact with specific installed apps requires a mapping database that doesn't exist publicly. This is a data asset built over time, starting with the most popular apps.
- **AI accuracy at launch:** The multi-agent verification system requires R&D iteration. The basic AI chat can be built quickly; calibrating confidence and eliminating hallucinations takes longer. This is the primary reason for not rushing to launch.
- **LLM cost per interaction:** Multi-agent verification means 2–3 LLM calls per merchant question. At scale with a $20–50/month price point, per-query cost needs monitoring.
- **Headless browser in production:** Lighthouse requires Chrome. Running headless browsers at scale introduces memory management, timeout handling, and container complexity. This is solvable but operationally heavy.
- **Shopify App Store trust:** As a new app with zero reviews, early traction depends on a compelling free tier and fast word of mouth. The review count disadvantage against established tools is real.
- **Data retention and privacy:** Storing scan results and interaction records that include merchant store data must comply with Shopify's data handling requirements. Design constraint from day one.
- **Unit economics:** Multi-agent verification means 2–3 LLM calls per merchant question, plus token costs for code analysis and scan interpretation. LLM cost per merchant per month must be modeled before pricing tiers are finalized. If per-query cost exceeds what a $20–50/month price point can sustain, either the verification pipeline must be optimized (caching, smaller models for routine checks) or the pricing must adjust. This analysis happens during architecture design, not after launch.

---

## 12. Support Model

Human support is part of the product vision, scaling to 24/7 coverage over time. At launch, support availability is honest — do not promise 24/7 if it's one person. The product should state realistic response times and grow the support commitment as the team grows. Promising a feature that doesn't exist at launch is a trust-destroying experience for merchants.

The architecture must support the full support model from the start: interaction records, merchant history, escalation paths from AI to human. The infrastructure is there even when the team is small.

---

## 13. Non-Previewable Actions

Not every fix can be applied through theme editing. Actions like "uninstall this app," "change this Shopify admin setting," or "update your DNS configuration" can't be done through a preview theme. For these cases:

- The AI guides the merchant through self-service steps (with screenshots or step-by-step instructions).
- For anything complex or risky, the AI escalates to the human support team.

The AI must know its own boundaries — this should be explicit in the architecture so it never attempts an action it can't safely perform.

---

## 14. API Scopes Validation

Before designing the full security/permissions analysis feature, submit a minimal Shopify app early and request the scopes needed to read installed apps and their permissions. This runs in parallel with architecture design — it doesn't block anything, but the answer determines whether we build a full permissions audit or fall back to storefront-observable signals. Test early, don't assume access.

---

## 15. AI Reliability Threshold

**"We don't launch until the AI is reliable" is meaningless without a measurable bar.** Before building the AI layer, define concrete metrics that constitute "ready to launch":

- Accuracy rate on finding explanations (verified against raw scan data)
- False positive rate on recommendations
- Percentage of interactions requiring human escalation
- Merchant satisfaction score from beta testers

The specific numbers get defined during AI layer design, but the principle — define the bar before building toward it — is a product-level requirement, not a technical afterthought.

---

## 16. Data Lifecycle and Privacy

### 16.1 Merchant Uninstall

When a merchant uninstalls the app, the system must handle cleanup promptly and completely:

- Delete all stored scan results, interaction records, and AI conversation history within a defined retention window.
- Clean up any preview themes created by the AI that were never published.
- Provide a short reactivation window (e.g., 30 days) where data is retained in case the merchant reinstalls, after which all data is permanently deleted.

### 16.2 Shopify Mandatory GDPR Webhooks

Shopify requires all apps to implement three mandatory webhooks:

- `customers/redact` — delete customer data on request.
- `shop/redact` — delete all shop data after uninstall (after the retention window).
- `customers/data_request` — provide all stored customer data on request.

These are non-negotiable compliance requirements. The data model must be designed from day one to support efficient lookup and deletion by merchant and by customer.

### 16.3 Data Retention Policy

Define clear retention periods for each data type: scan results, AI conversations, code change records, and merchant account data. Retention periods should balance operational needs (support history, trend analysis) with privacy obligations. The specific periods are defined during architecture design, but the principle — every stored data type has a defined lifecycle — is a product-level requirement.

---

## 17. Internal Business Analytics

The product brief describes what merchants see. The team also needs visibility into what's happening internally:

- Scan volume and frequency patterns
- AI interaction counts per merchant and per tier
- Human support escalation rates
- API cost per merchant per month (especially LLM costs)
- Churn signals and conversion rates between tiers
- Feature usage (which scan types, how often AI edits code, etc.)

**This is not a merchant-facing feature — it's an internal operations layer.** It should be designed in from the start, not bolted on after launch. You can't optimize what you can't measure.

---

## 18. What Happens Next

This product brief defines what we're building and why. It is the foundation for all subsequent work:

- **Technical architecture design** — how to adapt the existing BugSniffer pipeline to this new product, what carries over, what's new.
- **Phase planning** — what gets built first, what's deferred, what a meaningful first version looks like.
- **Design documents** — detailed specs for each system component, stored in docs/plans/.

This document has been reviewed by all three development agents, a fresh independent agent, and the project owner. It incorporates all feedback received. Every technical decision should trace back to this brief.
