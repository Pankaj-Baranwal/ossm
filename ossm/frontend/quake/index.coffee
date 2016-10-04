rivets = require 'rivets'
mousetrap = require 'mousetrap'
request = require 'mixins/request'
svg = require 'svg.js'
cash = require 'cash-dom'

_sample = require 'lodash/sample'
_random = require 'lodash/random'


rivets.binders['coor-*'] = (el, value) ->
  prop = if @args[0] is 'x' then 'left' else 'top'
  el.style.setProperty(prop, "#{value}px")


class Slides
  constructor: ->
    @slide_nb = null
    @_vw = window.innerWidth
    @container = cash('div[role="slides"]')
    @_init_nav_handlers_()
    @_callback = null
    @_activate_slide(0)

  _activate_slide: (nb) ->
    if nb < 0 or @slide_nb is nb then return
    lt = @slide_nb > nb
    margin = nb * @_vw
    @container.css('margin-left', "-#{margin}px")
    @container.css('background-position', "-#{margin / 4}px 0")
    @slide_nb = nb

    children = @container.children('section')
    children.removeClass('active')
    cash(children.get(nb)).addClass('active')

    @_callback?(nb, lt)

  _init_nav_handlers_: ->
    cash('div[role="nav"] button').on 'click', (el) =>
      switch el.currentTarget.className
        when 'left' then @_activate_slide @slide_nb - 1
        when 'right' then @_activate_slide @slide_nb + 1


module.exports = ->
  slides = new Slides()
