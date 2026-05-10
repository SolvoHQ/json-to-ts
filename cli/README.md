# @solvohq/json-to-ts

> JSON → TypeScript interfaces, Zod schemas, or Valibot schemas. CLI + library — same emitters as the live tool at **[json-to-ts-app.netlify.app](https://json-to-ts-app.netlify.app/)**.

[![npm version](https://img.shields.io/npm/v/@solvohq/json-to-ts.svg)](https://www.npmjs.com/package/@solvohq/json-to-ts)
[![Live demo](https://img.shields.io/badge/demo-live-brightgreen.svg)](https://json-to-ts-app.netlify.app/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Zero runtime dependencies. Pure Node — no install needed if you `npx` it.

## Quick start

```bash
echo '{"id":1,"name":"Ada","tags":["admin"]}' | npx @solvohq/json-to-ts
```

```ts
interface Root {
  id: number;
  name: string;
  tags: string[];
}
```

Switch to Zod or Valibot with one flag:

```bash
echo '{"id":1,"name":"Ada"}' | npx @solvohq/json-to-ts --mode zod
echo '{"id":1,"name":"Ada"}' | npx @solvohq/json-to-ts --mode valibot
```

```ts
// --mode zod
import { z } from "zod";

const RootSchema = z.object({
  id: z.number(),
  name: z.string(),
});
```

```ts
// --mode valibot
import * as v from "valibot";

const RootSchema = v.object({
  id: v.number(),
  name: v.string(),
});
```

## Install

```bash
# one-shot
npx @solvohq/json-to-ts < sample.json

# global
npm i -g @solvohq/json-to-ts
json-to-ts < sample.json

# project dependency (use as a library)
npm i @solvohq/json-to-ts
```

## CLI

```
Usage: json-to-ts [options] [file]

Options:
  --mode <ts|zod|valibot>   Output target (default: ts)
  --root <Name>             Root type/schema name (default: Root)
  --type                    TS only: emit `type` aliases instead of `interface`
  -h, --help                Show this help
  -v, --version             Show version
```

Reads JSON from stdin (or `[file]`) and writes the generated source to stdout. Errors go to stderr; exit code is `1` for invalid JSON, `2` for bad flags.

## Library

```js
const { jsonToTs, jsonToZod, jsonToValibot } = require("@solvohq/json-to-ts");

jsonToTs({ id: 1 });                       // string of TS source
jsonToZod({ id: 1 }, { rootName: "User" });
jsonToValibot([1, 2, 3]);
```

Each function accepts a parsed JSON value (already `JSON.parse`'d — pass objects, not strings) and returns a string. Options:

- `rootName` — name of the top-level type / schema. Default: `Root`.
- `mode` — TypeScript only: `"interface"` (default) or `"type"`.

## Why this exists

Most JSON-to-types tools either run in your browser (can't pipe), require a config file (heavy for one-off use), or pin you to one validator (Zod *or* Valibot, never both). This package is the same code that powers the browser tool, repackaged so it fits into pre-commit hooks, Makefile targets, and `curl | json-to-ts` one-liners.

## Live tool

If you'd rather paste JSON into a textbox: **[json-to-ts-app.netlify.app](https://json-to-ts-app.netlify.app/)**. The browser version supports the same three output modes and runs entirely client-side — no upload, no signup.

## License

MIT — see [LICENSE](LICENSE).
