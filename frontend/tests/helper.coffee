
# global.require_app = (name) ->
#   [bundle, module...] = name.split('/')
#   module_resolved = ['../..', bundle, 'frontend', module?.join?('/')].join('/')
#   require(module_resolved)
require('../../public/js/vendors')
require('../../public/js/commons')
require('../../public/js/ossm')
require('../../public/js/landing')
