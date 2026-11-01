# Networks (Cytoscape.js)

Who knows whom, intro paths, dependencies, org links: an interactive Cytoscape.js graph, never rows of step pills, and never a force-directed hairball.

## Build

- Load a pinned Cytoscape from the CDN: `<script src="https://cdn.jsdelivr.net/npm/cytoscape@3.34.4/dist/cytoscape.min.js"></script>` (check the latest version on jsdelivr, then pin it). Never inline the library; it is 430 KB.
- Layered `preset` layout, top-down or left-to-right: one layer per hop (you, your contacts, their contacts, bridges, targets). Hand-set the order of each middle layer to cut crossings; order the target layer by the bridge that reaches each target. Stagger labels in a crowded layer (alternate y by about 50px).
- People are circles with their photo (`background-image` pointing at the same photo file the page's cards and tables use, `background-fit: cover`, and `background-image-crossorigin: "null"`, or Chrome blocks the image over `file://` with a CORS error) or an initials SVG (`data:image/svg+xml;utf8,` + `encodeURIComponent`, not base64). Status as a 3px border color (for example teal = left the company, slate = still there); dashed and faded for "no path".
- One edge style per relationship type. Dense many-to-many edges (who overlapped with whom) stay hidden until a node is clicked. Edge labels only on lit edges, `text-rotation: autorotate`.
- `userZoomingEnabled: false` and `userPanningEnabled: false` so the page scrolls on touch; height about 0.6 of the width, capped (420-680px); a legend and a Reset button ("Show the recommended path").

## Behavior

- Compute one canonical chain per node in the data step (fewest intros, then the bridge who reaches the most people, then direct connections over coworker-only links) and store it on the node. Never recompute "shortest" in the browser with different weights: the graph and the tables must name the same chain.
- Open with the recommended path already lit (the same chain the Next steps name).
- Click a node: light its canonical chain strongly, its other incoming paths faintly, fade everything else, and print the chain under the graph. Click a bridge: also show who it reaches. Click the background or You: back to the recommended path.
- Under 640px hide the canvas; the table carries the same chains.
- Pair the graph with a table (or a column in the main table) listing each target's chain.

## Test

Clicking needs the canvas in the viewport: `scrollIntoViewIfNeeded()` first, then click at `boundingBox + node.renderedPosition()` (expose the instance as `window.__cy` for tests). Compare the caption with the table cell for the same person.
