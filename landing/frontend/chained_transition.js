const d3 = require('d3')

module.exports = (svg, width, height) => {
  const a = 10, b = 5,
        n = ~~((width + b) / (a + b)),
        m = ~~((height + b) / (a + b))

  var greenTeal = d3.interpolateRgb("#5DD39E", "#348AA7"),
      blueorange = d3.interpolateRgb("#348AA7", "#0582CA"),
      orangewhite = d3.interpolateRgb("#0582CA", "#2A9D8F");

  d3.select(svg).selectAll("rect")
      .data(d3.range(n * m))
    .enter()
      .append("circle")
      .attr('fill', 'transparent')
      .attr("r", d => Math.random() + (a / 2))
      .attr("cx", d => b + ~~(d % n) * (a + b))
      .attr("cy", d => b + ~~(d / n) * (a + b))
    .transition()
      .delay(function(d, i) { return i + Math.random() * n / 4; })
      .ease(d3.easeLinear)
      .on("start", function repeat() {
          d3.active(this)
              .styleTween("fill", function() { return greenTeal; })
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
