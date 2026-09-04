# DTC E-Commerce Decision Frameworks

<!-- Added: 2026-05 | Source: Huzaifa Binyameen DTC Growth Marketer frameworks -->
<!-- Use: Applied by audit-meta and audit-budget agents when account is e-commerce/DTC -->

---

## 1. DTC Unit Economics: Deriving Break-Even

Before evaluating any ROAS or CAC target, calculate the brand's actual break-even from their unit economics. Never accept a stated target at face value.

### Formula

```
Variable Cost Rate = COGS% + Shipping% + Payment Processing% + Returns%
Contribution per Order = AOV × (1 − Variable Cost Rate)
Break-Even CAC = Contribution per Order
Break-Even ROAS = AOV / Contribution per Order
                = 1 / (1 − Variable Cost Rate)
```

### Typical DTC Variable Cost Ranges (for calibration only — always get actuals)

| Cost Component | Typical Range |
|----------------|--------------|
| COGS | 25–40% of AOV |
| Shipping + fulfillment | 8–15% of AOV |
| Payment processing | 2–3% of AOV |
| Returns (category-dependent) | 5–15% of AOV |
| **Total variable costs** | **40–73% of AOV** |

### What to Ask the Brand

- What is their blended variable cost as a % of revenue?
- What is their first-order contribution margin target?
- What LTV assumptions underpin their CAC target (if any)?

### How to Classify a Stated CAC/ROAS Target

| If stated ROAS is... | It means... | Audit flag |
|----------------------|-------------|------------|
| Below break-even ROAS | Losing money on every first order | FAIL — not a profitability target, a growth-at-loss bet. Flag explicitly. |
| At break-even | Zero contribution on first order | WARNING — sustainable only with strong LTV |
| 1.5–2× break-even | Healthy profitability | PASS for most DTC businesses |
| 3–4× break-even | Top-decile, achievable at scale | Excellent if maintained |

---

## 2. Staged ROAS Progression Model

Different playbooks apply at different ROAS stages. Audits must assess which stage the account is currently in before recommending tactics — applying scale tactics to a below-break-even account accelerates losses.

```
Stage 1: Stop losing money → reach break-even
  Playbook: Tracking integrity, campaign consolidation, kill worst ad sets,
            fix structural issues (ad set fragmentation, creative fatigue)

Stage 2: Break-even → industry-healthy (1.5–2× break-even ROAS)
  Playbook: Creative testing pipeline, offer optimization, funnel fixes (landing page, mobile CVR)

Stage 3: Healthy → efficient scale (3–4× break-even)
  Playbook: Lookalike expansion, new creative angles, UGC scaling, LTV-based CAC reinvestment

Stage 4: Efficient → top-decile (4×+ break-even)
  Playbook: Incrementality testing, cross-channel expansion, retention loop,
            post-purchase survey attribution
```

### Audit Instruction

1. Calculate break-even ROAS from brand's variable costs (Section 1)
2. Identify current stage from account ROAS vs break-even
3. Flag if tactics being recommended (by the brand or current account structure) are mismatched to the current stage
4. Set staged milestone targets, not just the final target

---

## 3. Learning Phase Budget Adequacy Math

The existing meta-audit.md check M13 flags "Learning Limited" status. This framework goes one step further: calculate whether the current budget is structurally capable of exiting learning phase, regardless of status.

### Formula

```
Meta learning phase exit: ≥50 purchase events in 7 days per ad set
Required purchases per day = 50 / 7 ≈ 7.1
Minimum daily budget per ad set = Required purchases/day × Target CPA

Example logic: If target CPA is $40 → minimum = 7.1 × $40 = ~$285/day per ad set
```

### Audit Check

```
1. Get total daily budget and number of active ad sets
2. Calculate average daily budget per ad set = Total daily / Number of ad sets
3. Calculate minimum required = (50/7) × target CPA
4. If average per ad set < minimum required → STRUCTURAL FAIL
   → No optimization will fix this; consolidation is required
5. Calculate how many ad sets the current budget can actually support:
   Max viable ad sets = Total daily budget / Minimum required per ad set
```

