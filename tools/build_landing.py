#!/usr/bin/env python3
"""Generate long-tail SEO landing pages under code/<slug>/index.html.

Each page is self-contained: same converter as code/index.html, different
pre-loaded JSON sample, unique <title> / <meta description> / H1 / SEO body,
and a cross-link block to the other landing pages.
"""

from __future__ import annotations

import json
import pathlib
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
CODE_DIR = ROOT / "code"


# Order matters: it's the order shown in cross-links and in product/seo.md.
PAGES = [
    {
        "slug": "stripe-webhook-to-typescript",
        "title": "Stripe Webhook to TypeScript Types — checkout.session.completed → TS",
        "description": "Convert a Stripe webhook payload to TypeScript types instantly. Pre-loaded with a real checkout.session.completed event — paste your own to generate matching types.",
        "h1": "Stripe Webhook to TypeScript",
        "subhead": "Paste a Stripe webhook event (checkout.session.completed, payment_intent.succeeded, etc.) and get accurate TypeScript types in your browser. No signup, no upload.",
        "keyword": "Stripe webhook to TypeScript",
        "json_source": "Stripe Events API — checkout.session.completed (real event shape, redacted IDs)",
        "seo_paragraphs": [
            "Stripe webhook events all share the outer Event envelope (id, type, data.object, livemode, etc.) but the data.object payload changes per event type. Typing the outer envelope once is easy; the hard part is keeping data.object aligned with the dozens of inner shapes (Checkout Session, Payment Intent, Subscription, Invoice, etc.). Pasting a real event from your Stripe Dashboard's webhook log gives you a TypeScript interface that matches the exact event you received — including optional fields, nullable values, and metadata you actually use.",
            "Use these types in your webhook handler to narrow event.type === 'checkout.session.completed' and get full autocomplete for the inner Session fields. Paired with a runtime guard (or Stripe's own SDK), they catch shape drift before it reaches production. The official @stripe/stripe-node SDK ships its own types, but generated types from the live payload are useful when you only consume a subset of fields, want a stable shape across SDK versions, or need to share the type with a non-Node consumer.",
        ],
        "sample": {
            "id": "evt_1NQz5KJZ7p9KqYxRxMm8LgxF",
            "object": "event",
            "api_version": "2024-04-10",
            "created": 1715212800,
            "data": {
                "object": {
                    "id": "cs_test_a1B2c3D4e5F6g7H8i9J0kLmNoP",
                    "object": "checkout.session",
                    "amount_subtotal": 2000,
                    "amount_total": 2000,
                    "currency": "usd",
                    "customer": "cus_PqRsTuVwXyZ123",
                    "customer_email": "alice@example.com",
                    "mode": "payment",
                    "payment_intent": "pi_3QRsTuVwXy12345",
                    "payment_status": "paid",
                    "status": "complete",
                    "metadata": {"order_id": "ord_4567"},
                    "line_items": None,
                    "success_url": "https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
                    "cancel_url": "https://example.com/cancel",
                }
            },
            "livemode": False,
            "pending_webhooks": 0,
            "request": {"id": None, "idempotency_key": None},
            "type": "checkout.session.completed",
        },
    },
    {
        "slug": "github-api-to-typescript",
        "title": "GitHub API Response to TypeScript — /repos/{owner}/{repo} → TS interface",
        "description": "Convert any GitHub REST API response to TypeScript interfaces. Pre-loaded with a real /repos/{owner}/{repo} response — paste any GitHub JSON to generate matching types.",
        "h1": "GitHub API Response to TypeScript",
        "subhead": "Paste any GitHub REST API JSON response and get TypeScript interfaces instantly. Works for repos, issues, pull requests, users, releases, workflow runs — any /api.github.com/* endpoint.",
        "keyword": "GitHub API to TypeScript",
        "json_source": "GitHub REST API — GET /repos/{owner}/{repo} (octocat/Hello-World canonical example)",
        "seo_paragraphs": [
            "GitHub publishes an OpenAPI spec at github.com/github/rest-api-description, but it's huge, frequently lags behind the live API, and pulls in the full @octokit/types tree even when you only call a single endpoint. For one-off scripts, GitHub Actions, or internal dashboards that talk to a handful of endpoints, generating a TypeScript interface from a real JSON response is faster and produces a smaller, more readable surface area.",
            "Paste the JSON returned by any /api.github.com/ endpoint — repos, issues, pull requests, runs, releases, users — and the converter walks the shape, merges arrays of objects into a single interface, marks fields optional when they're missing in any sample, and produces nested types for embedded objects like owner, license, or head/base. Drop the result into your script and you get autocomplete on every field GitHub actually returned.",
        ],
        "sample": {
            "id": 1296269,
            "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
            "name": "Hello-World",
            "full_name": "octocat/Hello-World",
            "private": False,
            "owner": {
                "login": "octocat",
                "id": 1,
                "node_id": "MDQ6VXNlcjE=",
                "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                "gravatar_id": "",
                "type": "User",
                "site_admin": False,
            },
            "html_url": "https://github.com/octocat/Hello-World",
            "description": "This your first repo!",
            "fork": False,
            "created_at": "2011-01-26T19:01:12Z",
            "updated_at": "2011-01-26T19:14:43Z",
            "pushed_at": "2011-01-26T19:06:43Z",
            "homepage": "https://github.com",
            "size": 108,
            "stargazers_count": 80,
            "watchers_count": 9,
            "language": "C",
            "has_issues": True,
            "has_projects": True,
            "has_downloads": True,
            "has_wiki": True,
            "has_pages": False,
            "forks_count": 9,
            "mirror_url": None,
            "archived": False,
            "disabled": False,
            "open_issues_count": 0,
            "license": {
                "key": "mit",
                "name": "MIT License",
                "spdx_id": "MIT",
                "url": "https://api.github.com/licenses/mit",
                "node_id": "MDc6TGljZW5zZW1pdA==",
            },
            "topics": ["octocat", "atom", "electron", "api"],
            "default_branch": "master",
        },
    },
    {
        "slug": "openai-chat-completion-to-typescript",
        "title": "OpenAI Chat Completion to TypeScript — chat.completion response → TS",
        "description": "Convert an OpenAI Chat Completions response to TypeScript types instantly. Pre-loaded with a real gpt-4o response — paste your own to type your LLM client.",
        "h1": "OpenAI Chat Completion to TypeScript",
        "subhead": "Paste an OpenAI Chat Completions JSON response and get a TypeScript interface for choices, usage, message, tool_calls, and the rest. Works for any /v1/chat/completions response.",
        "keyword": "OpenAI chat completion to TypeScript",
        "json_source": "OpenAI Chat Completions API — gpt-4o response (canonical, single-choice, no tools)",
        "seo_paragraphs": [
            "The official openai npm package ships its own TypeScript types, but you'll still want a generated interface when you're calling the OpenAI-compatible endpoint of a different provider (Groq, Together, OpenRouter, local Ollama), proxying responses through your own backend, or persisting the response to a database where the schema needs to match exactly what came back over the wire. Generating types from a real response captures the actual shape, including provider-specific extensions OpenAI's official types don't know about.",
            "The shape includes id, object, created, model, choices[].message, choices[].finish_reason, and a usage block with prompt/completion/total tokens. Recent gpt-4o responses also include nested prompt_tokens_details and completion_tokens_details, plus an optional system_fingerprint. Paste your own response (with a tool_calls field, refusal, or logprobs filled in) and the converter merges everything into one accurate interface.",
        ],
        "sample": {
            "id": "chatcmpl-8hkRX9zYqAbCdEfGhIjKlMn",
            "object": "chat.completion",
            "created": 1715212800,
            "model": "gpt-4o-2024-08-06",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "TypeScript is a typed superset of JavaScript that compiles to plain JavaScript.",
                        "refusal": None,
                    },
                    "logprobs": None,
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 24,
                "completion_tokens": 18,
                "total_tokens": 42,
                "prompt_tokens_details": {"cached_tokens": 0},
                "completion_tokens_details": {
                    "reasoning_tokens": 0,
                    "accepted_prediction_tokens": 0,
                    "rejected_prediction_tokens": 0,
                },
            },
            "system_fingerprint": "fp_a1b2c3d4e5",
        },
    },
    {
        "slug": "json-api-to-typescript",
        "title": "JSON:API to TypeScript — single resource + included → TS interface",
        "description": "Convert a JSON:API (jsonapi.org) response to TypeScript interfaces. Pre-loaded with a real single-resource document including relationships and included — paste your own.",
        "h1": "JSON:API to TypeScript",
        "subhead": "Paste any JSON:API document — single resource, collection, or compound document with included — and get TypeScript interfaces for data, attributes, relationships, and links.",
        "keyword": "JSON:API to TypeScript",
        "json_source": "JSON:API v1.1 (jsonapi.org) — single resource with relationships + included",
        "seo_paragraphs": [
            "JSON:API (jsonapi.org) imposes a strict envelope: every resource has a type, an id, an attributes bag, an optional relationships bag, and optional links. Compound documents add a top-level included array carrying related resources. Hand-typing this in TypeScript is tedious, especially when the attributes shape varies by resource type. Pasting a real document — pulled from your API or from your fixture file — generates accurate interfaces in one paste.",
            "The result lets you narrow on data.type, type-safely access attributes, and walk relationships into the included array. For applications consuming Ember Data, JSON:API-compliant Rails APIs, or Laravel JSON:API, this is the fastest way to bootstrap a typed client without committing to a heavyweight code-generation pipeline.",
        ],
        "sample": {
            "data": {
                "type": "articles",
                "id": "1",
                "attributes": {
                    "title": "JSON:API paints my bikeshed!",
                    "body": "The shortest article. Ever.",
                    "created": "2026-01-15T22:14:24Z",
                    "updated": "2026-01-15T22:14:24Z",
                },
                "relationships": {
                    "author": {"data": {"type": "people", "id": "42"}},
                    "comments": {
                        "data": [
                            {"type": "comments", "id": "5"},
                            {"type": "comments", "id": "12"},
                        ]
                    },
                },
                "links": {"self": "https://example.com/articles/1"},
            },
            "included": [
                {
                    "type": "people",
                    "id": "42",
                    "attributes": {
                        "name": "John",
                        "email": "john@example.com",
                    },
                    "links": {"self": "https://example.com/people/42"},
                }
            ],
            "links": {"self": "https://example.com/articles/1"},
            "jsonapi": {"version": "1.1"},
        },
    },
    {
        "slug": "aws-lambda-event-to-typescript",
        "title": "AWS Lambda Event to TypeScript — API Gateway HTTP API v2 → TS",
        "description": "Convert an AWS Lambda event payload to TypeScript types. Pre-loaded with a real API Gateway HTTP API v2 event — paste your own (S3, SQS, EventBridge) for matching types.",
        "h1": "AWS Lambda Event to TypeScript",
        "subhead": "Paste any AWS Lambda event payload — API Gateway, SQS, S3, EventBridge, DynamoDB Streams — and get a TypeScript interface for your handler signature.",
        "keyword": "AWS Lambda event to TypeScript",
        "json_source": "AWS API Gateway HTTP API v2 → Lambda integration (real event shape from CloudWatch)",
        "seo_paragraphs": [
            "Lambda event shapes change per integration: API Gateway REST (v1) is different from HTTP API (v2), SQS batches arrays of records, S3 sends nested s3 + object descriptors, EventBridge wraps everything in detail-type / detail. The @types/aws-lambda package covers most of these but pulls in a large surface area you don't need. Generating a type from one real event payload — copied straight out of CloudWatch Logs — gives you a tight interface for that exact handler.",
            "Paste an event your function actually received and the converter walks every nested level (requestContext, http, headers, queryStringParameters, multiValueHeaders, etc.). The resulting interface is what you put in your handler signature — and because it's generated from a real payload, fields you don't get (like multiValueHeaders on HTTP API v2) won't appear in the type, eliminating dead branches.",
        ],
        "sample": {
            "version": "2.0",
            "routeKey": "POST /items",
            "rawPath": "/items",
            "rawQueryString": "limit=10",
            "headers": {
                "accept": "application/json",
                "content-length": "85",
                "content-type": "application/json",
                "host": "api.example.com",
                "user-agent": "curl/7.68.0",
                "x-amzn-trace-id": "Root=1-654321ab-1234567890abcdef",
            },
            "queryStringParameters": {"limit": "10"},
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "abc1234",
                "domainName": "api.example.com",
                "domainPrefix": "api",
                "http": {
                    "method": "POST",
                    "path": "/items",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "192.0.2.1",
                    "userAgent": "curl/7.68.0",
                },
                "requestId": "Z9Sw8jBDoAMEPOA=",
                "routeKey": "POST /items",
                "stage": "$default",
                "time": "10/May/2026:04:30:00 +0000",
                "timeEpoch": 1715315400,
            },
            "body": '{"name":"widget","qty":3}',
            "isBase64Encoded": False,
        },
    },
]


