request = require 'mixins/request'
mousetrap = require 'mousetrap'
cash = require 'cash-dom'
d3 = require 'd3'

isometric = require 'landing/isometric'
maze = require 'landing/maze'
swarm = require 'landing/swarm'
hexbin = require 'landing/hexbin'
game = require 'landing/game'
chained_transition = require 'landing/chained_transition'
pixels = require 'landing/pixels'
balls = require 'landing/balls'
connectivity = require 'landing/connectivity'
particles = require 'landing/particles'


class Slides
  constructor: ->
    @slide_nb = null
    @container = cash('body > main > .slides')

    @_init_refs_()
    @_init_nav_handlers_()
    @_init_hash_handlers_()
    @_hasLoaded = no
    @onActivate = {}

  activate: (arg) ->
    try
      slide = @container.find("section[ref=#{arg}]")
      nb = @refs.indexOf(arg)
      ref = arg
    catch
      slide = cash(@container.children('section').get(arg))
      nb = arg
      ref = slide.attr('ref')

    if nb < 0 or nb > 5 or @slide_nb is nb then return
    lt = @slide_nb > nb
    margin = nb * window.innerWidth

    @container
      .css('margin-left', "-#{margin}px")
      .css('background-position', "-#{margin / 4}px 0")
      .attr('slide-active', ref)

    cash('body').attr('slide-active', ref)
    @slide_nb = nb

    @container.children('section').removeClass('active')
    slide.addClass('active')

    window.location.hash = ref

    @onActivate[ref]?(slide)

  _init_nav_handlers_: ->
    ltHandler = => @activate @slide_nb - 1
    rtHandler = => @activate @slide_nb + 1

    cash('button.switch.left').on 'click', ltHandler
    cash('button.switch.right').on 'click', rtHandler

    mousetrap.bind ['left', 'a', 'h'], ltHandler
    mousetrap.bind ['right', 'd', 'l'], rtHandler

  _init_hash_handlers_: ->
    window.addEventListener('hashchange', =>
      unless @_hasLoaded then return
      ref = window.location.hash
      @activate ref[1..]
    )

  _init_refs_: ->
    @refs = @container.find('section[ref]').map((el) -> cash(el).attr('ref'))

  init: ->
    initial_hash = window.location.hash?[1..]
    @activate if initial_hash in @refs then initial_hash else 'home'
    @_hasLoaded = yes


class Backdrop
  constructor: ->
    @canvas = document.querySelector '#backdrop'
    @width = 2 * window.innerWidth
    @height = 2 * window.innerHeight

    @canvas.width = @width
    @canvas.height = @height

    @context = @canvas.getContext('2d')
    @timer = null

  reinit: ->
    @context.clearRect 0, 0, @width, @height
    @timer?.stop?()

  init: (animation) ->
    @reinit()
    @timer = animation @context, @width, @height


module.exports = ->
  slides = new Slides()
  backdrop = new Backdrop()

  slides.onActivate =
    home: ->
      backdrop.init isometric
    ossome: ->
      backdrop.init maze
    dataweave: ->
      backdrop.init connectivity
    design: ->
      backdrop.init balls
    programming: ->
      backdrop.init particles

  slides.init()
