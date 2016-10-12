const d3 = require('d3')


module.exports = (context, width, height) => {
  context.globalAlpha = .2
  context.fillStyle = '#333333'
  let counts = 0, offX, offY, offYB = height / 2

  const timer = d3.timer(el => {
    if (el < 1000 || el - counts < 100) {
      return
    }
    context.save()
    if (Math.random() > .99) {
      context.clearRect(0, 0, width, height)
    }
    counts = el
    offX = (el % width)
    offY = offYB * (1 + Math.random())
    context.fillRect(offX, offY, offX * Math.random(), height)
    context.restore()
  })

  return timer
}
