const path = require("path");

module.exports = {
  entry: "./cifront/app/scripts/app.js",
  output: {
    path: path.resolve("./cifront/static/editor"),
    filename: "bundle.js"
  },
  resolve: {
    alias: {
      assets: path.resolve("./cifront/app/assets")
    }
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use: ["babel-loader"]
      },
      {
        test: /\.scss$/,
        use: ["style-loader", "css-loader", "postcss-loader", "sass-loader"]
      },
      { test: /\.png/, use: ["url-loader?mimetype=image/png"] },
      { test: /\.ttf/, use: ["url-loader?mimetype=font/ttf"] }
    ]
  }
};