### Diagnostic Table

| Situation | Verdict | Fix |
|-----------|---------|-----|
| Budget per ad set ≥ minimum required | PASS — can exit learning | Optimize creative and targeting |
| Budget per ad set 50–100% of minimum | WARNING — borderline | Consolidate to fewer ad sets |
| Budget per ad set < 50% of minimum | FAIL — structurally impossible | Consolidate aggressively before any other optimization |

---

## 4. New-Customer ROAS Isolation

Platform ROAS includes returning customers who would have bought regardless of the ad. New-customer ROAS is the honest signal for whether paid acquisition is working.

### Methodology

1. Pull Meta-attributed purchases for the period (from Ads Manager)
2. Segment those orders in Shopify by customer type (new vs. returning) using the source filter
   - Method: Filter orders where `customer.orders_count == 1` (first-time buyer) AND source/UTM matches Meta
3. Calculate new-customer ROAS = Revenue from new customers only / Meta spend
4. Compare to blended platform ROAS

### What the Gap Reveals

| If new-customer ROAS is... | Interpretation |
|----------------------------|----------------|
| Close to blended ROAS (< 15% difference) | Account is primarily acquiring new customers — good |
| 20–40% below blended ROAS | Significant mix of returning customers credited to Meta — retargeting is high or attribution window is long |
| > 40% below blended ROAS | Platform ROAS is significantly inflated by returning customer credit — new acquisition may be at or below break-even |

### When to Flag

Flag in audit if new-customer ROAS cannot be calculated (no Shopify source attribution) — this is a measurement gap. Recommend UTM tagging + Shopify source tracking as a quick win.

---

## 5. MER Trend vs Platform ROAS Trend Diagnostic

**Key principle:** MER and platform ROAS have different denominators (MER includes all revenue sources; platform ROAS only counts attributed revenue), so comparing absolute values is meaningless. What matters is whether the TRENDS move together.

### How to Run the Diagnostic

```
Step 1: Calculate MER by week for the last 8–12 weeks
        MER = Total Shopify Revenue / Total Ad Spend (all platforms)

Step 2: Calculate platform ROAS by week for the same window

Step 3: Plot both trends. Compare direction of movement, not absolute values.
```

### Interpretation

| MER trend | Platform ROAS trend | Conclusion | Action |
|-----------|---------------------|------------|--------|
| Flat or stable | Sharp drop | Likely tracking break — platform is seeing fewer attributed events but business is fine | Fix tracking before touching campaigns |
| Both dropped | Both dropped | Real performance decline | Investigate campaign, creative, funnel |
| Both rose | Both rose | Real improvement — trust the signal | Scale carefully |
| MER dropped | Platform ROAS flat or rose | Organic/email/direct traffic declined, or paid spend increased without revenue lift | Check organic channels, not just paid |

### Tracking Integrity Check (always run before MER comparison)

Compare: Meta-reported purchase events → Shopify Meta-attributed orders (same window)
- If ratio diverged from its historical pattern → tracking break first
- Check: CAPI event dedup rate, server-side GTM deployment log, recent theme updates, new Shopify app installs

---

## 6. Creative Fatigue vs Audience Saturation

These require different fixes. Misdiagnosing one as the other keeps accounts stuck.

### Diagnostic Table

| Signal | Creative Fatigue | Audience Saturation |
|--------|-----------------|---------------------|
| CTR | Drops for affected creatives | Holds steady or drops slowly across all |
| CPM | Stable or slightly declining | Rising — fewer eligible users in auction |
| Frequency | Rising within specific creatives | Rising across all creatives in the ad set |
| Hook rate (3s video) | Drops sharply over time | Holds — new viewers still respond to hook |
| Scope | Affects specific creatives | Affects all creatives simultaneously |

