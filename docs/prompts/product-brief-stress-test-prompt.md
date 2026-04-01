# Stress-Test Prompt for ShopSniffer Product Brief

Paste this prompt into all three agents and the fresh agent. For the fresh agent, provide the product brief document directly — do not give repo access or any prior context.

---

Read the ShopSniffer Product Brief (`docs/plans/product-vision-draft.md` — or the document provided to you if you're a fresh agent with no repo access).

Your job is to break this document. Not to praise it, not to summarize it, not to say what's strong. Find what's weak, vague, contradictory, or missing. This document is about to become the foundation for all architecture and implementation decisions. Anything unclear here becomes a wrong assumption later.

Answer every question below. If the answer is "the document doesn't say," that's a finding.

**1. Try to build from this.**
Imagine you're the engineer assigned to implement the first feature tomorrow. Pick any feature described in the brief. Can you actually build it from what's written here? What questions would you need answered before you could start? List every ambiguity that would force you to stop and ask.

**2. Find the contradictions.**
Are there any places where two sections imply different things? For example, does the monetization section promise something the AI architecture section can't deliver? Does the trust model conflict with the feature set? Does the support model scale the way the document assumes?

**3. Walk through the merchant's worst day.**
The AI recommends a code change. The merchant publishes the preview theme. Something breaks — the store looks wrong, a product page 404s, or the checkout flow is disrupted. Walk through exactly what happens next, step by step, using only what the document specifies. Where does the process break down? What's missing from the safety net?

**4. Walk through the AI's hardest question.**
A merchant asks: "I installed three apps last week and my store got slower. Which one is causing it?" Using only what the document describes, can the system answer this? What data would it need? What if two of the apps are obscure and not in the app-to-script mapping database? What does the AI say when it doesn't know?

**5. Find the scope traps.**
Which features sound simple in the brief but are actually massive engineering efforts? Which ones have hidden dependencies that the document doesn't acknowledge? Which features, if cut, would not damage the core product — and which ones, if cut, would make the product pointless?

**6. Challenge the monetization.**
A merchant on the free tier runs their scan, sees 12 findings, and wants to ask the AI about them — but AI access requires the mid tier. What happens? Do they convert, or do they leave? Now flip it: a merchant on the top tier hits their usage cap on day 15 of the billing cycle. What happens? Does this create a support burden? Is the cap structure actually described well enough to implement?

**7. What's not in this document that should be?**
Think about: data deletion and GDPR, what happens when a merchant uninstalls the app, how the AI handles multiple languages, what happens when Shopify's API changes or breaks, how scan results behave when a store is password-protected or under maintenance mode, how the system handles stores with 10,000+ products vs. 5 products.

**8. What would kill this product?**
Not "what's risky." What's the single most likely reason this product fails, based on what's described here? Is it technical, market-based, or operational? Does the document address it or ignore it?

**Output format:**
For each section above, give specific findings with references to the document. Don't say "the monetization section could be more specific" — say exactly what's missing and why it matters. If you find nothing wrong in a section, say so and explain why you're confident.
