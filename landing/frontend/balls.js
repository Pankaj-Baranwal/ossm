const d3 = require('d3')


module.exports = (context, width, height) => {


  var nodes = d3.range(350).map(() => ({radius: Math.random() * 10 + 2})),
      root = nodes[0];

  root.radius = 0;
  root.fixed = true;
  const w2 = width / 2, h2 = height / 2

  const manybody = d3.forceManyBody(),
        centering = d3.forceCenter()

  var force = d3.forceSimulation(nodes)
        .force("charge", manybody)
        .force("center", centering);

  context.strokeStyle = "#6486AD";
  context.fillStyle = "#2D4472";
  context.lineWidth = 3;

  force.on("tick", function(e) {
    var q = d3.quadtree(nodes),
        i,
        d,
        x,
        y,
        n = nodes.length;

    for (i = 1; i < n; ++i) q.visit(collide(nodes[i]));

    context.clearRect(0, 0, width, height);
    context.beginPath();
    for (i = 1; i < n; ++i) {
      d = nodes[i];
      x = d.x + w2
      y = d.y + h2
      context.moveTo(x, y);
      context.arc(x, y, d.radius, 0, 2 * Math.PI);
    }
    context.stroke();
    context.fill();
  });

  function collide(node) {
    var r = node.radius + 16,
        nx1 = node.x - r,
        nx2 = node.x + r,
        ny1 = node.y - r,
        ny2 = node.y + r;
    return function(quad, x1, y1, x2, y2) {
      if (quad.point && (quad.point !== node)) {
        var x = node.x - quad.point.x,
            y = node.y - quad.point.y,
            l = Math.sqrt(x * x + y * y),
            r = node.radius + quad.point.radius;
        if (l < r) {
          l = (l - r) / l * .5;
          node.x -= x *= l;
          node.y -= y *= l;
          quad.point.x += x;
          quad.point.y += y;
        }
      }
      return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
    };
  }

  return force
}
