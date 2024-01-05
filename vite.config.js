import path from "node:path";

const outDir = path.resolve(path.join(__dirname, "cifront/static/editor"));

/** @type {import('vite').UserConfig} */
export default {
  root: "./code-in-the-dim",
  base: "/static/editor",
  build: {
    outDir,
  },
};
