# Native product advertising photoshoot

Create ad-ready product photography using the native image-editing capability available
in ChatGPT or Codex.

## Intake

Obtain the product image, brand profile or visual direction, desired styles, platforms,
placements, and aspect ratios. Default styles are Studio, Floating, Ingredient/Material,
In Use, and Lifestyle, but generate only what the request needs.

When a product image is supplied, pass it as an actual image reference and preserve
geometry, materials, packaging, colors, labels, logo, and distinctive details. If the
surface cannot pass the image to the editing tool, do not claim a faithful product
render. A description-only result is concept photography and must be labelled as such.

## Workflow

1. Inspect the source image and identify fidelity-critical details.
2. Create a job manifest using the same fields as `skills/ads-generate/instructions.md`.
3. Write one prompt per style and placement, including composition and crop-safe zones.
4. Generate or edit through the native image capability.
5. Inspect fidelity, brand fit, lighting, perspective, artifacts, text/logo integrity,
   and crop safety. Regenerate at most once for a material failure.
6. Return images inline in ChatGPT. In Codex, save available files under
   `ad-assets/photoshoot/<style>/` and write `generation-manifest.json`.

If generation is unavailable, return final prompts and the shot list without implying
that images were produced.
