# Agora NHS
fs = require 'fs'
glob = require 'glob'
_ = require 'lodash'

# [@prashnts] This bit here is used to generate the watched folders
MODULE_PATH = '**/frontend/**/@(index|main).@(coffee|cjsx|jsx|js|styl)'
watched = _
  .chain(glob.sync MODULE_PATH)
  .map (filename) ->
    [_, dirname] = /^(.+)\/(index|main).\w+$/.exec filename
    dirname
  .uniq()
  .value()

console.log "---> Discovered #{watched.length} components"


module.exports = config:
  paths:
    watched: watched

  plugins:
    autoReload:
      enabled: yes
    postcss:
      processors: [
        require('autoprefixer')(['last 8 versions'])
      ]
    stylus:
      plugins: [
        'jeet'
        'axis'
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
        .replace /\.js/, ''
        .replace /\.jsx/, ''
        .replace /\.styl/, ''

  files:
    javascripts:
      joinTo: 'js/app.js'
    stylesheets:
      joinTo: 'css/app.css'
