cash = require 'cash-dom'


class Ossm
  constructor: ->
    @attach_nav()

  attach_nav: ->
    cash('a[data-toggle]').on 'click', (e) ->
      cash(@).next('[data-toggle="target"]').toggleClass('open')

    cash('body').on 'click', (e) ->
      el = cash(e.target)
      alpha = el.data('toggle')?
      beta = !!(el.parents().filter (n) -> cash(n).data('toggle')).length
      unless alpha or beta
        cash('[data-toggle="target"]').removeClass('open')


module.exports = Ossm
