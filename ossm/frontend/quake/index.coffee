rivets = require 'rivets'
mousetrap = require 'mousetrap'

Isomer = require 'isomer'
{Shape, Point, Color} = Isomer
{Prism} = Shape

blue = new Color 50, 60, 160

class Quake
  constructor: (container) ->
    console.log Isomer
    @MULTIPLIER = 10
    @canvas =
      character:
        emotion: ':)'
        coor_x: 0
        left: no

    mousetrap.bind ['left', 'a', 'h'], @getMotion(-1)
    mousetrap.bind ['right', 'd', 'l'], @getMotion(1)

    @_view = rivets.bind container, @canvas

  getMotion: (direction) -> (e) =>
    @canvas.character.coor_x += direction * @MULTIPLIER
    console.log @canvas.character.coor_x


class IsoQuake
  constructor: (container) ->
    @container = container
    canvas = container.querySelector 'canvas'
    canvas.height = @_h = 2 * window.innerHeight
    canvas.width = @_w = 2 * window.innerWidth
    @context = canvas.getContext('2d')
    @iso = new Isomer canvas
    @_state =
      tile_count: 0
      frame_ct: 0
    window.requestAnimationFrame @stack_tiles

  clear: ->
    @context.clearRect(0, 0, @_w, @_h)

  stack_tiles: =>
    @clear()
    for i in [0...@_state.tile_count + 1]
      if i is @_state.tile_count
        @_state.frame_ct += 1
        @iso.add(Prism(Point(10 - i * 2, 0, 9 - @_state.frame_ct), 2, 2, .5))
        if @_state.frame_ct is 10
          @_state.frame_ct = 0
          @_state.tile_count += 1
      else
        @iso.add(Prism(Point(10 - i * 2, 0, -1), 2, 2, .5))
    if @_state.tile_count < 6
      window.requestAnimationFrame @stack_tiles

module.exports = ->
  new IsoQuake document.getElementById 'quake'
