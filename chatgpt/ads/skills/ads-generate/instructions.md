# Native ad image generation

Generate production-ready concepts with the native image generation or editing
capability exposed by the current ChatGPT or Codex surface.

## Inputs

Use `campaign-brief.md` and `brand-profile.json` when present. Otherwise obtain the
offer, audience, objective, required platforms/placements, brand constraints, and any
reference images. Read only the applicable creative-spec references.

## Jobs

Build a manifest entry before generation for each requested concept and placement:

```json
{"job_id":"meta-concept-1-story","platform":"Meta","placement":"Story","aspect_ratio":"9:16","target_dimensions":"1080x1920","prompt":"...","constraints":[],"source_reference":null,"attempt":1,"status":"planned"}
```

Tell the user the job count before a large batch and obtain confirmation when the
request did not clearly authorize that volume. Do not invent provider costs.

For each job:

1. Compose a precise prompt from the concept, brand voice, palette, typography,
   composition, subject, environment, lighting, emotion, copy zone, and placement.
2. Pass supplied product, logo, person, or style images as actual image references.
   If the surface cannot include a required reference, stop that job rather than claim
   identity or product fidelity.
3. Generate at the closest supported aspect ratio. Do not promise exact pixel output.
4. Inspect the result for brief fidelity, brand alignment, crop and safe-zone safety,
   unintended text, visual artifacts, and product/logo identity.
5. Regenerate at most once when the result materially fails and the authorized batch
   permits it. Record the reason and attempt.
6. Validate actual dimensions when available. Resize or crop only if it preserves the
   subject and safe zones; never stretch.

In Codex, save returned files when paths are available under
`ad-assets/<platform>/<concept>/` and write `generation-manifest.json`. In ChatGPT web,
return images inline and provide the same manifest as a structured artifact or table if
filesystem paths are unavailable.

If native image generation is unavailable, deliver final generation-ready prompts,
placement specifications, and the manifest; clearly state that images were not created.

The manifest records surface, requested ratio, target and actual dimensions, reference
input, status/error, attempt, and quality notes. Use `references/agent-roles/visual-designer.md`
and `format-adapter.md` inline or as Codex subagent briefs.
