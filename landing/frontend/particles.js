/**
 * Created by devkhan on 06/10/16.
 * Inspiration: http://codepen.io/soulwire/pen/Ffvlo
 */

const d3 = require('d3');
const cash = require('cash-dom')

var ROWS = 30,
    COLS = 90,
    NUM_PARTICLES = ( ( ROWS ) * ( COLS ) ),
    THICKNESS = Math.pow( 30, 3 ),
    SPACING = 70,
    MARGIN = 100,
    COLOR = 220,
    DRAG = 0.95,
    EASE = 0.25,
    particle,
    list,
    tog,
    man,
    context,
    dx, dy,
    mx, my,
    d, t, f,
    a, b,
    i, n,
    width, height,
    p;

particle = {
    vx: 0,
    vy: 0,
    x: 0,
    y: 0
};

function init(ctx, w, h) {

    context = ctx;
    width = w;
    height = h;
    ROWS = ~~(height/SPACING);
    COLS = ~~(width/SPACING);
    NUM_PARTICLES = ROWS * COLS;
    man = false;
    tog = true;
    list = [];

    for ( i = 0; i < NUM_PARTICLES; i++ ) {
        p = Object.create( particle );
        p.x = p.ox = MARGIN + SPACING * ( i % COLS );
        p.y = p.oy = MARGIN + SPACING * Math.floor( i / COLS );

        list[i] = p;
    }

    // cash('canvas').on( 'mousemove', function(e) {
    //     var bounds = document.body.getBoundingClientRect();
    //     mx = e.clientX - bounds.left;
    //     my = e.clientY - bounds.top;
    //     man = true;
    // });
}

function step() {
    if ( tog = !tog ) {
        if ( !man ) {

            t = +new Date() * 0.001;
            mx = width * 0.5 + ( Math.cos( t * 2.1 ) * Math.cos( t * 0.9 ) * width * 0.45 );
            my = height * 0.5 + ( Math.sin( t * 3.2 ) * Math.tan( Math.sin( t * 0.8 ) ) * height * 0.45 );
        }

        for ( i = 0; i < NUM_PARTICLES; i++ ) {

            p = list[i];

            d = ( dx = mx - p.x ) * dx + ( dy = my - p.y ) * dy;
            f = -THICKNESS / d;

            if ( d < THICKNESS ) {
                t = Math.atan2( dy, dx );
                p.vx += f * Math.cos(t);
                p.vy += f * Math.sin(t);
            }

            p.x += ( p.vx *= DRAG ) + (p.ox - p.x) * EASE;
            p.y += ( p.vy *= DRAG ) + (p.oy - p.y) * EASE;
        }
    }
    else {
        b = ( a = context.createImageData( width, height ) ).data;

        for ( i = 0; i < NUM_PARTICLES; i++ ) {
            p = list[i];
            b[n = ( ~~p.x + ( ~~p.y * width ) ) * 4] = b[n+1] = b[n+2] = COLOR, b[n+3] = 255;
        }
        context.putImageData( a, 0, 0 );
    }

    requestAnimationFrame( step );
}

module.exports = (context, width, height) => {
    const timer = d3.timer(function(elapsed) {
        init(context, width, height);
        step();
        timer.stop();
    });
    return timer;
}
