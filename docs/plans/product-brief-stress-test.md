# ShopSniffer Product Brief — Stress Test Report

**Date:** 2026-04-01
**Author:** Claude Cowork (Orchestrator)
**Document under test:** `docs/plans/product-vision-draft.md`
**Purpose:** Break this document before it becomes architecture. Find what's weak, vague, contradictory, or missing.

---

## 1. Try to Build From This

**Feature chosen: AI Code Editing via Preview Theme System (Section 3.4)**

This is the stated core differentiator. If I'm the engineer starting tomorrow, here's where I stop and ask questions:

### Blocking Ambiguities

**How does the AI "create a duplicate theme"?**
The document says the AI creates a duplicate theme and makes code changes in it. Shopify's Theme API allows duplicating themes, but the document doesn't specify: Does the AI duplicate the *entire* live theme every time it proposes a fix? What if the merchant already has the maximum number of themes allowed by their Shopify plan (free plans allow up to 20 themes)? What happens when a merchant accumulates 15 preview themes from prior AI fixes — who cleans them up? The document is silent on theme lifecycle management.

**What constitutes a "fixable issue"?**
Section 3.4 says "when the AI identifies a fixable issue, it doesn't just tell the merchant what to do — it does it." There's no taxonomy of what's fixable vs. what's not. Performance issues identified in Section 4.1 include render-blocking resources, image optimization, and script bloat. Can the AI fix all of these through theme code? Image optimization requires re-encoding and re-uploading assets — that's not a Liquid template edit. Removing render-blocking resources may require modifying how third-party apps inject scripts, which is outside theme code. The boundary between "the AI fixes it" and "the AI guides you" (Section 13) is undefined.

**What does "makes the code changes" actually mean technically?**
The AI needs to: read the current theme's Liquid templates, understand Shopify's template structure (layouts, sections, snippets, assets), identify which file(s) to modify, generate correct Liquid/HTML/CSS/JS changes, and write them via the Shopify Asset API. None of this technical flow is described. The engineer needs to know: Does the AI get the full theme as context? What's the token limit implication of sending an entire theme to an LLM? How does it handle themes with 200+ files?

**What does "the merchant previews the result" mean?**
Does this mean a Shopify theme preview URL? A side-by-side comparison in our UI? A screenshot? The document says the merchant "sees exactly what changed, described in plain language" (Section 5.3), but that's the changelog — not the visual preview. A merchant who can't read code needs to *see* their store looking correct, not just read a description of what changed.

**Rollback mechanics are underspecified.**
Section 7 says "the previous theme is preserved" and "the merchant can revert by republishing the previous theme." But if the merchant publishes the AI's theme, then makes manual changes to it, and *then* wants to rollback — they'd lose their manual changes. The document treats rollback as simple, but Shopify's theme publishing model makes it a one-way door once you start editing the new live theme. This isn't addressed.

**What Shopify API scopes does theme duplication and editing require?**
Section 14 discusses validating API scopes for the *security audit* feature, but theme read/write access is arguably more critical — it's the core product. If Shopify restricts or rate-limits theme API access, the entire code-editing feature is compromised. This validation isn't mentioned.

### Verdict
An engineer cannot build Section 3.4 from what's written here. The feature description is a user story, not an engineering spec. That's acceptable for a product brief — but the brief should at minimum acknowledge the open technical questions, the way Section 11 does for other risks.

---

## 2. Find the Contradictions

### Contradiction 1: "24/7 support" vs. "possibly just the founder"

Section 6.2 states: "24/7 human support, with full access to the merchant's interaction history." Section 12 then says: "This does not mean a full support team on day one — it scales over time. Initially the team is small (possibly just the founder)."

One person cannot provide 24/7 support. The document tries to resolve this by saying "the architecture supports it from the start" — but a merchant who sees "24/7 human support" as a product feature and then waits 12 hours for a response from a solo founder has a trust-destroying experience. The brief presents 24/7 support as a *product principle* (Section 7 calls trust principles "non-negotiable"), then immediately undercuts it with operational reality. This needs to be resolved: either the launch version explicitly does *not* promise 24/7, or there's a plan to staff it.

### Contradiction 2: "AI never states something with more confidence than the data supports" vs. no defined confidence thresholds

Section 5.2 establishes the core rule: "The AI never states something with more confidence than the underlying data supports." But what constitutes the underlying data? Performance scans produce numeric scores. App-to-script mapping (Section 4.2) is explicitly described as starting with only the top 50-100 apps and growing over time. So for the majority of Shopify apps (there are 10,000+ in the ecosystem), the AI has *no* attribution data.

