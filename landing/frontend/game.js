const d3 = require('d3')

module.exports = (context, width, height) => {
  let cells = []
  context.strokeStyle = '#21344F';
  context.fillStyle = '#5D8722';
  context.lineWidth = 10;

  const cellSpacing = 20,
        cellWidth = ~~(1 + (width + cellSpacing) / (cellSpacing)),
        cellHeight = ~~(1 + (height + cellSpacing) / (cellSpacing));
  const offset = cellWidth > 60 ? 20 : 10

  function init() {
      for (var i=0; i<cellWidth; i++) {
          cells[i] = [];
          for (var j=0; j<cellHeight; j++) {
              cells[i][j] = 0;
          }
      }

      // Prefilled cells
      [
          // Gosper glider gun
          [1, 5],[1, 6],[2, 5],[2, 6],[11, 5],[11, 6],[11, 7],[12, 4],[12, 8],[13, 3],[13, 9],[14, 3],[14, 9],[15, 6],[16, 4],[16, 8],[17, 5],[17, 6],[17, 7],[18, 6],[21, 3],[21, 4],[21, 5],[22, 3],[22, 4],[22, 5],[23, 2],[23, 6],[25, 1],[25, 2],[25, 6],[25, 7],[35, 3],[35, 4],[36, 3],[36, 4],

          // [60, 47],[61,47],[62,47],
          // [60, 48],[61,48],[62,48],
          // [60, 49],[61,49],[62,49],
          // [60, 51],[61,51],[62,51],
          // [60, 51],[61,51],[62,51],
          // [20, 51],[31,51],
          [60, 30], [61, 30], [62, 30],           [64, 30],
          [60, 31],
                                        [63, 32], [64, 32],
                    [61, 33], [62, 33],           [64, 33],
          [60, 34],           [62, 34],           [64, 34],
      ]
      .forEach(function(point) {
        try {
          cells[point[0] + offset][point[1] + 10] = 1;
        } catch (e) {}
      });

      update();
  }

  function update() {
      var result = [];

      /**
       * Return amount of alive neighbours for a cell
       */
      function _countNeighbours(x, y) {
          var amount = 0;

          function _isFilled(x, y) {
              return cells[x] && cells[x][y];
          }

          if (_isFilled(x-1, y-1)) amount++;
          if (_isFilled(x,   y-1)) amount++;
          if (_isFilled(x+1, y-1)) amount++;
          if (_isFilled(x-1, y  )) amount++;
          if (_isFilled(x+1, y  )) amount++;
          if (_isFilled(x-1, y+1)) amount++;
          if (_isFilled(x,   y+1)) amount++;
          if (_isFilled(x+1, y+1)) amount++;

          return amount;
      }

      cells.forEach(function(row, x) {
          result[x] = [];
          row.forEach(function(cell, y) {
              var alive = 0,
                  count = _countNeighbours(x, y);

              if (cell > 0) {
                  alive = count === 2 || count === 3 ? 1 : 0;
              } else {
                  alive = count === 3 ? 1 : 0;
              }

              result[x][y] = alive;
          });
      });

      cells = result;

      draw();
  }


  function draw() {
      context.clearRect(0, 0, width, height);
      cells.forEach(function(row, x) {
          row.forEach(function(cell, y) {
              if (cell) {
                context.beginPath();
                context.rect(x * cellSpacing, y * cellSpacing, cellSpacing - 10, cellSpacing - 10);
                if (Math.random() > .42) {
                  context.fillStyle = '#0A71B6'
                } else if (Math.random() > .92) {
                  context.fillStyle = '#F4CE4B'
                } else {
                  context.fillStyle = '#78A153'
                }
                context.fill();
              }
          });
      });
  }

  const timer = d3.timer(() => {
    update()
  })
  init();
  return timer
}
