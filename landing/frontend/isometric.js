const d3 = require('d3')

const angle = Math.PI / 6
const identity = [
  1, 0, 0, 0,
  0, 1, 0, 0,
  0, 0, 1, 0
]

class Isometric {
  constructor (context) {
    this._moveTo = context.moveTo.bind(context);
    this._lineTo = context.lineTo.bind(context);
    this.closePath = context.closePath.bind(context);
    this._matrix = identity.slice();
    this._matrixes = [];
    this._projection = [
      Math.cos(angle), Math.cos(Math.PI - angle),
      -Math.sin(angle), -Math.sin(Math.PI - angle)
    ];
  }

  _project (point, x, y, z) {
    point(
      x * this._projection[0] + y * this._projection[1],
      x * this._projection[2] + y * this._projection[3] - z
    );
  }

  _transform (point, x, y, z) {
    this._project(point,
      x * this._matrix[0] + y * this._matrix[1] + z * this._matrix[2] + this._matrix[3],
      x * this._matrix[4] + y * this._matrix[5] + z * this._matrix[6] + this._matrix[7],
      x * this._matrix[8] + y * this._matrix[9] + z * this._matrix[10] + this._matrix[11]
    );
  }

  save () {
    this._matrixes.push(this._matrix.slice());
  }
  restore () {
    if (this._matrixes.length) this._matrix = this._matrixes.pop();
  }

  // | a b c d |   | kx  0  0 0 |   | a * kx b * ky c * kz d |
  // | e f g h | * |  0 ky  0 0 | = | e * kx f * ky g * kz h |
  // | i j k l |   |  0  0 kz 0 |   | i * kx j * ky k * kz l |
  // | 0 0 0 1 |   |  0  0  0 1 |   |      0      0      0 1 |
  scale3d (kx, ky, kz) {
    this._matrix[0] *= kx;
    this._matrix[1] *= ky;
    this._matrix[2] *= kz;
    this._matrix[4] *= kx;
    this._matrix[5] *= ky;
    this._matrix[6] *= kz;
    this._matrix[8] *= kx;
    this._matrix[9] *= ky;
    this._matrix[10] *= kz;
  }

  // | a b c d |   | cos -sin 0 0 |   | a * cos + b * sin a * -sin + b * cos c d |
  // | e f g h | * | sin  cos 0 0 | = | e * cos + f * sin e * -sin + f * cos g h |
  // | i j k l |   |   0    0 1 0 |   | i * cos + j * sin i * -sin + j * cos k l |
  // | 0 0 0 1 |   |   0    0 0 1 |   |                 0                  0 0 1 |
  rotateZ (angle) {
    var cos = Math.cos(angle),
        sin = Math.sin(angle),
        a = this._matrix[0],
        b = this._matrix[1],
        c = this._matrix[2],
        d = this._matrix[3],
        e = this._matrix[4],
        f = this._matrix[5],
        g = this._matrix[6],
        h = this._matrix[7],
        i = this._matrix[8],
        j = this._matrix[9],
        k = this._matrix[10],
        l = this._matrix[11];
    this._matrix[0] = a * cos + b * sin;
    this._matrix[1] = a * -sin + b * cos;
    this._matrix[4] = e * cos + f * sin;
    this._matrix[5] = e * -sin + f * cos;
    this._matrix[8] = i * cos + j * sin;
    this._matrix[9] = i * -sin + j * cos;
  }

  // | a b c d |   | 1 0 0 tx |   | a b c a * tx + b * ty + c * tz + d |
  // | e f g h | * | 0 1 0 ty | = | e f g e * tx + f * ty + g * tz + h |
  // | i j k l |   | 0 0 1 tz |   | i j k i * tx + j * ty + k * tz + l |
  // | 0 0 0 1 |   | 0 0 0  1 |   | 0 0 0                            1 |
  translate3d (tx, ty, tz) {
    this._matrix[3] += this._matrix[0] * tx + this._matrix[1] * ty + this._matrix[2] * tz;
    this._matrix[7] += this._matrix[4] * tx + this._matrix[5] * ty + this._matrix[6] * tz;
    this._matrix[11] += this._matrix[8] * tx + this._matrix[9] * ty + this._matrix[10] * tz;
  }

  moveTo (x, y, z) {
    this._transform(this._moveTo, x, y, z);
  }

  lineTo (x, y, z) {
    this._transform(this._lineTo, x, y, z);
  }
}


module.exports = (context, width, height) => {
  let isocontext = new Isometric(context);
  isocontext.scale3d(100, 100, 100);

  const timer = d3.timer(function(elapsed) {
    context.save();
    context.clearRect(0, 0, width, height);
    context.fillStyle = "#003459";
    context.strokeStyle = "#000";
    context.translate(width / 2, height * 0.6);
    for (let x = 14, d, t = (elapsed / 5000) % 1; x >= -14; --x) {
      for (let y = 14; y >= -14; --y) {
        if ((d = distanceManhattan(x, y)) > 15) {
          continue;
        }
        const te = d3.easeCubic(Math.max(0, Math.min(1, t * 4.8 - distanceCartesian(x, y) / 20)));
        drawCube((d & 1 ? -1 : +1) * (Math.PI / 4 - te * Math.PI / 2), x * 1.42, y * 1.42 + te * (x & 1 ? 1 : -1) * 1.42, te * 1.42 * 2);
      }
    }
    context.restore();
    if (elapsed > 5000) {
      timer.stop();
    }
  });

  function distanceCartesian(x, y) {
    return Math.sqrt(x * x + y * y);
  }

  function distanceManhattan(x, y) {
    return Math.abs(x) + Math.abs(y);
  }

  function drawCube(angle, x, y, z) {
    if ((angle %= Math.PI / 2) < 0) angle += Math.PI / 2;
    isocontext.save();
    isocontext.translate3d(x, y, z);
    isocontext.rotateZ(angle - Math.PI / 4);

    context.beginPath();
    isocontext.moveTo(+0.5, -0.5, +0.5);
    isocontext.lineTo(+0.5, +0.5, +0.5);
    isocontext.lineTo(-0.5, +0.5, +0.5);
    isocontext.lineTo(-0.5, +0.5, -0.5);
    isocontext.lineTo(-0.5, -0.5, -0.5);
    isocontext.lineTo(+0.5, -0.5, -0.5);
    isocontext.closePath();
    context.fill();
    context.lineWidth = 1.5;
    context.stroke();

    context.beginPath();
    isocontext.moveTo(-0.5, -0.5, +0.5);
    isocontext.lineTo(+0.5, -0.5, +0.5);
    isocontext.moveTo(-0.5, -0.5, +0.5);
    isocontext.lineTo(-0.5, +0.5, +0.5);
    isocontext.moveTo(-0.5, -0.5, +0.5);
    isocontext.lineTo(-0.5, -0.5, -0.5);
    context.lineWidth = 0.75;
    context.stroke();

    isocontext.restore();
  }
}