### How to Diagnose

```
Pull: Frequency, CPM, CTR broken out by individual creative over last 14 days

If CTR dropped but CPM held flat or fell → Creative fatigue
  Fix: New creatives, same broad audience

If CPM rose and CTR stayed relatively flat across all creatives → Saturation signal
  Fix on broad Advantage+ accounts: New creative ANGLES that speak to different buyer
  types (different pain points, different formats, different narratives) — NOT
  new audience segments, because the algorithm already finds those. Different angles
  unlock different audience subsets within the same broad targeting.

If both moved → Both present, but creative is faster to fix
```

### Note on Saturation at Scale

At typical DTC spend levels (<$300/day), true audience saturation in a broad US campaign is unlikely given the size of the total addressable market. What presents as saturation is almost always creative fatigue across all running creatives. Reserve the saturation diagnosis for large-budget accounts with documented impression share exhaustion.

---

## 7. DTC Funnel Benchmarks and Prioritization Method

See `benchmarks.md` → `## DTC E-commerce Funnel Benchmarks` for rate benchmarks by category.

### Prioritization Method

Do not prioritize funnel fixes by relative drop rate alone. Prioritize by: **volume of visitors lost × benchmark gap**.

```
Priority Score = (Visitors lost at stage) × (Gap between current rate and benchmark midpoint)

Example:
  PDP→ATC: 5,000 visitors lost, rate is 7% vs 12% benchmark midpoint → Gap = 5pp
  Priority Score = 5,000 × 5 = 25,000

  Checkout→Purchase: 150 visitors lost, rate is 55% vs 70% benchmark midpoint → Gap = 15pp
  Priority Score = 150 × 15 = 2,250

  → Fix PDP→ATC first despite smaller relative gap, because the volume impact is far larger
```

### Revenue Impact Formula

```
Incremental purchases from X% lift at stage N =
  (Current visitors at stage N) × (Current rate × (1 + X%)) - Current purchases through stage N

Flow-through: multiply by downstream conversion rates to get final purchase count
Annualized revenue = Incremental monthly purchases × AOV × 12
```

---

## 8. Mobile CVR Optimization — DTC

For DTC Shopify accounts where mobile traffic is the majority but converts below desktop rate, address friction points in this order:

| Priority | Fix | Why It Works | How to Measure |
|----------|-----|-------------|----------------|
| 1 | Sticky ATC bar + move primary ATC above the fold | Reduces distance between decision and action. If ATC requires scrolling to reach, a portion of ready-to-buy users never complete the action. Worst case: neutral. | ATC rate and downstream checkout rate before/after. CVR by device. |
| 2 | Dynamic checkout buttons on PDP (Shop Pay, Apple Pay, Google Pay) | Skips checkout form entirely for users already enrolled. Removes the single biggest friction point for a decided buyer. | Checkout completion rate by payment method. Shopify analytics CVR by device. |
| 3 | Image performance: WebP format, lazy load, touch-optimized zoom | Sensory products (bedding, apparel, beauty) sell on visual quality. Slow-loading images hurt both engagement and conversion. | PageSpeed Insights LCP before/after. CVR by device. |
| 4 | Trust block above fold on mobile PDP: star rating, review count, shipping guarantee, return policy, certifications | Premium products require both product risk and purchase risk to be resolved. Placing trust signals near price and ATC removes the main hesitation points. | ATC rate from PDP. Scroll depth on mobile. |
| 5 | Replace dropdown variant selectors with tap-friendly swatches/button groups; show OOS variants greyed not hidden | Dropdowns on mobile require precise taps and are error-prone. Greyed OOS signals scarcity rather than confusion. Reduces checkout errors from wrong variant selection. | ATC rate by variant. Checkout abandonment rate. |

### Diagnostic Tools

- Microsoft Clarity: heatmaps, rage-clicks, session recordings (filter to mobile first)
- GA4 enhanced ecommerce: view_item → add_to_cart event lag, time-on-PDP distribution
- PageSpeed Insights: mobile LCP — if above 4s, fix speed before anything else on the page

