const d3 = require('d3')
const _throttle = require('lodash/throttle')

const cursor = [[1, 0, 0, 0, 0, 0, 0],
       [1, 1, 0, 0, 0, 0, 0],
       [1, 2, 1, 0, 0, 0, 0],
       [1, 2, 2, 1, 0, 0, 0],
       [1, 2, 2, 2, 1, 0, 0],
       [1, 2, 2, 2, 2, 1, 0],
       [1, 2, 2, 2, 2, 1, 1],
       [1, 2, 1, 2, 1, 0, 0],
       [1, 1, 0, 1, 2, 1, 0],
       [0, 0, 0, 0, 1, 1, 0]]
const CUR_W = 11, CUR_H = 17

module.exports = (svg, width, height) => {
  const a = 10, b = 10,
        n = ~~((width + b) / (a + b)),
        m = ~~((height + b) / (a + b))

  const color = d3.scaleLinear()
          .domain([0, 20])
          .range(["#843B62", "#612B48"])
          .interpolate(d3.interpolateLab);

  let data = d3.select(svg)
    .selectAll("rect")
    .data(d3.range(n * m))

  let nodes = data.enter()
    .append("circle")
      .attr('fill', d => color(d%20))
      .attr("r", d => Math.random() * 3 + (a / 2))
      .attr("cx", d => b + ~~(d % n) * (a + b))
      .attr("cy", d => b + ~~(d / n) * (a + b))

  function mouseHandler (ev) {
    const cx = ~~(ev % n),
          cy = ~~(ev / n)

    nodes.attr('fill', function (d) {
      const dy = ~~(d % n) - cx + 2,
            dx = ~~(d / n) - cy + 4

      const bitc = cursor[dx] && cursor[dx][dy]

      switch (bitc) {
        case 1: return '#348AA7'
        case 2: return '#5DD39E'
        default: return color(d%20)
      }
    })
  }

  nodes.on('mouseover', _throttle(mouseHandler, 50))
}
