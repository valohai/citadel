module.exports = {
  env: {
    browser: true,
    es2019: true,
  },
  extends: ["airbnb-base"],
  globals: {
    Atomics: "readonly",
    SharedArrayBuffer: "readonly",
  },
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: "module",
  },
  rules: {
    "arrow-parens": "off",
    "comma-dangle": "off",
    "no-alert": "off",
    "no-param-reassign": "off",
    "no-plusplus": "off",
    "object-curly-newline": "off",
    "operator-linebreak": "off",
    quotes: ["error", "double"],
  },
};