---

## 9. Performance Drop 7-Step Triage

Run in this order. Fastest/cheapest checks first. Do not jump to campaign changes before ruling out structural causes.

| Step | Check | Data to Pull | What You're Looking For |
|------|-------|-------------|------------------------|
| 1 | **Tracking integrity** | Platform purchase events vs CRM/Shopify Meta-attributed orders (same window). CAPI dedup rate, EMQ score, server GTM log, theme update history, recent Shopify app installs | Did the ratio of platform-attributed to Shopify-source orders diverge from its historical pattern? If yes → tracking break. Fix before anything else. |
| 2 | **MER trend vs platform ROAS trend** | MER by week + platform ROAS by week for last 8–12 weeks | If MER held flat while platform ROAS dropped → tracking issue (Step 1 fix). If both trends dropped together → real performance decline, proceed to Step 3. |
| 3 | **Funnel decomposition** | CPM, CTR, CPC, ATC rate, checkout initiation rate, purchase rate, AOV — week over week for last 6 weeks | Which specific metric moved? CPM rise = auction pressure. CTR drop = creative or ad disapproval. LP CVR drop = site issue. AOV drop = product mix or promo change. Each diagnosis → different fix. |
| 4 | **Creative and frequency audit** | Top-spending creatives by week, frequency by ad set, hook rate trend, creative age, ad-level status history | Frequency >3 + CTR declining = fatigue. Frequency stable + CTR dropped across all creatives = check for ad disapprovals or competitor entry. Any ad disapprovals in last 30 days? |
| 5 | **Recent changes audit** | Platform Activity Log (last 30 days), Google auto-applied recommendations log | Did anyone (or any auto-apply) change budget, audience, optimization event, attribution window, or bid strategy? Auto-applied recommendations in Google can silently damage accounts. |
| 6 | **External factors** | GA4 by source/medium (last 6 weeks), branded search trend (Google Trends), competitor spend check (Meta Ad Library), industry promo calendar | Did organic + branded search drop alongside paid? If yes → off-platform cause (PR, supply issue, news). Did a competitor launch a major offer or flood the auction? |
| 7 | **Site and inventory health** | Shopify uptime log, PageSpeed Insights for last 30 days, top-product OOS status, return rate, support ticket volume | Theme update broke ATC on iOS Safari? Top SKU went OOS and suppressed CVR? Return surge signals product or fulfillment issue that ads cannot fix. |

### Escalation Criteria

**Continue optimizing** if: tracking is healthy, MER trend confirms real dip, root cause identified in steps 3–7, corrective changes show signal within 5–7 days.

**Escalate** if: root cause requires dev resources, supply/pricing/PR issue outside ad account, 14 days of corrective work produced no recovery. If 14 days of optimization haven't moved the needle, the problem is not in the ad account.

---

## 10. Amazon + DTC Cross-Channel Frameworks

### A. Email Suppression to Reduce Wasted CAC

Sync the Klaviyo "engaged in last 90 days" segment as a suppression audience in Meta Custom Audiences and Google Customer Match. The brand can reach these people for free via email. Paying to acquire them again through paid prospecting is wasted spend.

Expected impact: 10–20% reduction in blended CAC by reallocating spend to genuinely new audiences. Scales with email list size.

Secondary tactic: Build source-tagged Klaviyo flows by acquisition source via UTM. Abandoned-cart and post-purchase flows that match the original ad angle (offer, creative hook) convert at 15–25% higher rate than generic flows.

### B. Amazon Brand Referral Bonus (BRB)

BRB pays brand-registered sellers ~10% of revenue (credited against referral fees) on Amazon sales from external traffic tracked via Amazon Attribution tags.

