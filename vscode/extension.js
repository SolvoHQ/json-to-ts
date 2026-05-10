"use strict";

const vscode = require("vscode");
const https = require("https");
const http = require("http");
const url = require("url");

const MODE_PICKS = [
  { label: "ts", description: "TypeScript interface" },
  { label: "zod", description: "Zod schema (z.object, z.array, ...)" },
  { label: "valibot", description: "Valibot schema (v.object, v.array, ...)" }
];

function getConfig() {
  const cfg = vscode.workspace.getConfiguration("jsonToTs");
  return {
    apiUrl: cfg.get("apiUrl") || "https://json-to-ts-app.netlify.app/api/convert",
    rootName: cfg.get("rootName") || "Root"
  };
}

function postJson(endpoint, payload) {
  return new Promise(function (resolve, reject) {
    let parsed;
    try { parsed = url.parse(endpoint); } catch (e) { return reject(e); }
    const lib = parsed.protocol === "http:" ? http : https;
    const body = JSON.stringify(payload);
    const req = lib.request({
      method: "POST",
      protocol: parsed.protocol,
      hostname: parsed.hostname,
      port: parsed.port,
      path: parsed.path,
      headers: {
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(body),
        "User-Agent": "json-to-ts-vscode/0.1.0"
      }
    }, function (res) {
      const chunks = [];
      res.on("data", function (c) { chunks.push(c); });
      res.on("end", function () {
        const text = Buffer.concat(chunks).toString("utf8");
        let json = null;
        try { json = JSON.parse(text); } catch (e) { /* keep null */ }
        resolve({ status: res.statusCode || 0, body: json, raw: text });
      });
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

function languageIdFor(mode) {
  // All three outputs are valid TypeScript source. Open as `typescript` so
  // VS Code highlights z.object / v.object / interface uniformly.
  return "typescript";
}

async function pickMode() {
  const pick = await vscode.window.showQuickPick(MODE_PICKS, {
    placeHolder: "Output mode",
    title: "JSON to TS — choose target"
  });
  return pick ? pick.label : null;
}

async function readSelectionOrDocument() {
  const ed = vscode.window.activeTextEditor;
  if (!ed) {
    vscode.window.showWarningMessage("JSON to TS: no active editor. Open a JSON file or use 'Convert Clipboard'.");
    return null;
  }
  const sel = ed.selection;
  if (sel && !sel.isEmpty) {
    return ed.document.getText(sel);
  }
  return ed.document.getText();
}

async function readClipboard() {
  return await vscode.env.clipboard.readText();
}

async function convert(source, modeOverride) {
  if (!source || !source.trim()) {
    vscode.window.showWarningMessage("JSON to TS: input is empty.");
    return;
  }
  const mode = modeOverride || (await pickMode());
  if (!mode) return; // user cancelled

  const cfg = getConfig();

  await vscode.window.withProgress({
    location: vscode.ProgressLocation.Notification,
    title: "JSON to TS: converting (" + mode + ")…",
    cancellable: false
  }, async function () {
    let res;
    try {
      res = await postJson(cfg.apiUrl, {
        json: source,
        mode: mode,
        root: cfg.rootName
      });
    } catch (e) {
      vscode.window.showErrorMessage("JSON to TS: network error — " + (e && e.message ? e.message : String(e)));
      return;
    }
    if (res.status !== 200 || !res.body || typeof res.body.output !== "string") {
      const msg = res.body && res.body.error ? res.body.error : ("HTTP " + res.status);
      vscode.window.showErrorMessage("JSON to TS: " + msg);
      return;
    }
    const doc = await vscode.workspace.openTextDocument({
      content: res.body.output,
      language: languageIdFor(mode)
    });
    await vscode.window.showTextDocument(doc, { preview: false });
  });
}

async function convertSelection() {
  const source = await readSelectionOrDocument();
  if (source === null) return;
  await convert(source);
}

async function convertClipboard() {
  const source = await readClipboard();
  if (!source || !source.trim()) {
    vscode.window.showWarningMessage("JSON to TS: clipboard is empty.");
    return;
  }
  await convert(source);
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand("json-to-ts.convertSelection", convertSelection),
    vscode.commands.registerCommand("json-to-ts.convertClipboard", convertClipboard)
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
