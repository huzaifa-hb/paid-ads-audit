# Native image generation

Use the image generation/editing capability available in the current ChatGPT or Codex
surface. Tool names and model versions are runtime details and must not be hardcoded.

- Text-to-image jobs require a final prompt, ratio, placement, and constraints.
- Image-editing jobs must attach every fidelity-critical reference image.
- Generated dimensions can differ from requested dimensions; inspect actual output.
- Return images inline when the surface manages artifacts. Save paths and manifests
  only when filesystem-backed outputs are exposed.
- If no image capability exists, deliver prompts and a manifest, not fake files.
- Never require user API keys for the default workflow.
