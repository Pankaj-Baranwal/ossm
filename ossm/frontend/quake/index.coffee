rivets = require 'rivets'
mousetrap = require 'mousetrap'

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


class Quake
  constructor: (container) ->
    @oat = new Oat container.querySelector '#oat'


module.exports = ->
  new Quake document.getElementById 'quake'
