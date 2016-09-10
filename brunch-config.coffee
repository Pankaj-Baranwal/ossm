# OSSM
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

bundles = do ->
  bndls =
    js: 'js/vendors.js': /^node_modules/
    css: 'css/vendors.css': /^node_modules/
  for app in (watched.map (x) -> x.split('/')[0])
    bndls.js["js/#{app}.js"]    = new RegExp "^#{app}\/"
    bndls.css["css/#{app}.css"] = new RegExp "^#{app}\/"
  bndls

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
