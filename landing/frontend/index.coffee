request = require('mixins/request')

isometric = require 'landing/isometric'
maze = require 'landing/maze'
swarm = require 'landing/swarm'


module.exports = ->
  width = window.innerWidth * 2
  height = window.innerHeight * 2
  canvas = document.querySelector '#isoslide'
  canvas.width = width
  canvas.height = height

  context = canvas.getContext('2d')

  # isometric context, width, height
  # maze context, width, height
  swarm context, width, height
