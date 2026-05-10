# JSON to TypeScript / Zod / Valibot — VS Code extension

Convert JSON in your editor selection or your clipboard into a **TypeScript interface**, a **Zod schema**, or a **Valibot schema** without leaving the editor. The output opens in a new untitled doc you can copy, save, or paste into your project.

This extension is the 6th artifact in the json-to-ts parity lineage:

1. Hosted UI — [json-to-ts-app.netlify.app](https://json-to-ts-app.netlify.app/)
2. npm CLI — [`@solvohq/json-to-ts`](https://www.npmjs.com/package/@solvohq/json-to-ts)
3. HTTP API — [`/api/convert`](https://json-to-ts-app.netlify.app/api/)
4. GitHub Action — [SolvoHQ/json-to-ts-action](https://github.com/SolvoHQ/json-to-ts-action)
5. Embed widget — [iframe at `/embed/`](https://json-to-ts-app.netlify.app/embed/)
6. **VS Code extension** (this repo)

All six surfaces share the same emitter algorithm. The extension calls the public `/api/convert` endpoint by default, so emitter upgrades reach you without a re-install.

## Install

The extension is currently distributed as a `.vsix` attached to the [`vscode-v0.1.0` release on SolvoHQ/json-to-ts](https://github.com/SolvoHQ/json-to-ts/releases/tag/vscode-v0.1.0). Marketplace listing is a follow-up.

Download the `.vsix`, then:

```bash
code --install-extension json-to-ts-0.1.0.vsix
```

Or in VS Code: **Extensions** panel → **…** menu → **Install from VSIX…**.

## Use

Two commands, both available in the command palette (`Cmd+Shift+P` / `Ctrl+Shift+P`):

| Command | What it does |
|--|--|
| **JSON to TS: Convert Selection (or Document)** | Reads your current text selection. If the selection is empty, reads the entire active document. |
| **JSON to TS: Convert Clipboard** | Reads JSON from the system clipboard. Useful when you've just copied a payload from a browser network tab, a logging tool, or a docs page. |

After running, you'll see a quick-pick to choose the output mode (`ts` / `zod` / `valibot`). The result opens in a new untitled TypeScript document next to your editor.

### Walkthrough

```jsonc
// Select this in any open file:
{
  "id": 42,
  "email": "ada@example.com",
  "tags": ["admin", "early-access"]
}
```

Run **JSON to TS: Convert Selection**, choose `ts`, and a new doc opens with:

```ts
interface Root {
  id: number;
  email: string;
  tags: string[];
}
```

Run again, choose `zod`, and you get:

```ts
import { z } from "zod";

const RootSchema = z.object({
  id: z.number(),
  email: z.string(),
  tags: z.array(z.string()),
});
```

## Settings

| Setting | Default | What it controls |
|--|--|--|
| `jsonToTs.apiUrl` | `https://json-to-ts-app.netlify.app/api/convert` | Conversion endpoint. Override only if you self-host the [HTTP API](https://json-to-ts-app.netlify.app/api/). |
| `jsonToTs.rootName` | `Root` | Name of the generated root interface / type / schema. |

## Why call the API instead of bundling the emitter?

The HTTP API is the single source of truth for the algorithm. The other 5 surfaces (the [hosted UI](https://json-to-ts-app.netlify.app/), the [`@solvohq/json-to-ts` CLI](https://www.npmjs.com/package/@solvohq/json-to-ts), the GitHub Action, the embed widget, and now this extension) are parity-checked clients of it. Bundling the emitter into the extension would create a copy that drifts on every emitter upgrade and force users to re-install for fixes. Calling `/api/convert` keeps your install permanently fresh.

If your security policy forbids outbound HTTP from VS Code, point `jsonToTs.apiUrl` at a self-hosted copy of the function or use the npm CLI offline:

```bash
echo '{"a":1}' | npx @solvohq/json-to-ts --mode zod
```

## Privacy

The JSON you select is sent over HTTPS to `json-to-ts-app.netlify.app/api/convert` for conversion and is **not logged** beyond Netlify's standard request access logs (no body capture, no analytics on payloads). The API has no auth, no cookies, no tracking. Treat it like any other public converter — don't paste secrets.

## Links

- Live tool — [json-to-ts-app.netlify.app](https://json-to-ts-app.netlify.app/)
- HTTP API docs — [/api/](https://json-to-ts-app.netlify.app/api/)
- One of the per-shape landing pages — [Stripe webhook → TypeScript](https://json-to-ts-app.netlify.app/stripe-webhook-to-typescript/)
- Source — [github.com/SolvoHQ/json-to-ts/tree/main/vscode](https://github.com/SolvoHQ/json-to-ts/tree/main/vscode)
- Issues — [github.com/SolvoHQ/json-to-ts/issues](https://github.com/SolvoHQ/json-to-ts/issues)

## License

MIT — see [LICENSE](LICENSE).
