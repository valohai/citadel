const autoprefixer = require('autoprefixer');
const path = require('path');

module.exports = {
  entry: './cifront/app/scripts/app.coffee',
  output: {
    path: path.resolve('./cifront/static/editor'),
    filename: 'bundle.js',
  },
  resolve: {
    extensions: [".js", ".coffee", ".scss", ".css", ".ttf"],
    alias: {
      "assets": path.resolve('./cifront/app/assets'),
    },
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          'style-loader',
          'css-loader',
          {
            loader: 'postcss-loader',
            options: {
              plugins: ((loader) => [
                autoprefixer({browsers: ["last 2 version"]}),
              ])
            },
          },
          'sass-loader',
        ]
      },
      {test: /\.coffee$/, use: ['coffee-loader']},
      {test: /\.png/, use: ['url-loader?mimetype=image/png']},
      {test: /\.ttf/, use: ['url-loader?mimetype=font/ttf']},
    ],
  },
};
