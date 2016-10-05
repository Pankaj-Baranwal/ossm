request = require('mixins/request')
cash = require 'cash-dom'
d3 = require 'd3'

isometric = require 'landing/isometric'
maze = require 'landing/maze'
swarm = require 'landing/swarm'
hexbin = require 'landing/hexbin'
game = require 'landing/game'
chained_transition = require 'landing/chained_transition'
pixels = require 'landing/pixels'


class Slides
  constructor: ->
    @slide_nb = null
    @container = cash('div[role="slides"]')

    @_vw = window.innerWidth
    @_init_nav_handlers_()

    @onActivate = {}

  activate: (nb) ->
    if nb < 0 or @slide_nb is nb then return
    lt = @slide_nb > nb
    margin = nb * @_vw
    @container.css('margin-left', "-#{margin}px")
    @container.css('background-position', "-#{margin / 4}px 0")
    @container.attr('active', nb)
    @slide_nb = nb

    children = @container.children('section')
    children.removeClass('active')
    cash(children.get(nb)).addClass('active')

    @onActivate[nb]?()

  _init_nav_handlers_: ->
    cash('div[role="nav"] button').on 'click', (el) =>
      switch el.currentTarget.className
        when 'left' then @activate @slide_nb - 1
        when 'right' then @activate @slide_nb + 1


module.exports = ->
  [width, height] = [window.innerWidth, window.innerHeight]
  [width2x, height2x] = (x * 2 for x in [width, height])

  canvas = document.querySelector '#backdropC'
  context = canvas.getContext('2d')

  canvas.width = width2x
  canvas.height = height2x

  svg = document.querySelector '#backdropS'

  slides = new Slides()
  timer = null

  reset = ->
    context.clearRect(0, 0, width2x, height2x)
    cash(svg).empty()
    timer?.stop()

  slides.onActivate[0] = ->
    reset()
    timer = isometric context, width2x, height2x

  slides.onActivate[1] = ->
    reset()
    timer = maze context, width2x, height2x

  slides.onActivate[2] = ->
    reset()
    timer = chained_transition svg, width, height

  slides.activate(0)

  # isometric context, width2x, height2x

  # swarm context, width2x, height2x
  # hexbin svg, width, height
  # chained_transition svg, width, height
  # pixels svg, width, height
  # game svg, width, height
