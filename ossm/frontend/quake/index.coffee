rivets = require 'rivets'
mousetrap = require 'mousetrap'
request = require 'mixins/request'
svg = require 'svg.js'

_sample = require 'lodash/sample'
_random = require 'lodash/random'


rivets.binders['coor-*'] = (el, value) ->
  prop = if @args[0] is 'x' then 'left' else 'top'
  el.style.setProperty(prop, "#{value}px")

class Oat
  constructor: (el) ->
    @el = el
    @state =
      cx: 0
      cy: 100
      fl: no
      emote: ':)'
    @_init_rv_binding()
    @_init_key_binding()
    @move 0

  _init_rv_binding: ->
    @_view = rivets.bind @el, @state

  _init_key_binding: ->
    mousetrap.bind ['left', 'a', 'h'], => @move -40
    mousetrap.bind ['right', 'd', 'l'], => @move 30

  getY: (x) -> if x > 200 then 200 else 100
  getX: (dx) ->
    dxi = @state.cx + dx
    switch
      when dxi < 10 then 10
      when dxi > 400 then 400
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


class Woot
  constructor: ->
    @_sprites = {}
    @svg = new svg document.getElementById 'woot'
    @_vp =
      h: window.innerHeight
      w: window.innerWidth
    @_init_()

  _init_: ->
    request(url: '/static/img/rad/woot.json')
    .then (dat) =>
      defs = @svg.defs()
      dat.map (node) =>
        path = @svg.path node.path
        path.node.id = node.id
        defs.add path
      #@draw(80, 250, '#14213D', 1)
      #@draw(60, 150, '#003459')
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
    console.log s_count
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


class Quake
  constructor: (container) ->
    @oat = new Oat container.querySelector '#oat'


module.exports = ->
  quaker = document.getElementById 'quake'
  new Quake quaker
  new Woot
