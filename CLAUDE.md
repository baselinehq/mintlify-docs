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

## Style guide

Pages follow the
[Google developer documentation style guide](https://developers.google.com/style).
The rules that matter most here, in the order they usually bite:

- **Critical information first.** Lead every page and every paragraph with the
  point. Readers scan; the last sentence of a paragraph is the one they skip.
- **One idea per paragraph, under 26 words per sentence.** Split rather than
  join. A single-sentence paragraph is fine.
- **Second person, present tense, active voice.** "CostGraph reports", not
  "will report" or "is reported by CostGraph".
- **Contractions.** Use the common ones, and prefer negation contractions:
  "doesn't" is harder to misread than "does not".
- **Prescriptive, not exhaustive.** Give one path. "Must" for a requirement,
  "we recommend" for advice, "can" for an option. Never "should".
- **No excessive claims.** No superlatives, no "ensure" or "guarantee", no
  comparisons with other products. State what the software does.
- **Conditions before instructions.** "If you self-host Lago, set **API URL**",
  not a question and not the condition at the end.
- **Procedures.** Each step starts with an imperative verb, does one thing, names
  where it happens before what to do, and carries its result in the same
  paragraph. Prerequisites go in a **Before you begin** list, not inside steps.
- **UI.** Bold the visible label. Click a button, select an option, enter text.
  Menu paths use bold and a greater-than sign: **Settings > API keys**.
- **Headings.** Sentence case. Task headings are bare verbs (`Connect`,
  `Tag spend by customer`); concept headings are noun phrases (`Event payload`).
  No `-ing` first words, no punctuation, no questions.
- **Notices.** A `<Note>` or `<Warning>` holds something the reader can skip
  and still succeed. Anything that decides whether the setup works is body
  text. Never two notices back to back; rarely more than one per page.
- **No directional language.** "The following table", not "the table below".
- **Tables.** Introduce with a full sentence. Three or more facts per row, or
  use a list.
- **Don't pre-announce.** Document what exists today. No "until X lands".

### Shared content

When several pages describe variants of one feature, put everything they share
on one overview page and cut each variant page to what only it does. The
[Billing exports](/costgraph/integrations/exports/overview) section is the
model: the overview owns the mechanism, the tag rules, and the nightly
behavior, opens with a comparison table of how the platforms differ, and each
platform page is 40 to 70 lines in a fixed shape:

1. One-sentence lead naming what the platform bills, with a link to the
   overview.
2. **Before you begin**: what must exist on the platform first.
3. **Connect**: the `<Steps>`, platform-specific detail only.
4. **Tag spend by customer**: what the tag value must be and what happens to an
   unknown one.
5. The payload and the aggregation it needs.
6. **<Platform> behavior**: the one or two things only this platform does.

Copying a sibling page and swapping the product name is how the duplication
starts. Write the shared page first.

### Review process

When reviewing or rewriting a page:

1. Read the diff against `origin/main`, then read the page top to bottom as a
   reader would. Mark every paragraph that repeats a sibling page or restates
   the paragraph before it.
2. Compare the register with a recent post on
   [blog.costgraph.ai](https://blog.costgraph.ai): the problem in one or two
   sentences, then the mechanism, no throat-clearing.
3. Move shared material to the overview. Cut what is left to the fixed shape.
4. Turn each notice into body text unless the reader can skip it.
5. Run `scripts/style-lint.py <files>` and fix every error. Read the warnings;
   most are real.
6. Check the frontmatter `description` is specific to the page, not shared with
   its siblings.

### Enforcement

`scripts/style-lint.py` checks the mechanical rules: em dashes, spaced hyphens
used as dashes, ASCII arrows, `should`, `simply`, `please`, `e.g.`, `i.e.`,
`in order to`, `click on`, missing descriptions, and back-to-back notices. It
warns on sentence length, `-ing` headings, `will`, `just`, directional words,
and absolutes. It runs on every pull request against the changed pages
and fails on errors. Run it locally with no arguments to lint what you changed,
or pass paths. Older pages have known hits; fix them when you touch the page.

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
- `scripts/style-lint.py` passes on the pages you changed.

Preview is optional and there is no required local toolchain. If you have the
Mintlify CLI installed, `mint dev` serves the site locally; otherwise Mintlify
builds and deploys it from the repository.
