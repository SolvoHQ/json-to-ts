#!/usr/bin/env node
"use strict";

var emitters = require("./index.js");

var HELP = [
  "Usage: json-to-ts [options] [file]",
  "",
  "  Read JSON from stdin (or [file]) and emit TypeScript / Zod / Valibot.",
  "  Mirrors https://json-to-ts-app.netlify.app/ — same emitter algorithms.",
  "",
  "Options:",
  "  --mode <ts|zod|valibot>   Output target (default: ts)",
  "  --root <Name>             Root type/schema name (default: Root)",
  "  --type                    TS only: emit `type` aliases instead of `interface`",
  "  -h, --help                Show this help",
  "  -v, --version             Show version",
  "",
  "Examples:",
  "  echo '{\"a\":1}' | npx @solvohq/json-to-ts",
  "  echo '{\"a\":1}' | npx @solvohq/json-to-ts --mode zod",
  "  npx @solvohq/json-to-ts --mode valibot --root User user.json",
  ""
].join("\n");

function parseArgs(argv) {
  var opts = { mode: "ts", rootName: "Root", typeMode: "interface", file: null };
  var i = 0;
  while (i < argv.length) {
    var a = argv[i];
    if (a === "-h" || a === "--help") { opts.help = true; i++; continue; }
    if (a === "-v" || a === "--version") { opts.version = true; i++; continue; }
    if (a === "--mode") { opts.mode = argv[++i]; i++; continue; }
    if (a === "--root") { opts.rootName = argv[++i]; i++; continue; }
    if (a === "--type") { opts.typeMode = "type"; i++; continue; }
    if (a.indexOf("--mode=") === 0) { opts.mode = a.slice(7); i++; continue; }
    if (a.indexOf("--root=") === 0) { opts.rootName = a.slice(7); i++; continue; }
    if (a[0] === "-") { return { error: "unknown option: " + a }; }
    if (opts.file === null) { opts.file = a; i++; continue; }
    return { error: "unexpected argument: " + a };
  }
  return opts;
}

function readStdin() {
  return new Promise(function (resolve, reject) {
    var chunks = [];
    process.stdin.on("data", function (c) { chunks.push(c); });
    process.stdin.on("end", function () { resolve(Buffer.concat(chunks).toString("utf8")); });
    process.stdin.on("error", reject);
  });
}

function readSource(file) {
  if (file) {
    var fs = require("fs");
    return Promise.resolve(fs.readFileSync(file, "utf8"));
  }
  if (process.stdin.isTTY) {
    return Promise.reject(new Error("no input on stdin and no file argument — try `--help`"));
  }
  return readStdin();
}

function emit(opts, src) {
  var trimmed = src.replace(/^﻿/, "").trim();
  if (!trimmed) throw new Error("input is empty");
  var parsed;
  try { parsed = JSON.parse(trimmed); }
  catch (e) { throw new Error("invalid JSON: " + e.message); }

  if (opts.mode === "ts") {
    return emitters.jsonToTs(parsed, { mode: opts.typeMode, rootName: opts.rootName });
  }
  if (opts.mode === "zod") {
    return emitters.jsonToZod(parsed, { rootName: opts.rootName });
  }
  if (opts.mode === "valibot") {
    return emitters.jsonToValibot(parsed, { rootName: opts.rootName });
  }
  throw new Error("unknown --mode: " + opts.mode + " (expected ts|zod|valibot)");
}

function main() {
  var opts = parseArgs(process.argv.slice(2));
  if (opts.error) {
    process.stderr.write("json-to-ts: " + opts.error + "\n\n" + HELP);
    process.exit(2);
  }
  if (opts.help) { process.stdout.write(HELP); return; }
  if (opts.version) {
    var pkg = require("./package.json");
    process.stdout.write(pkg.version + "\n");
    return;
  }
  readSource(opts.file).then(function (src) {
    var out = emit(opts, src);
    process.stdout.write(out);
  }).catch(function (err) {
    process.stderr.write("json-to-ts: " + err.message + "\n");
    process.exit(1);
  });
}

main();
