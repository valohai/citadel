module.exports = {
  parser: "babel-eslint",
  env: {
    browser: true,
    es6: true
  },
  extends: ["airbnb-base"],
  globals: {
    Atomics: "readonly",
    SharedArrayBuffer: "readonly"
  },
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: "module"
  },
  rules: {
    "arrow-parens": "off",
    "comma-dangle": "off",
    "no-alert": "off",
    "no-param-reassign": "off",
    "no-plusplus": "off",
    "object-curly-newline": "off",
    "operator-linebreak": "off",
    "quotes": ["error", "double"]
  }
};
