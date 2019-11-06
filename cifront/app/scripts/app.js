import "../styles/index.scss";
import { debounce, throttle, defer, sample } from "lodash";
import $ from "jquery";
import ace from "brace";
import "brace/mode/html";
import "brace/theme/vibrant_ink";
import "brace/ext/searchbox";

const POWER_MODE_ACTIVATION_THRESHOLD = 200;
const STREAK_TIMEOUT = 10 * 1000;

const MAX_PARTICLES = 500;
const PARTICLE_NUM_RANGE = [5, 6, 7, 8, 9, 10, 11, 12];
const PARTICLE_GRAVITY = 0.075;
const PARTICLE_SIZE = 8;
const PARTICLE_ALPHA_FADEOUT = 0.96;
const PARTICLE_VELOCITY_RANGE = {
  x: [-2.5, 2.5],
  y: [-7, -3.5]
};

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
  "comment.xml": [0, 255, 121]
};

const EXCLAMATION_EVERY = 10;
const EXCLAMATIONS = [
  "Super!",
  "Radical!",
  "Fantastic!",
  "Great!",
  "OMG",
  "Whoah!",
  ":O",
  "Nice!",
  "Splendid!",
  "Wild!",
  "Grand!",
  "Impressive!",
  "Stupendous!",
  "Extreme!",
  "Awesome!"
];

class App {
  constructor() {
    this.currentStreak = 0;
    this.powerMode = false;
    this.particles = [];
    this.particlePointer = 0;
    this.lastDraw = 0;

    this.$streakCounter = $(".streak-container .counter");
    this.$streakBar = $(".streak-container .bar");
    this.$exclamations = $(".streak-container .exclamations");
    this.$reference = $(".reference-screenshot-container");
    this.$nameTag = $(".name-tag");
    this.$result = $(".result");
    this.$editor = $("#editor");
    this.canvas = this.setupCanvas();
    this.canvasContext = this.canvas.getContext("2d");
    this.$finish = $(".finish-button");

    this.$body = $("body");

    this.debouncedSaveContent = debounce(this.saveContent, 300);
    this.debouncedEndStreak = debounce(this.endStreak, STREAK_TIMEOUT);
    this.throttledShake = throttle(this.shake, 100, { trailing: false });
    this.throttledSpawnParticles = throttle(this.spawnParticles, 25, {
      trailing: false
    });

    this.editor = this.setupAce();
    this.loadContent();
    this.editor.focus();

    this.editor.getSession().on("change", this.onChange);
    $(window).on("beforeunload", () => "Hold your horses!");

    $(".instructions-container, .instructions-button").on(
      "click",
      this.onClickInstructions
    );
    this.$reference.on("click", this.onClickReference);
    this.$finish.on("click", this.onClickFinish);
    this.$nameTag.on("click", () => this.getName(true));

    this.getName();

    if (typeof window.requestAnimationFrame === "function") {
      window.requestAnimationFrame(this.onFrame);
    }
  }

  setupAce() {
    const editor = ace.edit("editor");

    editor.setShowPrintMargin(false);
    editor.setHighlightActiveLine(false);
    editor.setFontSize(20);
    editor.setTheme("ace/theme/vibrant_ink");
    editor.getSession().setMode("ace/mode/html");
    editor.session.setOption("useWorker", false);
    editor.session.setFoldStyle("manual");
    editor.$blockScrolling = Infinity;

    return editor;
  }

  setupCanvas() {
    const canvas = $(".canvas-overlay")[0];
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    return canvas;
  }

  getName(forceUpdate) {
    const name =
      (!forceUpdate && localStorage["name"]) || prompt("What's your name?");
    localStorage["name"] = name;
    if (name) {
      this.$nameTag.text(name);
    }
  }

  loadContent() {
    let content;
    if (!(content = window.localStorage[window.STORAGE_ID || "content"])) {
      return;
    }
    this.editor.setValue(content, -1);
  }

  saveContent = () => {
    window.localStorage[
      window.STORAGE_ID || "content"
    ] = this.editor.getValue();
  };

  onFrame = time => {
    this.drawParticles(time - this.lastDraw);
    this.lastDraw = time;
    if (window.requestAnimationFrame) window.requestAnimationFrame(this.onFrame);
  };

  increaseStreak() {
    this.currentStreak++;
    if (
      this.currentStreak > 0 &&
      this.currentStreak % EXCLAMATION_EVERY === 0
    ) {
      this.showExclamation();
    }

    if (
      this.currentStreak >= POWER_MODE_ACTIVATION_THRESHOLD &&
      !this.powerMode
    ) {
      this.activatePowerMode();
    }

    this.refreshStreakBar();
    this.renderStreak();
  }

  endStreak() {
    this.currentStreak = 0;
    this.renderStreak();
    this.deactivatePowerMode();
  }

  renderStreak() {
    this.$streakCounter.text(this.currentStreak).removeClass("bump");

    defer(() => {
      this.$streakCounter.addClass("bump");
    });
  }

