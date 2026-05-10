"use strict";

// JSON -> { TypeScript, Zod, Valibot } emitters.
// Ported verbatim from the live tool at https://json-to-ts-app.netlify.app/
// (code/index.html). Parity with the live tool is the contract.

var IDENT_RE = /^[a-zA-Z_$][a-zA-Z0-9_$]*$/;
var TS_RESERVED = {
  "break": 1, "case": 1, "catch": 1, "class": 1, "const": 1, "continue": 1, "debugger": 1,
  "default": 1, "delete": 1, "do": 1, "else": 1, "enum": 1, "export": 1, "extends": 1,
  "false": 1, "finally": 1, "for": 1, "function": 1, "if": 1, "import": 1, "in": 1,
  "instanceof": 1, "new": 1, "null": 1, "return": 1, "super": 1, "switch": 1, "this": 1,
  "throw": 1, "true": 1, "try": 1, "typeof": 1, "var": 1, "void": 1, "while": 1, "with": 1
};

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

function jsonToZod(value, opts) {
  opts = opts || {};
  var rootName = opts.rootName || "Root";

  var schemas = [];
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

  function primZod(v) {
    if (v === null) return "z.null()";
    var t = typeof v;
    if (t === "string") return "z.string()";
    if (t === "number") return "z.number()";
    if (t === "boolean") return "z.boolean()";
    return "z.unknown()";
  }

  function valuesToZod(values, hint) {
    var objects = [];
    var arrays = [];
    var primParts = [];
    var seen = Object.create(null);
    for (var i = 0; i < values.length; i++) {
      var v = values[i];
      if (Array.isArray(v)) {
        arrays.push(v);
      } else if (v !== null && typeof v === "object") {
        objects.push(v);
      } else {
        var p = primZod(v);
        if (!seen[p]) { seen[p] = 1; primParts.push(p); }
      }
    }
    var union = primParts.slice();
    if (arrays.length > 0) {
      var allElements = [];
      for (var j = 0; j < arrays.length; j++) {
        for (var k = 0; k < arrays[j].length; k++) allElements.push(arrays[j][k]);
      }
      union.push(arrayZod(allElements, hint));
    }
    if (objects.length > 0) {
      var merged = mergeObjectsZ(objects);
      union.push(generateZodObject(merged, hint));
    }
    if (union.length === 0) return "z.unknown()";
    if (union.length === 1) return union[0];
    return "z.union([" + union.join(", ") + "])";
  }

  function arrayZod(arr, hint) {
    if (arr.length === 0) return "z.array(z.unknown())";
    var childHint = singular(hint) || "Item";
    var element = valuesToZod(arr, childHint);
    return "z.array(" + element + ")";
  }

  function mergeObjectsZ(objects) {
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

  function generateZodObject(merged, hint) {
    var typeName;
    if (!namedRoot) {
      typeName = uniquify(rootName);
      namedRoot = true;
    } else {
      typeName = uniquify(pascal(hint) || "Type");
    }
    var schemaName = typeName + "Schema";

    var keys = Object.keys(merged);
    if (keys.length === 0) {
      schemas.push({ name: schemaName, body: "const " + schemaName + " = z.object({});\n" });
      return schemaName;
    }

    var lines = [];
    for (var i = 0; i < keys.length; i++) {
      var key = keys[i];
      var info = merged[key];
      var schemaStr = valuesToZod(info.values, key);
      var optional = info.optional ? ".optional()" : "";
      lines.push("  " + quoteKey(key) + ": " + schemaStr + optional + ",");
    }
    schemas.push({
      name: schemaName,
      body: "const " + schemaName + " = z.object({\n" + lines.join("\n") + "\n});\n"
    });
    return schemaName;
  }

  function objectToZod(obj, hint) {
    var keyOrder = Object.keys(obj);
    var merged = {};
    for (var i = 0; i < keyOrder.length; i++) {
      merged[keyOrder[i]] = { values: [obj[keyOrder[i]]], optional: false };
    }
    return generateZodObject(merged, hint);
  }

  var header = 'import { z } from "zod";\n\n';

  if (value === null || typeof value !== "object") {
    var rootSchema = uniquify(rootName) + "Schema";
    return header + "const " + rootSchema + " = " + primZod(value) + ";\n";
  }
  if (Array.isArray(value)) {
    var rootAlias = uniquify(rootName);
    namedRoot = true;
    var elementType = arrayZod(value, "Item");
    schemas.push({
      name: rootAlias + "Schema",
      body: "const " + rootAlias + "Schema = " + elementType + ";\n"
    });
    return header + schemas.map(function (s) { return s.body; }).join("\n");
  }
  objectToZod(value, rootName);
  return header + schemas.map(function (s) { return s.body; }).join("\n");
}

function jsonToValibot(value, opts) {
  opts = opts || {};
  var rootName = opts.rootName || "Root";

  var schemas = [];
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

  function primV(v) {
    if (v === null) return "v.null()";
    var t = typeof v;
    if (t === "string") return "v.string()";
    if (t === "number") return "v.number()";
    if (t === "boolean") return "v.boolean()";
    return "v.unknown()";
  }

  function valuesToV(values, hint) {
    var objects = [];
    var arrays = [];
    var primParts = [];
    var seen = Object.create(null);
    for (var i = 0; i < values.length; i++) {
      var v = values[i];
      if (Array.isArray(v)) {
        arrays.push(v);
      } else if (v !== null && typeof v === "object") {
        objects.push(v);
      } else {
        var p = primV(v);
        if (!seen[p]) { seen[p] = 1; primParts.push(p); }
      }
    }
    var union = primParts.slice();
    if (arrays.length > 0) {
      var allElements = [];
      for (var j = 0; j < arrays.length; j++) {
        for (var k = 0; k < arrays[j].length; k++) allElements.push(arrays[j][k]);
      }
      union.push(arrayV(allElements, hint));
    }
    if (objects.length > 0) {
      var merged = mergeObjectsV(objects);
      union.push(generateVObject(merged, hint));
    }
    if (union.length === 0) return "v.unknown()";
    if (union.length === 1) return union[0];
    return "v.union([" + union.join(", ") + "])";
  }

  function arrayV(arr, hint) {
    if (arr.length === 0) return "v.array(v.unknown())";
    var childHint = singular(hint) || "Item";
    var element = valuesToV(arr, childHint);
    return "v.array(" + element + ")";
  }

  function mergeObjectsV(objects) {
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

  function generateVObject(merged, hint) {
    var typeName;
    if (!namedRoot) {
      typeName = uniquify(rootName);
      namedRoot = true;
    } else {
      typeName = uniquify(pascal(hint) || "Type");
    }
    var schemaName = typeName + "Schema";

    var keys = Object.keys(merged);
    if (keys.length === 0) {
      schemas.push({ name: schemaName, body: "const " + schemaName + " = v.object({});\n" });
      return schemaName;
    }

    var lines = [];
    for (var i = 0; i < keys.length; i++) {
      var key = keys[i];
      var info = merged[key];
      var schemaStr = valuesToV(info.values, key);
      var wrapped = info.optional ? ("v.optional(" + schemaStr + ")") : schemaStr;
      lines.push("  " + quoteKey(key) + ": " + wrapped + ",");
    }
    schemas.push({
      name: schemaName,
      body: "const " + schemaName + " = v.object({\n" + lines.join("\n") + "\n});\n"
    });
    return schemaName;
  }

  function objectToV(obj, hint) {
    var keyOrder = Object.keys(obj);
    var merged = {};
    for (var i = 0; i < keyOrder.length; i++) {
      merged[keyOrder[i]] = { values: [obj[keyOrder[i]]], optional: false };
    }
    return generateVObject(merged, hint);
  }

  var header = 'import * as v from "valibot";\n\n';

  if (value === null || typeof value !== "object") {
    var rootSchema = uniquify(rootName) + "Schema";
    return header + "const " + rootSchema + " = " + primV(value) + ";\n";
  }
  if (Array.isArray(value)) {
    var rootAlias = uniquify(rootName);
    namedRoot = true;
    var elementType = arrayV(value, "Item");
    schemas.push({
      name: rootAlias + "Schema",
      body: "const " + rootAlias + "Schema = " + elementType + ";\n"
    });
    return header + schemas.map(function (s) { return s.body; }).join("\n");
  }
  objectToV(value, rootName);
  return header + schemas.map(function (s) { return s.body; }).join("\n");
}

module.exports = { jsonToTs: jsonToTs, jsonToZod: jsonToZod, jsonToValibot: jsonToValibot };
