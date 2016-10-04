const d3 = require('d3')

module.exports = (context, width, height) => {
  let data = d3.range(500).map(function() {
    return {xloc: 0, yloc: 0, xvel: 0, yvel: 0};
  });

  const angle = 2 * Math.PI;

  let x = d3.scaleLinear()
      .domain([-5, 5])
      .range([0, width]);

  let y = d3.scaleLinear()
      .domain([-5, 5])
      .range([0, height]);

  let time0 = Date.now(),
      time1;

  context.fillStyle = "#007EA7";
  context.strokeStyle = "#003459";
  context.strokeWidth = 1.5;

  d3.timer(function() {
    context.clearRect(0, 0, width, height);

    data.forEach(function(d) {
      d.xloc += d.xvel;
      d.yloc += d.yvel;
      d.xvel += 0.04 * (Math.random() - .5) - 0.05 * d.xvel - 0.0005 * d.xloc;
      d.yvel += 0.04 * (Math.random() - .5) - 0.05 * d.yvel - 0.0005 * d.yloc;
      context.beginPath();
      context.arc(x(d.xloc), y(d.yloc), Math.min(1 + 1000 * Math.abs(d.xvel * d.yvel), 10), 0, angle);
      context.fill();
      context.stroke();
    });
  });
}