Three tactical applications:
1. **Secondary "Buy on Amazon" button on DTC PDPs** tagged with Attribution link. Captures the Amazon-intent buyer segment without losing them entirely. Primary ATC stays the priority.
2. **Tag top-of-funnel DTC content** (comparison blogs, gift guides, category articles) with Attribution links to Amazon listings. Turns organic-bound traffic into a measurable, credited revenue stream.
3. **Use BRB attribution data as creative feedback** — which content topics and formats drive Amazon conversions tells you which buyer intents and messages are converting, informing DTC creative and targeting.

### C. Price Parity Decision Logic

When Amazon runs a discount (coupon, lightning deal, etc.):

```
Do not automatically match. Ask:
  1. Is the DTC offer already differentiated (exclusive bundle, colorway, gift packaging, extended warranty)?
     → If yes: maintain DTC price. The value proposition is already distinct.

  2. Is the SKU commoditized and is DTC CVR measurably dropping during the Amazon promo?
     → Value-match first (free gift, loyalty credit, free shipping upgrade) before price-matching.
     → If CVR still drops materially, match the effective value for that window only.

  3. Is this a long-running structural discount, not a flash event?
     → Revisit DTC SKU differentiation strategy. Sustainable parity requires differentiated value, not permanent price matching.

Rule: Compete on value before competing on price. Discounting DTC trains buyers to wait for sales,
      which degrades LTV and brand positioning over time.
```

---

## 11. Attribution Three-Numbers Framework

When platform ROAS, GA4, and Shopify report different numbers for the same period, they are not contradicting each other. Each answers a different question.

### Why They Differ

| Source | Attribution Model | What it counts | Why it's higher/lower |
|--------|------------------|----------------|----------------------|
| Meta Ads Manager | 7-day click + 1-day view (default 2026) | Any purchase that touched a Meta ad in that window, including view-throughs and returning customers | Over-credits: takes credit for view-throughs and last-touch on purchases other channels influenced |
| Google Analytics 4 | Data-driven (cross-channel) | Deduplicates across channels, no view-through | Under-credits Meta: if user clicked Google ad after Meta ad, Google gets GA4 credit |
| Shopify | Last UTM click | Only purchases with a Meta UTM as the last tracked parameter before purchase | Lowest: breaks on mobile in-app browsers, dark social, cross-device, view-through — all common on Meta |

### Which to Use When

| Decision | Use | Why |
|----------|-----|-----|
| Optimizing within Meta (bid strategy, creative, targeting) | Meta platform data | Meta's algorithm trains on its own event stream. Use it — but verify event signal quality (CAPI, EMQ, dedup) |
| Cross-channel budget allocation | MER + GA4 (cross-channel model) | MER gives business-level truth; GA4 deduplicates; neither model is perfect but together they're more reliable |
| Business-level profitability judgment | MER | Total revenue ÷ total ad spend. No attribution model, no overclaiming. |
| Explaining performance to leadership | MER as primary, platform ROAS as secondary context | Avoids the "which number is right" debate |

### CEO Explanation Template

> "There is no single 'real' ROAS. Meta, GA4, and Shopify each answer a different question about the same purchases. Meta reports highest because it claims credit for any purchase that saw one of our ads in the last 7 days. GA4 is lower because it deduplicates when multiple channels touched the same buyer. Shopify is lowest because it can only see UTM tags, which break on mobile and social. The number I use to run the business is MER — total revenue divided by total ad spend — because it doesn't depend on any attribution model. Our current MER is [X]. Platform ROAS tells me whether each channel is doing its job. MER tells me whether the whole engine is profitable."

### In-Platform Signal Quality Note

Optimizing on platform ROAS assumes the optimization event signal is accurate and aligned with business goals. Before accepting in-platform ROAS for optimization decisions, verify:
- CAPI is active and dedup rate ≥90% (check M02, M03 in meta-audit.md)
- EMQ score is ≥8.0 for Purchase events (check M04)
- The optimization event is new-customer purchase, not generic purchase (see Section 4 of this file)
- Attribution window matches business decision-making model (check M35)
