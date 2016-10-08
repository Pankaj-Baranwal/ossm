cash = require 'cash-dom'
request = require 'mixins/request'
Terminal = require 'ossm/term'


class Ossm
  constructor: ->
    @attach_nav()
    @attach_terminal()

  attach_terminal: ->
    el = document.getElementById 'term'
    new Terminal(el)

  attach_nav: ->
    cash('a[data-toggle]').on 'click', (e) ->
      elselect = @dataset.toggle
      cash(elselect).toggleClass('open')
      false

    cash('body').on 'click', (e) ->
      el = cash(e.target)
      alpha = el.data('toggle')?
      beta = !!(el.parents().filter (n) -> cash(n).data('toggleTarget')).length
      unless alpha or beta
        cash('[data-toggle-target]').removeClass('open')


module.exports = ->
  new Ossm()
