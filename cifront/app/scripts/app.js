import "../styles/index.scss";
import { debounce, defer, sample, throttle } from "lodash";
import $ from "jquery";
import ace from "brace";
import "brace/mode/html";
import "brace/theme/vibrant_ink";
import { ParticleHandler } from "./particles";

const POWER_MODE_ACTIVATION_THRESHOLD = 200;
const STREAK_TIMEOUT = 10 * 1000;

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

function setupAce() {
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

class App {
  constructor() {
    this.currentStreak = 0;
    this.powerMode = false;
    this.lastDraw = 0;

    this.$streakCounter = $(".streak-container .counter");
    this.$streakBar = $(".streak-container .bar");
    this.$exclamations = $(".streak-container .exclamations");
    this.$reference = $(".reference-screenshot-container");
    this.$nameTag = $(".name-tag");
    this.$result = $(".result");
    this.$editor = $("#editor");
    this.$finish = $(".finish-button");
    this.$body = $("body");

    this.particleHandler = new ParticleHandler($(".canvas-overlay")[0]);

    this.debouncedSaveContent = debounce(this.saveContent, 300);
    this.debouncedEndStreak = debounce(this.endStreak, STREAK_TIMEOUT);
    this.throttledShake = throttle(this.shake, 100, { trailing: false });
    this.throttledSpawnParticles = throttle(this.spawnParticles, 25, {
      trailing: false
    });

    this.editor = setupAce();
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

    if (window.requestAnimationFrame) {
      window.requestAnimationFrame(this.onFrame);
    }
  }

  getName(forceUpdate) {
    let { name } = localStorage;
    if (!name || forceUpdate) name = prompt("What's your name?");
    localStorage.name = name;
    if (name) {
      this.$nameTag.text(name);
    }
  }

  loadContent() {
    const content = window.localStorage[window.STORAGE_ID || "content"];
    if (!content) {
      return;
    }
    this.editor.setValue(content, -1);
  }

  saveContent = () => {
    const content = this.editor.getValue();
    window.localStorage[window.STORAGE_ID || "content"] = content;
  };

  onFrame = time => {
    this.particleHandler.drawParticles(time - this.lastDraw);
    this.lastDraw = time;
    if (window.requestAnimationFrame) {
      window.requestAnimationFrame(this.onFrame);
    }
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
    this.particleHandler.spawnParticles(x, y, type);
  }

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
    const confirm = prompt(`
This will show the results of your code. Doing this before the round is over 
WILL DISQUALIFY YOU. Are you sure you want to proceed? Type "yes" to confirm.
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
      return null;
    }
    return $.ajax({
      type: "POST",
      url: window.SAVE_URL,
      data: {
        token: window.SAVE_TOKEN || "",
        code,
        author: localStorage.name || ""
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