The brief doesn't describe what the AI does when its data coverage is sparse. Does it say "I can't assess this app"? Does it guess? The confidence calibration system (Section 5.2) is described as adjusting language based on "data certainty," but the data certainty for app attribution will be *zero* for most apps at launch. The principle is stated; the operational reality of how it works with incomplete data isn't.

### Contradiction 3: Monetization gates vs. "the AI is the product"

Section 1 says: "The AI assistant is the product. The scanning and analysis is the engine underneath. The conversation is what merchants pay for." Section 8 then puts the AI behind the mid tier and limits it with interaction caps on all tiers.

If the AI is the product, then the free tier — which has no AI access — isn't really showing the product at all. It's showing the engine. The brief says the free tier should "demonstrate value and drive word of mouth," but if the value proposition is the AI conversation, and the free tier excludes it, the free tier demonstrates the *wrong* thing. This is a strategic tension the document should name explicitly rather than leave implicit.

### Contradiction 4: "We are in no rush" vs. the competitive landscape

Section 9.2 says "we are in no rush" and the product only launches when the AI is reliable. Section 10 identifies GrowthPilot AI as an existing competitor with "continuous monitoring + AI explanations." If GrowthPilot adds code editing while ShopSniffer is still tuning its AI layer, the core differentiator evaporates. The brief doesn't discuss time-to-market risk or what happens if the competitive window closes during the R&D phase.

---

## 3. Walk Through the Merchant's Worst Day

**Scenario: The AI recommends a code change. The merchant publishes the preview theme. Something breaks.**

### Step-by-step using only what the document specifies:

1. **The AI identifies a fixable issue** — say, a render-blocking script in the theme's `layout/theme.liquid`. It creates a duplicate theme, moves the script tag to defer loading, and explains the change in plain language (Section 3.4, 5.3).

2. **The merchant previews the result.** The document says they can preview, but doesn't specify *how*. Presumably via Shopify's built-in theme preview. Let's assume they click through a few pages and it looks fine.

3. **The merchant publishes the theme.** They're now live on the AI-modified code.

4. **Something breaks.** The deferred script was actually critical for the checkout flow — a third-party payment app injected it and it needs to load synchronously. The checkout page now throws a JavaScript error. Customers can't complete purchases.

5. **The merchant notices** — but when? The document mentions alerts for "regressions, new issues, or significant changes" (Section 3.5), but these are from *periodic scans*. If the next scan isn't for hours or days, the merchant discovers the problem from angry customers or failed orders, not from ShopSniffer.

6. **The merchant opens the app.** What do they see? The document doesn't describe an "undo last change" button or an emergency rollback flow in the UI. Section 7 says "the previous theme is preserved" and they can "revert by republishing the previous theme." But does the merchant *know* how to do this? The product is designed for non-technical merchants. Republishing a Shopify theme requires navigating to Shopify Admin → Online Store → Themes → finding the old theme → clicking "Publish." This is outside ShopSniffer's UI entirely.

7. **The merchant talks to the AI.** They say "something broke, fix it." Can the AI detect the checkout failure? The document doesn't describe any post-publish monitoring or automated health check after changes go live. The AI has scan data, not real-time production monitoring.

8. **The merchant escalates to human support.** Section 6.2 says human support has "full access to the merchant's interaction history." Good — they can see what the AI changed. But can the support person *undo* the change? The document doesn't describe whether the support team has theme-editing capabilities, or whether they guide the merchant through Shopify's admin to republish the old theme.

### Where it breaks down:

- **No post-publish health check.** The AI makes a change, the merchant publishes it, and then... nothing. There's no automated verification that the live store still works. This is the single biggest gap in the safety model.
- **No in-app rollback.** The rollback mechanism relies on Shopify's native theme management, which is outside the app's UI. For a non-technical merchant in a panic, this is a high-friction recovery path.
- **No real-time alerting.** Periodic scans won't catch a checkout-breaking change fast enough. The merchant needs to know within minutes, not hours.
- **The AI caused the problem but can't diagnose it in real time.** The AI's data sources are scan results and historical data — not live production telemetry. It can't see that checkout conversions just dropped to zero.

---

## 4. Walk Through the AI's Hardest Question

**"I installed three apps last week and my store got slower. Which one is causing it?"**

### Using only what the document describes:

1. **The AI needs historical performance data.** Section 4.5 says the system does "periodic automated scans to track trends" and can "correlate changes with specific events (app installed, theme updated)." So in theory, if scans ran before and after each app install, the AI can compare.

