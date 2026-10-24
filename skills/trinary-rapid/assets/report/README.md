# Report runtime assets

This pinned third-party stylesheet and the skill's own `report-theme.css` are
embedded into each rendered `report.html` so the report makes no runtime
resource requests. `report-theme.css` is the report's dark and light palette,
based on the trinary-agents dashboard; it is first-party and not pinned. The
renderer has no package dependencies. Keep the adjacent license file and the
notice block embedded in each rendered HTML page when distributing the asset
or page.

Copied unchanged from the trinary-agents dashboard assets, which were verified
from the exact npm package metadata and license file on 2026-10-18:

| File | Package and version | Source | License |
| --- | --- | --- | --- |
| `daisyui-5.7.50.css` | [`daisyui@5.7.50`](https://www.npmjs.com/package/daisyui/v/5.7.50), `daisyui.css` | [daisyUI repository](https://github.com/saadeghi/daisyui) | MIT, full text in `LICENSE-daisyui-MIT.txt` |

MIT redistribution requires the copyright and permission notice in copies or
substantial portions. The exact upstream license text is retained beside the
asset and embedded in rendered reports as an HTML comment.

The stylesheet contains inline `data:` SVG images whose markup declares the
standard `http://www.w3.org/2000/svg` XML namespace. These are namespace
identifiers, not resource references; nothing is fetched.

## Pinned file checksum

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `daisyui-5.7.50.css` | 1142434 | `6a2cf91a0e9a7da09cf8109c45c3fae171e8967122576043f2b94da47fdf6b64` |
