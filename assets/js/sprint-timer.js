/* PANDAUDIT workflow sprint timer.
   Click the clock to start/pause. Double-click to reset and draw a new mission.
   State persists in localStorage so a sprint survives page navigation. */
(function () {
  "use strict";

  var clockEl = document.getElementById("sprint-clock");
  var missionEl = document.getElementById("sprint-mission");
  var labelEl = document.getElementById("sprint-label");
  var boxEl = document.getElementById("sprint-box");
  if (!clockEl || !missionEl || !labelEl || !boxEl) return;

  var DURATION = 25 * 60; // seconds
  var KEY = "pandaudit-sprint-v1";

  var MISSIONS = [
    "Pick one messy finance task. Define the source, the rule, the exception, and the review output.",
    "Take one recipe you use every month and draft it as a SKILL.md your AI agent could run.",
    "Write the control-total check for one close workbook: rows in, rows out, amount tied.",
    "List every manual step in one reconciliation. Circle the ones an agent could own.",
    "Turn one exception report into three buckets: matched, source A only, source B only.",
    "Document one lookup chain: the key, the mapping table, and what counts as unmatched.",
    "Draft the prompt you would hand an AI agent to clean this month's export. Be specific.",
    "Pick one dashboard that breaks. Write down the upstream cleanup rule that would fix it."
  ];

  var state = load() || fresh();

  function fresh() {
    return {
      remaining: DURATION,
      running: false,
      endAt: null,
      done: false,
      mission: Math.floor((Date.now() / 86400000)) % MISSIONS.length
    };
  }

  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (typeof s.remaining !== "number") return null;
      if (s.running && s.endAt) {
        s.remaining = Math.max(0, Math.round((s.endAt - Date.now()) / 1000));
        if (s.remaining === 0) { s.running = false; s.done = true; }
      }
      return s;
    } catch (e) { return null; }
  }

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* private mode */ }
  }

  function fmt(secs) {
    var m = Math.floor(secs / 60);
    var s = secs % 60;
    return m + ":" + (s < 10 ? "0" : "") + s;
  }

  function render() {
    clockEl.textContent = fmt(state.remaining);
    boxEl.classList.toggle("sprint-running", state.running);
    boxEl.classList.toggle("sprint-done", state.done);
    if (state.done) {
      labelEl.textContent = "sprint complete";
      missionEl.textContent = "Nice work. Post what you finished in the PANDAUDIT Discord, then double-click the clock for a new mission.";
    } else {
      labelEl.textContent = state.running ? "sprint running" : "workflow sprint";
      missionEl.textContent = MISSIONS[state.mission % MISSIONS.length];
    }
    clockEl.title = state.done
      ? "Double-click to reset"
      : (state.running ? "Click to pause · double-click to reset" : "Click to start · double-click to reset");
  }

  var intervalId = null;

  function tick() {
    if (!state.running) return;
    state.remaining = Math.max(0, Math.round((state.endAt - Date.now()) / 1000));
    if (state.remaining === 0) {
      state.running = false;
      state.done = true;
      state.endAt = null;
      stopTicking();
      save();
    }
    render();
  }

  function startTicking() {
    if (!intervalId) intervalId = setInterval(tick, 1000);
  }

  function stopTicking() {
    if (intervalId) { clearInterval(intervalId); intervalId = null; }
  }

  function toggle() {
    if (state.done) return; // completed sprints reset via double-click
    if (state.running) {
      state.remaining = Math.max(0, Math.round((state.endAt - Date.now()) / 1000));
      state.running = false;
      state.endAt = null;
      stopTicking();
    } else {
      state.endAt = Date.now() + state.remaining * 1000;
      state.running = true;
      startTicking();
    }
    save();
    render();
  }

  function reset() {
    var nextMission = (state.mission + 1) % MISSIONS.length;
    state = fresh();
    state.mission = nextMission;
    stopTicking();
    save();
    render();
  }

  clockEl.addEventListener("click", function () {
    // Delay so a double-click (reset) doesn't also toggle start/pause.
    if (clockEl._clickTimer) return;
    clockEl._clickTimer = setTimeout(function () {
      clockEl._clickTimer = null;
      toggle();
    }, 250);
  });

  clockEl.addEventListener("dblclick", function () {
    if (clockEl._clickTimer) {
      clearTimeout(clockEl._clickTimer);
      clockEl._clickTimer = null;
    }
    reset();
  });

  if (state.running) startTicking();
  render();
})();