2. **The AI needs to know *when* each app was installed.** The document doesn't specify whether ShopSniffer tracks app install/uninstall events. Shopify provides webhooks for `app/installed` and `app/uninstalled` — but only for your *own* app. Knowing when *other* apps were installed requires either the Admin API scope to list apps (which Section 14 flags as needing validation) or inferring it from script changes between scans. If the three apps were all installed between two scan intervals, the AI can't distinguish which one appeared first.

3. **The AI needs app-to-script attribution.** Section 4.2 describes this as starting with the "top 50-100 popular apps" and growing over time. What if two of the three apps are obscure? The document says this explicitly: "This starts with the top 50–100 popular apps and grows over time."

4. **What happens with unknown apps?** The document doesn't say. The AI knows the store got slower (it has the scan data). It can see new scripts appeared (if the scans captured them). But it can't attribute those scripts to specific apps if they're not in the mapping database.

### What the AI should say but the document doesn't specify:

The AI would need to say something like: "Your store's load time increased by 1.2 seconds since last Tuesday. I can see three new scripts were added. I can identify one of them — it belongs to [App X] and is adding 340KB of JavaScript. The other two scripts are from apps I don't recognize yet. I'd recommend disabling apps one at a time to isolate the impact, starting with [App X] since I can confirm its contribution."

This is a *good* answer. But the document doesn't describe this fallback behavior. The confidence calibration system (Section 5.2) says ambiguous data produces "hedged language, not confident assertions" — but "hedged" is a vague instruction. Without explicit fallback patterns for partial-knowledge scenarios, the AI implementation is left to engineer judgment, which is exactly how you get inconsistent user experiences.

### Additional gap:
What if the merchant installed three apps but only one injected client-side scripts? The other two might only use backend APIs (webhooks, order processing). The AI can only see what's observable from the storefront — it can't see backend-only apps affecting performance through API latency or webhook processing. The document conflates "app impact" with "script impact" throughout Section 4.2 without acknowledging that some performance degradation from apps is invisible to storefront scanning.

---

## 5. Find the Scope Traps

### Features that sound simple but are massive engineering efforts:

**1. App-to-script mapping database (Section 4.2)**
The brief calls this a "long-term data asset" and says it "starts with the top 50-100 popular apps." Building and maintaining this is a product in itself. Apps update their scripts. CDN URLs change. Apps use dynamic script injection that varies by store configuration. The initial build requires someone to manually install 50-100 apps on test stores, record their script signatures, and create a mapping. Then it needs ongoing maintenance as apps update. The document frames this as a data collection task; it's actually a continuous data quality operation.

**2. Multi-agent AI verification (Section 5.2)**
"Multiple AI agents run behind the scenes" — an analysis agent, a verification agent, and confidence calibration. This triples the LLM cost per interaction (acknowledged in Section 11) but also triples the latency. A merchant asking "why is my store slow?" expects an answer in seconds, not 30 seconds while three AI agents deliberate. The document doesn't mention latency constraints at all. Furthermore, the verification agent needs to "fact-check claims against the raw scan data" — this requires structured tool use, not just prompt engineering. It's an AI engineering problem, not a prompt-writing problem.

**3. Security and app permissions analysis (Section 4.3)**
The document hedges this with a feasibility note, which is good. But even the fallback — "what's observable from the storefront (script tags, network requests)" — is a significant effort. Analyzing network requests at scan time means running a headless browser, capturing a HAR file, parsing it, identifying third-party domains, and mapping them to known services. This is essentially building a web security scanner on top of the performance scanner.

**4. Historical trend correlation (Section 4.5)**
"Correlating changes with specific events (app installed, theme updated)" requires a time-series data model, event ingestion from multiple sources, and a correlation engine. The current architecture uses SQLite with a flat scan record. This feature implies a fundamentally different data model.

### Features that could be cut without damaging the core product:

- **SEO Health (Section 4.4):** Useful but tangential. Dozens of existing Shopify SEO tools exist. Cutting it doesn't harm the "AI assistant that fixes your store" positioning.
- **Security/permissions audit (Section 4.3):** Already flagged as uncertain due to API scope approval. Could be deferred to v2 without weakening the launch product.
- **Post-session summaries via email (Section 6.3):** Nice to have, not core.

### Features that, if cut, would make the product pointless:

- **AI Code Editing (Section 3.4):** This is the stated differentiator. Without it, ShopSniffer is another dashboard.
- **AI Chat (Section 3.3):** The entire product positioning is "conversation as interface." Remove the chat, and you have a Lighthouse wrapper.
- **Performance scanning (Section 4.1):** The foundational data source. Without it, the AI has nothing to talk about.

---

## 6. Challenge the Monetization

