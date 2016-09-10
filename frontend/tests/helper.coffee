
global.require_app = (name) ->
  [bundle, module...] = name.split('/')
  module_resolved = ['../..', bundle, 'frontend', module?.join?('/')].join('/')
  require(module_resolved)
