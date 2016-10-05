const d3 = require('d3')

module.exports = (svg, width, height) => {
  const a = 20, b = 2,
        n = ~~((width + b) / (a + b)),
        m = ~~((height + b) / (a + b))

  var whiteblue = d3.interpolateRgb("#eee", "steelblue"),
      blueorange = d3.interpolateRgb("steelblue", "orange"),
      orangewhite = d3.interpolateRgb("orange", "#eee");

  d3.select(svg).selectAll("rect")
      .data(d3.range(n * m))
    .enter()
      .append("rect")
      .attr('fill', 'red')
      .attr("width", a)
      .attr("height", a)
      .attr("x", d => b + ~~(d % n) * (a + b))
      .attr("y", d => b + ~~(d / n) * (a + b))
    .transition()
      .delay(function(d, i) { return i + Math.random() * n / 4; })
      .ease(d3.easeLinear)
      .on("start", function repeat() {
          d3.active(this)
              .styleTween("fill", function() { return whiteblue; })
            .transition()
              .delay(1000)
              .styleTween("fill", function() { return blueorange; })
            .transition()
              .delay(1000)
              .styleTween("fill", function() { return orangewhite; })
            // .transition()
            //   .delay(n)
            //   .on("start", repeat);
        });
}