### Scenario 1: Free tier merchant sees 12 findings, can't ask the AI

The free tier gives "a scan every X days" and "basic health status and findings." The merchant runs their scan, sees 12 findings. They're alarmed. They want to understand what's wrong. But AI access requires the mid tier.

**What happens?** The merchant sees a list of issues they can't interpret. Remember — the target user is "non-technical merchants who can't interpret PageSpeed reports" (Section 2). The free tier gives them exactly what they can't interpret: a report. Without the AI to explain it, the free tier experience is *the exact problem the product claims to solve.*

**Conversion or abandonment?** This could go either way. A well-designed upgrade prompt might convert them: "Want to understand these findings? Talk to ShopSniffer AI — upgrade to Mid tier." But it could also frustrate them: they installed an app that tells them things are wrong but won't explain what, unless they pay. The brief doesn't describe the free-to-paid conversion UX at all.

**Missing from the document:** What does the free tier dashboard actually show? "Basic health status and findings" — but what level of detail? Does the merchant see finding titles but not explanations? Severity but not remediation? The implementation can't be designed without knowing exactly what's gated.

### Scenario 2: Top tier merchant hits usage cap on day 15

The top tier has "the most generous AI interaction limits (still capped)" and "no unlimited plans." A power user hits their cap mid-cycle.

**What happens?** Section 8 says: "Clear messaging when a merchant approaches their limit, with the option to upgrade or wait for the next billing cycle." But there's nothing to upgrade *to* — they're already on the top tier. The document then says "that's an enterprise conversation or a usage-based overage model."

**Support burden:** This merchant is now stuck. They're paying the maximum, they have an active problem, and the AI won't talk to them. They'll contact support — the same support team that's "possibly just the founder." This creates exactly the support burden the product can't handle at launch.

**Can this be implemented?** "Exact pricing, tier boundaries, and specific caps to be determined." The caps aren't defined. The overage model isn't defined. The enterprise tier isn't defined. An engineer can't build the billing system, the usage tracking, or the limit enforcement from what's written here. This section is directional (acknowledged), but it's *too* directional — there are no constraints narrow enough to make architectural decisions from. For example: Are interactions counted per message, per conversation, or per scan triggered from chat? If per message, a merchant asking follow-up questions burns through their cap fast. If per conversation, what defines a conversation boundary?

---

## 7. What's Not in This Document That Should Be

### Data deletion and GDPR

The document mentions "data retention and privacy" in Section 11 as a known risk but provides zero specifics. For an app that stores: scan results containing store structure information, AI conversation logs, code change history, and merchant interaction records — GDPR compliance is not a footnote risk. It needs to answer: What data is stored? Where? For how long? What happens when a merchant requests deletion? What happens when a merchant uninstalls the app? Shopify requires apps to respond to data deletion requests via mandatory GDPR webhooks (`customers/data_request`, `customers/redact`, `shop/redact`). This is a Shopify App Store *requirement*, not an optional feature.

### What happens when a merchant uninstalls the app

Not mentioned anywhere. Shopify sends an `app/uninstalled` webhook. The app needs to: stop all scheduled scans, handle any in-progress scans, decide what to do with stored data (retain? delete? for how long?), and clean up any duplicate themes the AI created. If preview themes are left behind, the merchant has orphaned themes cluttering their Shopify admin.

### Multilingual support

Not mentioned. Shopify merchants operate globally. The AI is described as speaking "plain language" — is that English only? What happens when a Japanese merchant installs the app and starts chatting in Japanese? LLMs can handle multilingual input, but the scan findings, remediation steps, and plain-language changelogs are all presumably authored in English. This should at minimum be noted as a scope constraint.

### Shopify API versioning and breaking changes

Shopify releases a new API version quarterly and deprecates old versions on a rolling basis. The document doesn't mention API versioning. If the app is built against API version `2026-04` and Shopify deprecates it in `2027-04`, the app needs migration work. This is an ongoing operational cost.

### Password-protected and maintenance-mode stores

Performance scans (Lighthouse, storefront analysis) require HTTP access to the store. Password-protected stores (common during development or pre-launch) return a password page, not the actual store. Stores in maintenance mode behave similarly. What does the scanner do? Return empty results? Report the store as "inaccessible"? Attempt to authenticate? This affects every merchant who installs the app before their store is public.

### Store size variance

The document doesn't acknowledge the difference between a store with 5 products and one with 10,000+. Scan scope, duration, resource consumption, and finding volume all scale with store size. A scan of a 10,000-product store that takes 45 minutes has a completely different UX than one that takes 30 seconds. Does the AI mention "I found issues on 847 of your product pages"? How is that presented? Are findings aggregated by pattern or listed individually?

