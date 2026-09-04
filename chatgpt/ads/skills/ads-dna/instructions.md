# Brand DNA extraction

Extract a reusable brand profile from a website and supplied brand assets.

## Workflow

1. Validate the URL and use the current surface's browser, web-fetch, or connected-site
   capability to inspect the homepage plus only relevant product/service and about pages.
2. Capture or inspect rendered pages when the available browser supports screenshots.
   If rendering is unavailable, distinguish DOM/text-derived conclusions from visual
   observations.
3. Extract logo usage, palette, typography, imagery, layout rhythm, tone, value
   proposition, audience, offers, proof, calls to action, and prohibited treatments.
4. Record source URLs and retrieval date. Do not infer exact fonts or colors when they
   cannot be observed; label estimates.
5. Create `brand-profile.json` when files are supported; otherwise return the same JSON
   as a structured artifact in chat. Follow `references/brand-dna-template.md`.

Do not require a local browser script or provider-specific path. Respect site access,
robots, authentication, and copyright constraints. Use supplied first-party brand files
as stronger evidence than inferred website styling.
