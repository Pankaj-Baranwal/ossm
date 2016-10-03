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

class Oat
  constructor: (slides) ->
    @el = document.getElementById 'oat'
    @state =
      cx: 0
      cy: 100
      fl: no
      emote: ':)'
    @slides = slides
    @_init_rv_binding()
    @_init_key_binding()
    @move 0
    @slides._callback = (nb, lt) =>
      @state.cx = if lt
        @slides._vw * (nb + 1) - 50
      else
        @slides._vw * nb

  _init_rv_binding: ->
    @_view = rivets.bind @el, @state

  _init_key_binding: ->
    mousetrap.bind ['left', 'a', 'h'], => @move -40
    mousetrap.bind ['right', 'd', 'l'], => @move 30

  getY: (x) -> 500
  getX: (dx) ->
    dxi = @state.cx + dx
    switch
      when dxi < 10 then 10
      else dxi
  getEmote: ->
    switch
      when @state.cx < 10 then '⌐■ ⍘ ■ つ¤==>'
      when @state.cx < 100 then '୧ᴗ ε ᴗ つ¤==>'
      else '⸮> ∀ <?つ¤==>'

  move: (dx) ->
    @state.fl = dx < 0
    @state.cx = @getX dx
    @state.cy = @getY @state.cx
    @state.emote = @getEmote()
    @slides._activate_slide ~~(@state.cx / @slides._vw)


class Woot
  access_uri: '/static/img/rad/woot.json'
  element_id: 'woot'

  constructor: ->
    @_sprites = {}
    @svg = new svg document.getElementById @element_id
    @_vp =
      h: window.innerHeight
      w: window.innerWidth
    @_init_()

  _init_: ->
    request(url: @access_uri).then (dat) => @routine(dat)

  routine: (dat) ->
    defs = @svg.defs()
    dat.map (node) =>
      path = @svg.path node.path
      path.node.id = node.id
      defs.add path
    @draw(0, 60, '#2A9D8F')
    @draw()

  draw: (x = 0, y = 0, fill = '#007EA7', scale = 1) ->
    ###
    # [L1, L2] >=> [CS2, CL2]
    # [L3, L4] >=> [CS4, CL4]
    # [CS1, CL1, CS3, CL3] >=> [R1, R2]
    # [CS2, CL2, CS4, CL4] >=> [CS1, CS2, CL1, CL2, R3, R4]
    ###
    group = @svg.group().move(x, y + (@_vp.h - 450)).fill(fill).scale(.8)
    w_l = 0
    e_l = null
    s_count = ~~(@_vp.w * 4 / 80)
    for i in [0..s_count]
      elid = null
      if i is 0
        elid = _sample ['L3', 'L4']
      else if i is s_count - 1
        elid = _sample ['R3', 'R4']
      else
        #if e_l in ['CS2', 'CL2', 'CS4', 'CL4'] or e_l.startsWith 'L'
        elid = _sample ['CS1', 'CS2', 'CL1', 'CL2']
      e_l = elid
      el = svg.get(elid)
      shape = @svg.use(el)
        .move w_l, _random(-20, 20)
        .scale 1.01
      group.add shape
      w_l += el.width()
    mask = @svg.rect(@_vp.w * 5, 800).move(0, 200).fill('#fff')
    group.clipWith mask


class Servers extends Woot
  access_uri: '/static/img/rad/servers.json'
  element_id: 'datacenter'

  constructor: ->
    super()
    {width, height} = @svg.node.getBoundingClientRect()
    @_vp.cw = width
    @_vp.ch = height

  routine: (data) =>
    defs = @svg.defs()
    for k, v of data
      defs.svg(v)
    @draw_racks()
    @draw_comp()
    @draw_blocks()

  draw_comp: ->
    master = @svg.group()
    comp = @svg.use(svg.get 'master')
    master.add(comp).center(@_vp.cw / 2, @_vp.ch / 2)

  draw_racks: ->
    racks = @svg.group()
    for i in [0...2]
      for j in [0...10]
        rack = @svg.use(svg.get 'rack')
          .move(140 * i, 30 * j)
          .scale(.2)
        racks.add rack
    {width, height} = racks.node.getBoundingClientRect()
    racks.move(0 - width, @_vp.ch - (height + 200))

  draw_blocks: ->
    blocks = @svg.group().move(100, 10)
    for i in [0...4]
      for j in [0...5]
        block = @svg.use(svg.get 'block')
          .scale(.3)
          .translate(130 * i, 20 * j)
        blocks.add block
    {width, height} = blocks.node.getBoundingClientRect()
    rect = @svg.rect(width, height).fill('#555572')
    blocks.add(rect).move(@_vp.cw - width, @_vp.ch - (height + 200))
    rect.scale(1.05, 1.1).back()

class Quake
  constructor: (container) ->
    @oat = new Oat container.querySelector '#oat'


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
  oat = new Oat(slides)
  new Woot()
  new Servers()
