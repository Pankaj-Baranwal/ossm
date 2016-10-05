const d3 = require('d3')
const _throttle = require('lodash/throttle')

const cursor = [
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0],
  [1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0],
  [1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0],
  [1, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0],
  [1, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0],
  [1, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0],
  [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
  [1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],
  [1, 2, 2, 2, 1, 2, 2, 1, 0, 0, 0],
  [1, 2, 2, 1, 0, 1, 2, 2, 1, 0, 0],
  [1, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0],
  [1, 1, 0, 0, 0, 0, 1, 2, 2, 1, 0],
  [0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
]
const CUR_W = 11, CUR_H = 17

module.exports = (svg, width, height) => {
  const a = 10, b = 2,
        n = ~~((width + b) / (a + b)),
        m = ~~((height + b) / (a + b))

  let data = d3.select(svg)
    .selectAll("rect")
    .data(d3.range(n * m))

  let nodes = data.enter()
    .append("circle")
      .attr('fill', 'red')
      .attr("r", a / 2)
      .attr("cx", d => b + ~~(d % n) * (a + b))
      .attr("cy", d => b + ~~(d / n) * (a + b))

  function mouseHandler (ev) {
    const cx = ~~(ev % n),
          cy = ~~(ev / n)

    nodes.attr('fill', function (d) {
      const dy = ~~(d % n) - cx + 5,
            dx = ~~(d / n) - cy + 8

      const bitc = cursor[dx] && cursor[dx][dy]

      switch (bitc) {
        case 1: return 'green'
        case 2: return 'blue'
        default: return 'red'
      }
    })
  }

  nodes.on('mouseover', _throttle(mouseHandler, 100))
}