### Rate limiting and concurrent scans

What happens when 100 merchants all trigger scans simultaneously? The current BugSniffer architecture runs scans synchronously — this is already flagged in PROJECT_STATE.md as "not implemented yet (async scan processing / job queue)." But the product brief doesn't mention queuing, concurrency limits, or what the merchant sees when their scan is queued.

### Theme app extensions vs. traditional themes

Shopify is migrating toward theme app extensions and JSON templates (Online Store 2.0). The document doesn't specify which theme architecture the AI understands. A store using a vintage theme with a monolithic `theme.liquid` is fundamentally different from a modern OS 2.0 theme with JSON templates and sections. The AI's code editing capability needs to handle both — or explicitly scope to one.

---

## 8. What Would Kill This Product

**The single most likely reason this product fails: the AI code editing doesn't work reliably enough to ship, and without it, the product has no differentiator.**

Here's why:

Section 10 says the competitive position rests on: AI conversation as interface, AI code editing with preview safety, cross-category analysis, historical tracking, and human support. Of these, the first two are the actual differentiators. The others are "nice to have" features that existing tools already offer in some form.

AI code editing in Shopify themes is an extremely hard problem:
- Liquid is a niche templating language with limited LLM training data compared to mainstream languages.
- Themes are structurally complex — a typical theme has 100+ files with interdependencies between layouts, sections, snippets, and assets.
- Correctness is binary from the merchant's perspective: the store either looks right or it doesn't. A "mostly correct" code change is a broken store.
- The verification agent (Section 5.2) needs to validate code changes against the original theme, which requires understanding both Liquid rendering and the visual output. This is closer to visual regression testing than traditional code review.

Section 11 acknowledges "AI accuracy at launch" as a risk and Section 15 defines reliability thresholds. But the document's own strategy is: "the basic AI chat ships first; the verification layer gets tuned over time until accuracy is trustworthy." This means the product launches *without* reliable code editing — which means it launches without its differentiator.

If the code editing feature ships in a degraded state ("available but not reliable"), merchants will try it, see broken preview themes, lose trust, and leave 1-star reviews. If it doesn't ship at all in v1, the product is a dashboard with a chatbot — and the market already has those.

The document acknowledges this risk exists but doesn't provide a mitigation plan beyond "don't rush." A mitigation plan would include: what's the minimum viable version of code editing (e.g., only image optimization changes, which are low-risk)? What categories of fixes does the AI attempt first? What's the fallback product positioning if code editing takes 12 months longer than expected?

**This is a technical risk, not a market risk.** The market demand for "an AI that fixes my Shopify store" is clear. The question is whether it can be built to the reliability standard the product demands. The brief is honest about the difficulty but doesn't have a plan B.

---

## Summary of Critical Findings

| # | Finding | Severity | Section Reference |
|---|---------|----------|-------------------|
| 1 | No post-publish health check after AI code changes go live | Critical | 3.4, 7 |
| 2 | No in-app rollback mechanism — relies on merchant navigating Shopify admin | Critical | 3.4, 7 |
| 3 | Theme lifecycle management unspecified (duplication limits, cleanup) | High | 3.4 |
| 4 | Free tier demonstrates reports, not the AI — contradicts the value proposition | High | 1, 8 |
| 5 | 24/7 support promised as principle, impossible at launch | High | 6.2, 12 |
| 6 | GDPR/data deletion not designed — Shopify App Store requirement | High | 11 |
| 7 | App uninstall behavior not specified | High | (missing) |
| 8 | Usage caps undefined — can't architect billing or enforcement | Medium | 8 |
| 9 | AI fallback behavior for unknown apps not specified | Medium | 4.2, 5.2 |
| 10 | No latency requirements for multi-agent AI verification | Medium | 5.2 |
| 11 | Theme API scope validation not mentioned (only security scopes are) | Medium | 14 |
| 12 | Password-protected stores, maintenance mode not addressed | Medium | (missing) |
| 13 | Store size variance and scan scaling not addressed | Medium | (missing) |
| 14 | Multilingual support not scoped | Low | (missing) |
| 15 | Shopify API versioning/deprecation not mentioned | Low | (missing) |
| 16 | No plan B if AI code editing takes too long to reach reliability | Strategic | 9.2, 11, 15 |

---

*This stress test is intended to strengthen the document, not dismiss it. The brief is well-written, self-aware about many risks, and correctly structured as a product vision rather than an engineering spec. The findings above are the gaps that need to be closed before this brief becomes architecture.*
