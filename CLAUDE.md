# CLAUDE.md

Guidance for working in the CostGraph documentation repository.

## Project overview

This repository is the CostGraph documentation site, built with **Mintlify** and
deployed to [docs.costgraph.ai](https://docs.costgraph.ai). Content is written in
**MDX** (Markdown plus Mintlify components). Navigation, theming, redirects, and
the OpenAPI wiring all live in `docs.json`.

**`docs.json` is hand-edited and is the single source of truth for navigation.**
There is no generator step. A page does not appear in the site until it is listed
in `docs.json`.

The site has two tabs:

- **CostGraph** the product docs. Groups: Get Started, CostGraph Operator,
  CostGraph Agent, Virtual Tags, MCP, Self-Hosted, and Integrations.
- **Pricing API** an OpenAPI reference plus its Getting Started, SDK, and
  Changelog pages. See [Pricing API tab](#pricing-api-tab) below.

## Repository layout

- `docs.json` navigation, theme, `redirects`, `contextual` options, and the
  Pricing API `openapi` source. Edit by hand.
- `index.mdx` the landing page.
- `costgraph/` product docs, grouped by area: `operator/`, `agent/` (plus the
  `costgraph/agent.mdx` overview), `self-hosted/`, `virtual-tags/`,
  `integrations/`, `mcp/`.
- `concepts/` conceptual pages (`how-it-works`, `tenancy`).
- `api-reference/` Pricing API `introduction`, `authentication`, and the
  `openapi.json` spec.
- `pricing-api/SDKs/` Pricing API SDK pages (`install`, `go`, `typescript`).
- `changelog/pricing/api.mdx` the Pricing API changelog. Per-product changelogs
  for the operator, agent, and self-hosted chart live inside their own area as
  `costgraph/<area>/changelog.mdx`, not here.
- `images/` screenshots and diagrams, referenced as `/images/...`. Most sit
  flat at the top of `images/`; a few areas have subfolders
  (`images/virtual-tags/`, `images/mcp/`). `images/logos/` holds provider logo
  SVGs used as `<Card>` icons.

## Content standards

**Front matter**: every `.mdx` page opens with YAML frontmatter. `title` is
required. Add a `description` on any real content page; it is the meta
description and the card subtitle. `icon` and `sidebar_position` appear
occasionally and are optional.

```mdx
---
title: Usage
description: "Create a tag, write the rules that fill it, and group your spend by it"
---
```

**Voice**: clear, direct, and calm. Write in the second person and the present
tense. Explain why before how. Match the tone of the existing pages, such as
`costgraph/self-hosted/overview.mdx`. Avoid hype.

**Simple over wordy**: headings are short noun phrases (`Generating tags`, not
`Two ways to generate tags`; `Overlapping rules`, not `When rules overlap`). Lead
with the point, prefer a tight sentence or a couple of bullets over a paragraph,
and cut any section that only restates the obvious. When in doubt, cut.

**Cut these** (a hard preference; write for a competent peer, do not perform):

- Payoff and reveal lines that congratulate the material or the reader: "This is
  the payoff of...", "The beauty of X is...", "notice how clean this is". State
  what happens and move on.
- Invented metaphor scaffolding used to sound clever: "the mental-model ladder",
  "Track 1 / Track 2", "make it do something". Use plain headings and sentences.
- Dramatic one-line fragments for effect: "Real APIs evolve.", "X is passive.".
  Fold the point into a normal sentence.
- Swipes at other tools or products: "unlike most tools", "the parts other docs
  skip". Explain the thing; skip the comparison.
- "the user" in a page that addresses the reader as "you". Stay in second person
  ("you", and "we" for shared steps).

**Hard style rules**:

- **No em dashes.** Rewrite the sentence with a comma, colon, or full stop
  instead of dropping the dash. Some older pages still contain them; do not add
  more.
- Use **bold** sparingly, for UI labels (`**Create new tag**`) and the
  occasional key term. It is not the tool for emphasis in running prose.
- Use backticks for code, paths, fields, and literal values: `docs.json`,
  `costgraph.ai/pricing-id.compute`, `service category`.
- Capitalize product names: CostGraph, Graph AI, Kubernetes, Helm, Prometheus,
  Mintlify.

**Mintlify components** (use them; do not hand-roll HTML). These are the ones
actually in use here:

- `<Note>` and `<Warning>` for callouts. (`<Tip>` and `<Info>` exist in Mintlify
  but are not used in this repo; prefer `<Note>`.)
- `<Steps>` / `<Step>` for ordered procedures.
- `<Card>` / `<CardGroup>` for next steps, option grids, and provider catalogues.
  A card icon is a Font Awesome name (`icon="tags"`) or a path to an asset
  (`icon="/images/logos/aws.svg"`).
- `<Accordion>` / `<AccordionGroup>` for optional or reference detail.
- `<Frame caption="...">` wrapping an `<img>` for a captioned screenshot; a plain
  inline screenshot is Markdown, `![alt text](/images/...)`.
- `<Tabs>` / `<Tab>` for alternative paths (for example install methods).
- `<Update label="YYYY-MM-DD" description="vX.Y.Z">` blocks for changelog
  entries, newest first (see any `costgraph/<area>/changelog.mdx`).
- Standard Markdown tables for comparisons and reference.
- ` ```mermaid ` fenced blocks for diagrams.
- Fenced code blocks carry a language only (` ```shell `, ` ```yaml `). There is
  no filename annotation on the fence; when a file name matters, put it in prose
  or write it into the command (`cat > my-values.yaml <<'EOF'`).

**Links**: cross-link with absolute doc paths (`/costgraph/virtual-tags/usage`),
no `.mdx` extension. Only link to pages that already exist; a link to a page you
have not created yet is a broken link. When a page is not built, describe it in
prose or a `<Note>` instead of linking.

**Page shape**: a typical overview or how-to page ends with a Next steps section:
one or more `<Card>` (or a `<CardGroup>`) pointing to the pages that follow. Keep
that pattern when it fits.

## Adding or changing a page

1. Create the `.mdx` file under the right area, for example
   `costgraph/<area>/<slug>.mdx`, with `title` frontmatter (and a `description`).
2. **Register it in `docs.json`** under the correct tab and group. Use nested
   groups for long sections (Integrations is split into `Cloud`, `AI / LLM`,
   `Databases`, and more). Group `icon` fields use Font Awesome names.
3. Add any images under `images/` (or an area subfolder that already exists) and
   reference them as `/images/<file>.png`.
4. Keep `docs.json` valid JSON and every internal link resolving.

### Moving or renaming a page

When a page's path changes, add an entry to the `redirects` array in `docs.json`
so old links keep working. A redirect can target a heading anchor:

```json
{ "source": "/costgraph/overview", "destination": "/costgraph/operator/overview" }
```

### Pricing API tab

The Pricing API reference is generated from an OpenAPI spec, not from `.mdx`
pages. The tab in `docs.json` sets `openapi` to the raw GitHub URL of
`api-reference/openapi.json`, and each endpoint page is an operation string such
as `"POST /pricing/compute"` listed under the tab's groups. Mintlify renders
those from the spec. To add or change an endpoint, edit `api-reference/openapi.json`
and list its `METHOD /path` string in `docs.json`. The hand-written pages on this
tab are `api-reference/introduction`, `api-reference/authentication`, and the
`pricing-api/SDKs/` pages.

## Screenshots and images

- Crop personal or account data out of product screenshots (account email,
  billing figures) before committing.
- Convert Apple exports first: a file that is HEIC mislabeled `.jpg` will not
  render in a browser. Check with `file`, convert with
  `sips -s format jpeg in.jpg --out out.jpg`.
- Match the wording in a page to the exact labels in its screenshots. When the UI
  says `is` and `View claims`, the prose says `is` and View claims.

## Accuracy and house rules

- Ground every feature claim in the real product or code. When a feature spans
  repositories or lives on an unmerged branch, flag what needs confirmation
  before publishing rather than guessing.
- Do not document capabilities that are only scaffolded and not yet wired up.
- Base documentation work on `origin/main`; the `docs.json` on `main` is the
  current navigation. Do not commit or open a PR unless asked.

## Before you open a PR

- `docs.json` parses as valid JSON.
- Every new page is registered in `docs.json`, and every internal link and image
  path resolves.
- Moved pages have a `redirects` entry.
- No em dashes, and product names are capitalized.

Preview is optional and there is no required local toolchain. If you have the
Mintlify CLI installed, `mint dev` serves the site locally; otherwise Mintlify
builds and deploys it from the repository.
