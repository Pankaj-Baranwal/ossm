request = require('mixins/request')

isometric = require 'landing/isometric'
maze = require 'landing/maze'
swarm = require 'landing/swarm'
hexbin = require 'landing/hexbin'
chained_transition = require 'landing/chained_transition'


module.exports = ->
  [width, height] = [window.innerWidth, window.innerHeight]
  [width2x, height2x] = (x * 2 for x in [width, height])

  canvas = document.querySelector '#isoslide'
  svg = document.querySelector '#hexslide'
  chained = document.querySelector '#chained'

  canvas.width = width2x
  canvas.height = height2x

  context = canvas.getContext('2d')

  # isometric context, width2x, height2x
  # maze context, width2x, height2x
  # swarm context, width2x, height2x
  # hexbin svg, width, height
  chained_transition chained
