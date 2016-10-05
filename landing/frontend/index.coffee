request = require('mixins/request')

isometric = require 'landing/isometric'
maze = require 'landing/maze'
swarm = require 'landing/swarm'
hexbin = require 'landing/hexbin'
game = require 'landing/game'
chained_transition = require 'landing/chained_transition'
pixels = require 'landing/pixels'


module.exports = ->
  [width, height] = [window.innerWidth, window.innerHeight]
  [width2x, height2x] = (x * 2 for x in [width, height])

  canvas = document.querySelector '#isoslide'
  svg = document.querySelector '#hexslide'

  canvas.width = width2x
  canvas.height = height2x

  context = canvas.getContext('2d')

  # isometric context, width2x, height2x
  # maze context, width2x, height2x
  # swarm context, width2x, height2x
  # hexbin svg, width, height
  pixels svg, width, height
  # game svg, width, height
