// Renders github-readme-stats cards locally (no Vercel) and writes them to stats/.
// Usage: node scripts/render-stats.mjs <path-to-github-readme-stats checkout>
// Needs PAT_1 in the environment. Exits non-zero (and writes nothing) if any card errors,
// so a bad run never replaces the existing images.
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const grs = resolve(process.argv[2] ?? "grs");
const load = async (p) => (await import(pathToFileURL(`${grs}/${p}`).href)).default;
const { CACHE_TTL } = await import(pathToFileURL(`${grs}/src/common/cache.js`).href);

const cards = [
  {
    out: "stats/top-langs.svg",
    handler: await load("api/top-langs.js"),
    query: { username: "merlinlcb", langs_count: "10", hide_title: "true", hide_border: "true", layout: "compact", theme: "dracula" },
  },
  {
    out: "stats/stats.svg",
    handler: await load("api/index.js"),
    query: { username: "merlinlcb", hide_border: "true", hide_title: "true", show_icons: "true", theme: "dracula" },
  },
];

const results = [];
for (const card of cards) {
  const headers = {};
  let body = "";
  const res = {
    setHeader: (k, v) => { headers[k.toLowerCase()] = String(v); },
    send: (b) => { body = String(b); return body; },
  };
  await card.handler({ query: card.query }, res);
  const cc = headers["cache-control"] ?? "";
  // Success path sets a normal cache header; error paths set the short error TTL or none at all.
  const failed = !cc || cc.startsWith(`max-age=${CACHE_TTL.ERROR},`) || !body.startsWith("<svg") && !body.trim().startsWith("<svg");
  if (failed) {
    console.error(`FAILED ${card.out}:\n${body.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim().slice(0, 400)}`);
    process.exit(1);
  }
  results.push([card.out, body]);
}
mkdirSync("stats", { recursive: true });
for (const [out, body] of results) {
  writeFileSync(out, body);
  console.log(`wrote ${out} (${body.length} bytes)`);
}