  refreshStreakBar() {
    this.$streakBar.css({
      "webkit-transform": "scaleX(1)",
      transform: "scaleX(1)",
      transition: "none"
    });

    defer(() => {
      this.$streakBar.css({
        "webkit-transform": "",
        transform: "",
        transition: `all ${STREAK_TIMEOUT}ms linear`
      });
    });
  }

  showExclamation() {
    const $exclamation = $("<span>")
      .addClass("exclamation")
      .text(sample(EXCLAMATIONS));

    this.$exclamations.prepend($exclamation);
    setTimeout(() => $exclamation.remove(), 3000);
  }

  getCursorPosition() {
    let { left, top } = this.editor.renderer.$cursorLayer.getPixelPosition();
    left += this.editor.renderer.gutterWidth + 4;
    top -= this.editor.renderer.scrollTop;
    return { x: left, y: top };
  }

  spawnParticles(type) {
    if (!this.powerMode) {
      return;
    }

    const { x, y } = this.getCursorPosition();
    const numParticles = sample(PARTICLE_NUM_RANGE);
    const color = this.getParticleColor(type);
    for (let i = 0; i < numParticles; i++) {
      this.particles[this.particlePointer] = this.createParticle(x, y, color);
      this.particlePointer = (this.particlePointer + 1) % MAX_PARTICLES;
    }
  }

  getParticleColor(type) {
    return PARTICLE_COLORS[type] || [255, 255, 255];
  }

  createParticle(x, y, color) {
    return {
      x,
      y: y + 10,
      alpha: 1,
      color,
      velocity: {
        x:
          PARTICLE_VELOCITY_RANGE.x[0] +
          Math.random() *
            (PARTICLE_VELOCITY_RANGE.x[1] - PARTICLE_VELOCITY_RANGE.x[0]),
        y:
          PARTICLE_VELOCITY_RANGE.y[0] +
          Math.random() *
            (PARTICLE_VELOCITY_RANGE.y[1] - PARTICLE_VELOCITY_RANGE.y[0])
      }
    };
  }

  drawParticles = timeDelta => {
    this.canvasContext.clearRect(0, 0, this.canvas.width, this.canvas.height);

    const result = [];
    this.particles.forEach(particle => {
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
      result.push(
        this.canvasContext.fillRect(
          Math.round(particle.x - PARTICLE_SIZE / 2),
          Math.round(particle.y - PARTICLE_SIZE / 2),
          PARTICLE_SIZE,
          PARTICLE_SIZE
        )
      );
    });
    return result;
  };

  shake() {
    if (!this.powerMode) {
      return;
    }

    const intensity =
      1 +
      2 *
        Math.random() *
        Math.floor(
          (this.currentStreak - POWER_MODE_ACTIVATION_THRESHOLD) / 100
        );
    const x = intensity * (Math.random() > 0.5 ? -1 : 1);
    const y = intensity * (Math.random() > 0.5 ? -1 : 1);

    this.$editor.css("margin", `${y}px ${x}px`);

    setTimeout(() => {
      this.$editor.css("margin", "");
    }, 75);
  }

  activatePowerMode = () => {
    this.powerMode = true;
    this.$body.addClass("power-mode");
  };

  deactivatePowerMode = () => {
    this.powerMode = false;
    this.$body.removeClass("power-mode");
  };

  onClickInstructions = () => {
    const $body = $("body");
    $body.toggleClass("show-instructions");
    if (!$body.hasClass("show-instructions")) {
      this.editor.focus();
    }
  };

  onClickReference = () => {
    this.$reference.toggleClass("active");
    if (!this.$reference.hasClass("active")) {
      this.editor.focus();
    }
  };

  onClickFinish = () => {
    const confirm = prompt(`\
This will show the results of your code. Doing this before the round is over \
WILL DISQUALIFY YOU. Are you sure you want to proceed? Type \"yes\" to confirm.\
`);
    if (!confirm) {
      return;
    }

    if (confirm.toLowerCase() !== "yes") {
      return;
    }
    const code = this.editor.getValue();
    this.trySaveCode(code);
    this.$result[0].contentWindow.postMessage(code, "*");
    this.$result.show();
  };

  onChange = event => {
    this.debouncedSaveContent();
    const insertTextAction = event.action === "insert";
    if (insertTextAction) {
      this.increaseStreak();
      this.debouncedEndStreak();
    }

    this.throttledShake();

    const pos = insertTextAction ? event.end : event.start;

    const token = this.editor.session.getTokenAt(pos.row, pos.column);

    defer(() => {
      if (token) {
        this.throttledSpawnParticles(token.type);
      }
    });
  };

  trySaveCode = code => {
    if (!window.SAVE_URL) {
      return;
    }
    return $.ajax({
      type: "POST",
      url: window.SAVE_URL,
      data: {
        token: window.SAVE_TOKEN || "",
        code,
        author: localStorage["name"] || ""
      },
      complete: (xhr, status) => {
        if (status !== "success") {
          alert(`Uploading your code failed (status: ${status})`);
        }
      }
    });
  };
}

$(() => new App());
