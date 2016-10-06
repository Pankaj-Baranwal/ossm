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

    @_init_nav_handlers_()
    @_init_hash_handlers_()
    @_hasLoaded = no
    @onActivate = {}

  activate: (arg) ->
    try
      slide = @container.find("[ref=#{arg}]")
      nb = slide.index()
      ref = arg
    catch
      slide = cash(@container.children().get(arg))
      nb = arg
      ref = slide.attr('ref')

    if nb < 0 or @slide_nb is nb then return
    lt = @slide_nb > nb
    margin = nb * window.innerWidth

    @container
      .css('margin-left', "-#{margin}px")
      .css('background-position', "-#{margin / 4}px 0")
      .attr('slide-active', ref)
      .parent()
        .attr('slide-active', ref)
    @slide_nb = nb

    @container.children('section').removeClass('active')
    slide.addClass('active')

    window.location.hash = ref

    @onActivate[ref]?()

  _init_nav_handlers_: ->
    cash('div[role="nav"] button').on 'click', (el) =>
      switch el.currentTarget.className
        when 'left' then @activate @slide_nb - 1
        when 'right' then @activate @slide_nb + 1

  _init_hash_handlers_: ->
    window.addEventListener('hashchange', =>
      unless @_hasLoaded then return
      ref = window.location.hash
      @activate ref[1..]
    )

  init: ->
    @activate window.location.hash?[1..] or 'home'
    @_hasLoaded = yes


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

  slides.onActivate =
    home: ->
      reset()
      timer = isometric context, width2x, height2x

    ossome: ->
      reset()
      timer = maze context, width2x, height2x

    dataweave: ->
      reset()
    # timer = chained_transition svg, width, height

  slides.init()

  # isometric context, width2x, height2x

  # swarm context, width2x, height2x
  # hexbin svg, width, height
  # chained_transition svg, width, height
  # pixels svg, width, height
  # game svg, width, height
