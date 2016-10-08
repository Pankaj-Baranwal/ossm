const d3 = require('d3')


module.exports = (context, width, height) => {
  const radius = 3,
        minDistance = 40,
        maxDistance = 120,
        minDistance2 = minDistance * minDistance,
        maxDistance2 = maxDistance * maxDistance

  const tau = 2 * Math.PI,
        n = ~~(width * height * .00004),
        particles = new Array(n)

  for (let i = 0; i < n; ++i) {
    particles[i] = {
      x: Math.random() * width,
      y: Math.random() * height,
      vx: 0,
      vy: 0
    }
  }

  context.strokeStyle = "#6486AD"
  context.fillStyle = "#f8cdda"
  context.lineWidth = 2

  const timer = d3.timer(function(elapsed) {
    context.save()
    context.clearRect(0, 0, width, height)

    for (var i = 0; i < n; ++i) {
      var p = particles[i]
      p.x += p.vx
      if (p.x < -maxDistance) {
        p.x += width + maxDistance * 2
      } else if (p.x > width + maxDistance) {
        p.x -= width + maxDistance * 2
      }
      p.y += p.vy
      if (p.y < -maxDistance) {
        p.y += height + maxDistance * 2
      } else if (p.y > height + maxDistance) {
        p.y -= height + maxDistance * 2
      }

      p.vx += 0.2 * (Math.random() - .5) - 0.01 * p.vx
      p.vy += 0.2 * (Math.random() - .5) - 0.01 * p.vy

      context.beginPath()
      context.arc(p.x, p.y, radius, 0, tau)
      context.fill()
    }

    for (var i = 0; i < n; ++i) {
      for (var j = i + 1; j < n; ++j) {
        let pi = particles[i],
            pj = particles[j],
            dx = pi.x - pj.x,
            dy = pi.y - pj.y,
            d2 = dx * dx + dy * dy
        if (d2 < maxDistance2) {
          context.globalAlpha = d2 > minDistance2
            ? (maxDistance2 - d2) / (maxDistance2 - minDistance2)
            : 1
          context.beginPath()
          context.moveTo(pi.x, pi.y)
          context.lineTo(pj.x, pj.y)
          context.stroke()
        }
      }
    }
    context.restore()
  })

  return timer
}