PAGE_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>__TITLE__</title>
<meta name="description" content="__DESCRIPTION__" />
<link rel="canonical" href="https://json-to-ts-app.netlify.app/__SLUG__/" />
<meta name="theme-color" content="#0b1020" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="JSON to TypeScript" />
<meta property="og:title" content="__TITLE__" />
<meta property="og:description" content="__DESCRIPTION__" />
<meta property="og:url" content="https://json-to-ts-app.netlify.app/__SLUG__/" />
<meta property="og:image" content="https://json-to-ts-app.netlify.app/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="JSON to TypeScript — two-pane converter showing JSON on the left and generated TS interfaces on the right" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="__TITLE__" />
<meta name="twitter:description" content="__DESCRIPTION__" />
<meta name="twitter:image" content="https://json-to-ts-app.netlify.app/og-image.png" />
<link rel="icon" href="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='12' fill='%230b1020'/><text x='32' y='42' text-anchor='middle' font-family='monospace' font-size='28' fill='%2378dce8' font-weight='700'>{ }</text></svg>" />
<style>
  :root {
    --bg: #0b1020;
    --panel: #11172b;
    --panel-2: #0e1424;
    --border: #1e2740;
    --text: #e6ecff;
    --text-dim: #8a93b8;
    --accent: #78dce8;
    --accent-2: #c792ea;
    --good: #a6e3a1;
    --bad: #f38ba8;
    --mono: ui-monospace, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; }
  body {
    background: var(--bg);
    color: var(--text);
    font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  header.nav {
    padding: 10px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 14px;
    flex-wrap: wrap;
  }
  header.nav .brand a {
    color: var(--text);
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
  }
  header.nav .brand a .accent { color: var(--accent); }
  header.nav .brand a .arrow { color: var(--text-dim); margin: 0 4px; }
  header.nav .brand a .accent-2 { color: var(--accent-2); }
  header.nav .brand a:hover .accent,
  header.nav .brand a:hover .accent-2 { text-decoration: underline; }
  header.nav .breadcrumb {
    color: var(--text-dim);
    font-size: 12px;
  }
  header.nav .controls {
    margin-left: auto;
    display: flex;
    gap: 8px;
    align-items: center;
  }
  .seg {
    display: inline-flex;
    background: var(--panel-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
  }
  .seg button {
    background: transparent;
    color: var(--text-dim);
    border: 0;
    padding: 6px 12px;
    font: inherit;
    cursor: pointer;
    font-family: var(--mono);
    font-size: 12px;
  }
  .seg button.active {
    background: var(--accent);
    color: #06202a;
    font-weight: 600;
  }
  .icon-btn {
    background: var(--panel-2);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 10px;
    font: inherit;
    font-size: 12px;
    cursor: pointer;
  }
  .icon-btn:hover { border-color: var(--accent); }
  section.hero {
    padding: 24px 20px 12px;
    max-width: 960px;
    margin: 0 auto;
    width: 100%;
  }
  section.hero h1 {
    margin: 0 0 8px 0;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.2px;
  }
  section.hero p.subhead {
    margin: 0;
    color: var(--text-dim);
    font-size: 15px;
    line-height: 1.55;
    max-width: 720px;
  }
  main {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: var(--border);
    min-height: 480px;
    margin-top: 16px;
  }
  .pane {
    background: var(--panel);
    display: flex;
    flex-direction: column;
    min-height: 0;
  }
  .pane-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 14px;
    border-bottom: 1px solid var(--border);
    color: var(--text-dim);
    font-family: var(--mono);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .pane-head .status { font-weight: 500; }
  .pane-head .status.ok { color: var(--good); }
  .pane-head .status.err { color: var(--bad); }
  .pane-body {
    flex: 1;
    min-height: 480px;
    position: relative;
  }
  textarea, pre {
    margin: 0;
    width: 100%;
    height: 100%;
    background: var(--panel);
    color: var(--text);
    border: 0;
    padding: 14px 16px;
    font-family: var(--mono);
    font-size: 13px;
    line-height: 1.55;
    resize: none;
    outline: none;
    overflow: auto;
    white-space: pre;
    tab-size: 2;
  }
  pre { color: var(--text); }
  .copy-floating {
    position: absolute;
    top: 10px;
    right: 14px;
    background: var(--panel-2);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 5px 10px;
    font: inherit;
    font-size: 12px;
    cursor: pointer;
    opacity: 0.85;
  }
  .copy-floating:hover { border-color: var(--accent); opacity: 1; }
  .copy-floating.copied { color: var(--good); border-color: var(--good); }
  .tk-kw { color: var(--accent-2); }
  .tk-type { color: var(--accent); }
  .tk-prim { color: #e0a458; }
  .tk-str { color: var(--good); }
  .tk-punc { color: var(--text-dim); }
  .tk-name { color: var(--text); }
  section.seo {
    padding: 28px 20px;
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
  }
  section.seo h2 {
    margin: 0 0 12px 0;
    font-size: 18px;
    font-weight: 600;
    color: var(--text);
  }
  section.seo p {
    color: var(--text-dim);
    line-height: 1.7;
    font-size: 14px;
    margin: 0 0 14px 0;
  }
  section.cross {
    padding: 8px 20px 28px;
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
  }
  section.cross h2 {
    margin: 0 0 10px 0;
    font-size: 16px;
    font-weight: 600;
    color: var(--text);
  }
  section.cross ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 8px;
  }
  section.cross li a {
    display: block;
    padding: 10px 12px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text);
    text-decoration: none;
    font-size: 13px;
  }
  section.cross li a:hover { border-color: var(--accent); }
  section.cross li a .dim { color: var(--text-dim); font-size: 11px; display: block; margin-top: 2px; }
  footer {
    padding: 8px 20px;
    border-top: 1px solid var(--border);
    color: var(--text-dim);
    font-size: 12px;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
  }
  footer a { color: var(--accent); text-decoration: none; }
  footer a:hover { text-decoration: underline; }
  @media (max-width: 720px) {
    main { grid-template-columns: 1fr; grid-template-rows: 1fr 1fr; }
    section.hero h1 { font-size: 22px; }
  }
</style>
</head>
<body>
<header class="nav">
  <div class="brand"><a href="/"><span class="accent">JSON</span><span class="arrow">→</span><span class="accent-2">TypeScript</span></a></div>
  <span class="breadcrumb">/__SLUG__</span>
  <div class="controls">
    <div class="seg" role="tablist" aria-label="Output style">
      <button id="mode-interface" class="active" type="button">interface</button>
      <button id="mode-type" type="button">type</button>
    </div>
    <button id="sample" class="icon-btn" type="button" title="Reload the example">reload sample</button>
  </div>
</header>
<section class="hero">
  <h1>__H1__</h1>
  <p class="subhead">__SUBHEAD__</p>
</section>
<main>
  <section class="pane">
    <div class="pane-head">
      <span>JSON input</span>
      <span id="status" class="status ok">valid</span>
    </div>
    <div class="pane-body">
      <textarea id="input" spellcheck="false" autocomplete="off" autocapitalize="off" autocorrect="off"></textarea>
    </div>
  </section>
  <section class="pane">
    <div class="pane-head">
      <span>TypeScript output</span>
    </div>
    <div class="pane-body">
      <pre id="output" aria-live="polite"></pre>
      <button id="copy" class="copy-floating" type="button">copy</button>
    </div>
  </section>
</main>
<section class="seo">
  <h2>About this conversion</h2>
__SEO_PARAGRAPHS__
</section>
<section class="cross">
  <h2>Other JSON shapes</h2>
  <ul>
__CROSS_LINKS__
  </ul>
</section>
<footer>
  <span>Runs entirely in your browser. Nothing is uploaded.</span>
  <span><a href="/">← back to the generic JSON-to-TypeScript tool</a></span>
</footer>
<script data-goatcounter="https://jsontots.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<script>
(function () {
  "use strict";

  function pascal(s) {
    if (!s) return "";
    return String(s)
      .replace(/[^a-zA-Z0-9]+(.)?/g, function (_, c) { return c ? c.toUpperCase() : ""; })
      .replace(/^([a-z])/, function (m) { return m.toUpperCase(); })
      .replace(/^([0-9])/, "_$1");
  }
  function singular(s) {
    if (!s) return s;
    if (/ies$/.test(s) && s.length > 3) return s.slice(0, -3) + "y";
    if (/sses$/.test(s)) return s.slice(0, -2);
    if (/s$/.test(s) && !/ss$/.test(s) && s.length > 1) return s.slice(0, -1);
    return s;
  }
  var IDENT_RE = /^[a-zA-Z_$][a-zA-Z0-9_$]*$/;
  var TS_RESERVED = {
    "break":1,"case":1,"catch":1,"class":1,"const":1,"continue":1,"debugger":1,
    "default":1,"delete":1,"do":1,"else":1,"enum":1,"export":1,"extends":1,
    "false":1,"finally":1,"for":1,"function":1,"if":1,"import":1,"in":1,
    "instanceof":1,"new":1,"null":1,"return":1,"super":1,"switch":1,"this":1,
    "throw":1,"true":1,"try":1,"typeof":1,"var":1,"void":1,"while":1,"with":1
  };
  function quoteKey(k) {
    return IDENT_RE.test(k) ? k : JSON.stringify(k);
  }

  function jsonToTs(value, opts) {
    opts = opts || {};
    var mode = opts.mode === "type" ? "type" : "interface";
    var rootName = opts.rootName || "Root";
    var types = [];
    var nameSet = Object.create(null);
    var namedRoot = false;

    function uniquify(name) {
      if (!name || !IDENT_RE.test(name) || TS_RESERVED[name.toLowerCase()]) {
        name = "T_" + (name || "Anon").replace(/[^a-zA-Z0-9_$]/g, "");
      }
      if (!nameSet[name]) { nameSet[name] = 1; return name; }
      var i = 2;
      while (nameSet[name + i]) i++;
      nameSet[name + i] = 1;
      return name + i;
    }

    function valuesToType(values, hint) {
      var objects = [];
      var arrays = [];
      var primTypes = [];
      var seen = Object.create(null);
      for (var i = 0; i < values.length; i++) {
        var v = values[i];
        if (v === null) {
          if (!seen["null"]) { seen["null"] = 1; primTypes.push("null"); }
        } else if (Array.isArray(v)) {
          arrays.push(v);
        } else if (typeof v === "object") {
          objects.push(v);
        } else {
          var t = typeof v;
          if (t !== "string" && t !== "number" && t !== "boolean") t = "unknown";
          if (!seen[t]) { seen[t] = 1; primTypes.push(t); }
        }
      }
      var unionTypes = primTypes.slice();
      if (arrays.length > 0) {
        var allElements = [];
        for (var j = 0; j < arrays.length; j++) {
          for (var k = 0; k < arrays[j].length; k++) allElements.push(arrays[j][k]);
        }
        unionTypes.push(arrayType(allElements, hint));
      }
      if (objects.length > 0) {
        var merged = mergeObjects(objects);
        unionTypes.push(generateInterface(merged, hint));
      }
      if (unionTypes.length === 0) return "unknown";
      return unionTypes.join(" | ");
    }

    function arrayType(arr, hint) {
      if (arr.length === 0) return "unknown[]";
      var childHint = singular(hint) || "Item";
      var element = valuesToType(arr, childHint);
      if (element.indexOf(" | ") !== -1) return "(" + element + ")[]";
      return element + "[]";
    }

    function mergeObjects(objects) {
      var keys = Object.create(null);
      var keyOrder = [];
      for (var i = 0; i < objects.length; i++) {
        for (var k in objects[i]) {
          if (Object.prototype.hasOwnProperty.call(objects[i], k)) {
            if (!keys[k]) { keys[k] = { values: [], optional: false }; keyOrder.push(k); }
          }
        }
      }
      for (i = 0; i < objects.length; i++) {
        for (var j = 0; j < keyOrder.length; j++) {
          var key = keyOrder[j];
          if (Object.prototype.hasOwnProperty.call(objects[i], key)) {
            keys[key].values.push(objects[i][key]);
          } else {
            keys[key].optional = true;
          }
        }
      }
      var ordered = {};
      for (i = 0; i < keyOrder.length; i++) ordered[keyOrder[i]] = keys[keyOrder[i]];
      return ordered;
    }

    function objectType(obj, hint) {
      var keyOrder = Object.keys(obj);
      var merged = {};
      for (var i = 0; i < keyOrder.length; i++) {
        merged[keyOrder[i]] = { values: [obj[keyOrder[i]]], optional: false };
      }
      return generateInterface(merged, hint);
    }

    function generateInterface(merged, hint) {
      var typeName;
      if (!namedRoot) {
        typeName = uniquify(rootName);
        namedRoot = true;
      } else {
        typeName = uniquify(pascal(hint) || "Type");
      }
      var slot = { name: typeName, body: null };
      types.push(slot);
      var keys = Object.keys(merged);
      var lines = [];
      if (keys.length === 0) {
        slot.body = mode === "interface"
          ? "interface " + typeName + " {}\n"
          : "type " + typeName + " = {};\n";
        return typeName;
      }
      for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        var info = merged[key];
        var typeStr = valuesToType(info.values, key);
        var optional = info.optional ? "?" : "";
        lines.push("  " + quoteKey(key) + optional + ": " + typeStr + ";");
      }
      var body;
      if (mode === "interface") {
        body = "interface " + typeName + " {\n" + lines.join("\n") + "\n}\n";
      } else {
        body = "type " + typeName + " = {\n" + lines.join("\n") + "\n};\n";
      }
      slot.body = body;
      return typeName;
    }

    if (value === null || typeof value !== "object") {
      var prim = value === null ? "null" : typeof value;
      if (prim !== "string" && prim !== "number" && prim !== "boolean" && prim !== "null") prim = "unknown";
      return "type " + uniquify(rootName) + " = " + prim + ";\n";
    }
    if (Array.isArray(value)) {
      var rootAliasName = uniquify(rootName);
      namedRoot = true;
      var elementType = arrayType(value, "Item");
      types.unshift({ name: rootAliasName, body: "type " + rootAliasName + " = " + elementType + ";\n" });
      return types.map(function (s) { return s.body; }).join("\n");
    }
    objectType(value, rootName);
    return types.map(function (s) { return s.body; }).join("\n");
  }

  function escapeHtml(s) {
    return s.replace(/[&<>]/g, function (c) {
      return c === "&" ? "&amp;" : c === "<" ? "&lt;" : "&gt;";
    });
  }
  var KW = ["interface","type","extends"];
  var PRIMS = ["string","number","boolean","null","undefined","unknown","any","never","void","object"];
  function highlight(src) {
    var out = "";
    var i = 0;
    while (i < src.length) {
      var ch = src[i];
      if (ch === '"') {
        var j = i + 1;
        while (j < src.length && src[j] !== '"') {
          if (src[j] === "\\" && j + 1 < src.length) j += 2;
          else j++;
        }
        j = Math.min(j + 1, src.length);
        out += '<span class="tk-str">' + escapeHtml(src.slice(i, j)) + "</span>";
        i = j;
        continue;
      }
      if (/[a-zA-Z_$]/.test(ch)) {
        var k = i;
        while (k < src.length && /[a-zA-Z0-9_$]/.test(src[k])) k++;
        var word = src.slice(i, k);
        var cls = "tk-name";
        if (KW.indexOf(word) !== -1) cls = "tk-kw";
        else if (PRIMS.indexOf(word) !== -1) cls = "tk-prim";
        else if (/^[A-Z]/.test(word)) cls = "tk-type";
        out += '<span class="' + cls + '">' + escapeHtml(word) + "</span>";
        i = k;
        continue;
      }
      if (/[{};:,?|()\[\]=]/.test(ch)) {
        out += '<span class="tk-punc">' + escapeHtml(ch) + "</span>";
        i++;
        continue;
      }
      out += escapeHtml(ch);
      i++;
    }
    return out;
  }

  var $input = document.getElementById("input");
  var $output = document.getElementById("output");
  var $status = document.getElementById("status");
  var $copy = document.getElementById("copy");
  var $sample = document.getElementById("sample");
  var $modeInterface = document.getElementById("mode-interface");
  var $modeType = document.getElementById("mode-type");

  var SAMPLE = __SAMPLE_JSON__;
  var ROOT_NAME = "__ROOT_NAME__";
  var mode = "interface";

  function setMode(next) {
    mode = next;
    $modeInterface.classList.toggle("active", mode === "interface");
    $modeType.classList.toggle("active", mode === "type");
    render();
  }

  function render() {
    var src = $input.value;
    if (!src.trim()) {
      $output.innerHTML = "";
      $status.textContent = "empty";
      $status.className = "status";
      return;
    }
    var parsed;
    try {
      parsed = JSON.parse(src);
    } catch (e) {
      $status.textContent = "invalid: " + (e.message || "parse error");
      $status.className = "status err";
      return;
    }
    $status.textContent = "valid";
    $status.className = "status ok";
    var ts;
    try {
      ts = jsonToTs(parsed, { mode: mode, rootName: ROOT_NAME });
    } catch (e) {
      $status.textContent = "convert error: " + (e.message || e);
      $status.className = "status err";
      return;
    }
    $output.innerHTML = highlight(ts);
    $output.dataset.raw = ts;
  }

  function loadSample() {
    $input.value = SAMPLE;
    render();
  }

  $input.addEventListener("input", render);
  $modeInterface.addEventListener("click", function () { setMode("interface"); });
  $modeType.addEventListener("click", function () { setMode("type"); });
  $sample.addEventListener("click", loadSample);

  $copy.addEventListener("click", function () {
    var text = $output.dataset.raw || $output.textContent || "";
    if (!text) return;
    if (window.goatcounter && typeof window.goatcounter.count === "function") {
      try { window.goatcounter.count({ path: "copy", title: "Copy button clicked", event: true }); } catch (e) {}
    }
    var done = function () {
      $copy.textContent = "copied";
      $copy.classList.add("copied");
      setTimeout(function () {
        $copy.textContent = "copy";
        $copy.classList.remove("copied");
      }, 1200);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text); done(); });
    } else {
      fallbackCopy(text);
      done();
    }
  });

  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
  }

  loadSample();
})();
</script>
</body>
</html>
"""


def root_name_from_slug(slug: str) -> str:
    # e.g. "stripe-webhook-to-typescript" -> "StripeWebhookEvent"-ish
    base = slug.replace("-to-typescript", "")
    parts = [p for p in base.split("-") if p]
    return "".join(p[:1].upper() + p[1:] for p in parts) or "Root"


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_cross_links(current_slug: str) -> str:
    out_lines = []
    for p in PAGES:
        if p["slug"] == current_slug:
            continue
        out_lines.append(
            f'    <li><a href="/{p["slug"]}/">{html_escape(p["h1"])}<span class="dim">{html_escape(p["keyword"])}</span></a></li>'
        )
    return "\n".join(out_lines)


def build_seo_paragraphs(paragraphs: list[str]) -> str:
    return "\n".join(f"  <p>{html_escape(p)}</p>" for p in paragraphs)


def build_page(page: dict) -> str:
    sample_json_literal = json.dumps(json.dumps(page["sample"], indent=2))
    root_name = root_name_from_slug(page["slug"])
    html = PAGE_TEMPLATE
    html = html.replace("__TITLE__", html_escape(page["title"]))
    html = html.replace("__DESCRIPTION__", html_escape(page["description"]))
    html = html.replace("__SLUG__", page["slug"])
    html = html.replace("__H1__", html_escape(page["h1"]))
    html = html.replace("__SUBHEAD__", html_escape(page["subhead"]))
    html = html.replace("__SEO_PARAGRAPHS__", build_seo_paragraphs(page["seo_paragraphs"]))
    html = html.replace("__CROSS_LINKS__", build_cross_links(page["slug"]))
    html = html.replace("__SAMPLE_JSON__", sample_json_literal)
    html = html.replace("__ROOT_NAME__", root_name)
    return html


SITEMAP_HEADER = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
SITEMAP_FOOTER = "</urlset>\n"


def build_sitemap(today: str) -> str:
    out = [SITEMAP_HEADER]
    out.append(
        f"  <url>\n    <loc>https://json-to-ts-app.netlify.app/</loc>\n"
        f"    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n"
        f"    <priority>1.0</priority>\n  </url>\n"
    )
    for p in PAGES:
        out.append(
            f"  <url>\n    <loc>https://json-to-ts-app.netlify.app/{p['slug']}/</loc>\n"
            f"    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n"
            f"    <priority>0.8</priority>\n  </url>\n"
        )
    out.append(SITEMAP_FOOTER)
    return "".join(out)


def main() -> None:
    import datetime as _dt

    today = _dt.date.today().isoformat()
    for page in PAGES:
        out_dir = CODE_DIR / page["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "index.html"
        out_path.write_text(build_page(page))
        print(f"wrote {out_path.relative_to(ROOT)} ({out_path.stat().st_size} bytes)")

    sitemap_path = CODE_DIR / "sitemap.xml"
    sitemap_path.write_text(build_sitemap(today))
    print(f"wrote {sitemap_path.relative_to(ROOT)} ({sitemap_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
