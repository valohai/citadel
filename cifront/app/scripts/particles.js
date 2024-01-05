import sample from "lodash/sample";

const MAX_PARTICLES = 500;
const PARTICLE_NUM_RANGE = [5, 6, 7, 8, 9, 10, 11, 12];
const PARTICLE_GRAVITY = 0.075;
const PARTICLE_SIZE = 8;
const PARTICLE_ALPHA_FADEOUT = 0.96;
const PARTICLE_VELOCITY_X_RANGE = [-2.5, 2.5];
const PARTICLE_VELOCITY_Y_RANGE = [-7, -3.5];
const PARTICLE_COLORS = {
  text: [255, 255, 255],
  "text.xml": [255, 255, 255],
  keyword: [0, 221, 255],
  variable: [0, 221, 255],
  "meta.tag.tag-name.xml": [0, 221, 255],
  "keyword.operator.attribute-equals.xml": [0, 221, 255],
  constant: [249, 255, 0],
  "constant.numeric": [249, 255, 0],
  "support.constant": [249, 255, 0],
  "string.attribute-value.xml": [249, 255, 0],
  "string.unquoted.attribute-value.html": [249, 255, 0],
  "entity.other.attribute-name.xml": [129, 148, 244],
  comment: [0, 255, 121],
  "comment.xml": [0, 255, 121],
};

const defaultColor = [255, 255, 255];

function getParticleColor(type) {
  return PARTICLE_COLORS[type] || defaultColor;
}

function randRange(r) {
  return r[0] + Math.random() * (r[1] - r[0]);
}

function createParticle(x, y, color) {
  return {
    x,
    y: y + 10,
    alpha: 1,
    color,
    velocity: {
      x: randRange(PARTICLE_VELOCITY_X_RANGE),
      y: randRange(PARTICLE_VELOCITY_Y_RANGE),
    },
  };
}

// eslint-disable-next-line import/prefer-default-export
export class ParticleHandler {
  constructor(canvas) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    this.canvas = canvas;
    this.canvasContext = this.canvas.getContext("2d");
    this.particles = [];
    this.particlePointer = 0;
  }

  drawParticles() {
    this.canvasContext.clearRect(0, 0, this.canvas.width, this.canvas.height);

    this.particles.forEach((particle) => {
      if (particle.alpha <= 0.1) {
        return;
      }

      particle.velocity.y += PARTICLE_GRAVITY;
      particle.x += particle.velocity.x;
      particle.y += particle.velocity.y;
      particle.alpha *= PARTICLE_ALPHA_FADEOUT;

      this.canvasContext.fillStyle = `rgba(${particle.color.join(", ")}, ${
        particle.alpha
      })`;
      this.canvasContext.fillRect(
        Math.round(particle.x - PARTICLE_SIZE / 2),
        Math.round(particle.y - PARTICLE_SIZE / 2),
        PARTICLE_SIZE,
        PARTICLE_SIZE,
      );
    });
  }

  spawnParticles(x, y, type) {
    const numParticles = sample(PARTICLE_NUM_RANGE);
    const color = getParticleColor(type);
    for (let i = 0; i < numParticles; i++) {
      this.particles[this.particlePointer] = createParticle(x, y, color);
      this.particlePointer = (this.particlePointer + 1) % MAX_PARTICLES;
    }
  }
}
