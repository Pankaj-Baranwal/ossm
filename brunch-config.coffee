# Agora NHS
fs = require 'fs'
glob = require 'glob'

module.exports = config:
  paths:
    watched: ['frontend']

  plugins:
    autoReload:
      enabled: yes
    postcss:
      processors: [
        require('autoprefixer')(['last 8 versions'])
      ]
    coffeelint:
      pattern: /^frontend\/.*\.(coffee|cjsx)$/
      useCoffeelintJson: yes
    stylus:
      plugins: [
        'jeet'
      ]

  overrides:
    production:
      optimize: true
      sourceMaps: false
      plugins: autoReload: enabled: false

  npm:
    enabled: yes
    styles:
      'normalize.css': ['normalize.css']

  modules:
    nameCleaner: (path) ->
      path
        .replace /\.cjsx/, ''
        .replace /\.coffee/, ''

  files:
    javascripts:
      joinTo:
        'js/libraries.js': /^(?!frontend\/)/
        'js/frontend.js': /^frontend\//
    stylesheets:
      joinTo:
        'css/libraries.css': /^(?!frontend\/)/
        'css/frontend.css': /^frontend\//
