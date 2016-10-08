request = require 'mixins/request'
mousetrap = require 'mousetrap'
cash = require 'cash-dom'
hammer = require 'hammerjs'
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


class Slides
  constructor: ->
    @slide_nb = null
    @container = cash('body > main > .slides')
    @_vw = window.innerWidth

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

    if nb < 0 or nb > 6 or @slide_nb is nb then return
    lt = @slide_nb > nb
    margin = nb * @_vw

    @container
      .css('margin-left', "-#{margin}px")
      .attr('slide-active', ref)

    cash('body').attr('slide-active', ref)
    cash('.page-navigation a').each (el) ->
      is_active = el.attributes.href.value is "##{ref}"
      el.className = if is_active then 'active' else ''

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

    body = cash('body > main')
    hammertime = new hammer(body.get(0))
    hammertime.on 'panmove', (e) =>
      margin = @slide_nb * @_vw - e.deltaX
      body.addClass 'panning'
      @container.css('margin-left', "-#{margin}px")

    hammertime.on 'panend', (e) =>
      body.removeClass 'panning'
      margin = @slide_nb * @_vw
      @container.css('margin-left', "-#{margin}px")

    hammertime.on 'swiperight', ltHandler
    hammertime.on 'swipeleft', rtHandler

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

  reinit: ->
    @activate @slide_nb


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
      backdrop.reinit()
    debugging: ->
      backdrop.reinit()
    sponsors: ->
      backdrop.reinit()

  slides.init()
  splash = cash('#splash')

  document.addEventListener 'DOMContentLoaded', ->
    splash.addClass 'loaded'
    window.setTimeout ->
      splash.remove()
      slides.reinit()
    , 400
