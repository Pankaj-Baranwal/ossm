# OSSM
fs = require 'fs'
glob = require 'glob'
_ = require 'lodash'

# [@prashnts] This bit here is used to generate the watched folders
MODULE_PATH = '**/frontend/**/@(index|main).@(coffee|cjsx|jsx|js|styl)'
watched = _
  .chain(glob.sync MODULE_PATH)
  .map (filename) ->
    [__, dirname] = /^(.+)\/(index|main).\w+$/.exec filename
    dirname
  .uniq()
  .value()

bundles = do ->
  bndls =
    js: 'js/vendors.js': /^node_modules/
    css: 'css/vendors.css': /^node_modules/
  for path in watched
    cpath = path.replace /\/?frontend/, ''
    app = if /^frontend/.test path then 'common' else cpath.replace /\//, '_'
    bndls.js["js/#{app}.js"]    = new RegExp "^#{path}\/[_\\d\\w]+\\.\\w+$"
    bndls.css["css/#{app}.css"] = new RegExp "^#{path}\/[_\\d\\w]+\\.\\w+$"
  bndls

console.log bundles
console.log "---> Discovered #{watched.length} components"


module.exports = config:
  paths:
    watched: watched

  conventions:
    ignored: [
      /tests\//
    ]

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

  npm:
    enabled: yes

  modules:
    nameCleaner: (path) ->
      path
        .replace /\.cjsx/, ''
        .replace /\.coffee/, ''
        .replace /\.js/, ''
        .replace /\.jsx/, ''
        .replace /\.styl/, ''
        .replace /frontend\//, ''
        .replace /\/index/, ''

  files:
    javascripts:
      joinTo: bundles.js
    stylesheets:
      joinTo: bundles.css
