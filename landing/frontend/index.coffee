request = require 'mixins/request'
mousetrap = require 'mousetrap'
cash = require 'cash-dom'
hammer = require 'hammerjs'
d3 = require 'd3'

isometric = require 'landing/isometric'
maze = require 'landing/maze'
balls = require 'landing/balls'
connectivity = require 'landing/connectivity'
game = require 'landing/game'
bsod = require 'landing/bsod'


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

  activate: (arg, reinit = no) ->
    try
      slide = @container.find("section[ref=#{arg}]")
      nb = @refs.indexOf(arg)
      ref = arg
    catch
      slide = cash(@container.children('section').get(arg))
      nb = arg
      ref = slide.attr('ref')

    if nb < 0 or nb > 6 or @slide_nb is nb and not reinit then return
    lt = @slide_nb > nb
    margin = nb * @_vw

    @container
      .css('margin-left', "-#{margin}px")
      .attr('slide-active', ref)

    cash('body')
      .attr('slide-active', ref)
      .attr('has-loaded', @_hasLoaded)

    cash('.page-navigation a').each (el) ->
      is_active = el.attributes.href.value is "##{ref}"
      el.className = if is_active then 'active' else ''

    cash('nav.root').prop 'scrollTop', 0

    @slide_nb = nb

    @container.children('section').removeClass('active')
    slide.addClass('active')

    window.location.hash = ref

    timer_id = window.setInterval ->
      scrollY = window.scrollY - 10
      if scrollY <= 0
        clearInterval timer_id
      else window.scrollTo(0, scrollY)
    , 1

    cash('[data-toggle-target]').removeClass('open')
    if @_hasLoaded or reinit then @onActivate[ref]?(slide)

  _init_nav_handlers_: ->
    ltHandler = => @activate @slide_nb - 1
    rtHandler = => @activate @slide_nb + 1

    cash('button.switch.left').on 'click', ltHandler
    cash('button.switch.right').on 'click', rtHandler

    body = cash('body')
    hammertime = new hammer(body.get(0))

    hammertime.on 'panstart', (e) ->
      body.addClass 'panning'

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

    mousetrap.bind ['left', 'pageup', 'a', 'h', 'shift+space', 'alt+b'], ltHandler
    mousetrap.bind ['right', 'pagedown', 'd', 'l', 'space', 'alt+f'], rtHandler

  _init_hash_handlers_: ->
    window.addEventListener('hashchange', =>
      unless @_hasLoaded then return
      ref = window.location.hash
      @activate ref[1..]
    )

  _init_refs_: ->
    @refs = @container.find('section[ref]').map((el) -> cash(el).attr('ref'))

  preinit: ->
    initial_hash = window.location.hash?[1..]
    @activate if initial_hash in @refs then initial_hash else 'home'

  init: ->
    @activate @slide_nb, yes
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
    @context.setTransform 1, 0, 0, 1, 0, 0
    @context.globalAlpha = 1
    @timer?.stop?()

  stop: ->
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
      backdrop.init game
    debugging: ->
      backdrop.init bsod
    sponsors: ->
      backdrop.reinit()

  slides.preinit()

  splash = cash('#splash')

  document.addEventListener 'DOMContentLoaded', ->
    splash.addClass 'loaded'
    slides.init()
    window.setTimeout ->
      splash.remove()
    , 400
