const energyInput = document.getElementById("energy");
const timeInput = document.getElementById("time");
const complexityInput = document.getElementById("complexity");
const energyValue = document.getElementById("energy-value");
const timeValue = document.getElementById("time-value");
const complexityValue = document.getElementById("complexity-value");
const sessionOutput = document.getElementById("session-length");
const focusOutput = document.getElementById("focus-level");
const restOutput = document.getElementById("rest-minutes");

const state = {
  energy: parseFloat(energyInput.value),
  time: parseFloat(timeInput.value),
  complexity: parseFloat(complexityInput.value),
};

function trapezoid(value, left, leftTop, rightTop, right) {
  if (value <= left || value >= right) return 0;
  if (left === leftTop && value === left) return 1;
  if (right === rightTop && value === right) return 1;
  if (value < leftTop) return (value - left) / (leftTop - left);
  if (value <= rightTop) return 1;
  return (right - value) / (right - rightTop);
}

function fuzzifyEnergy(energy) {
  return {
    low: trapezoid(energy, 0, 0, 3.5, 5.5),
    medium: trapezoid(energy, 3, 4.5, 5.5, 7.5),
    high: trapezoid(energy, 6, 7.5, 10, 10),
  };
}

function fuzzifyTime(time) {
  return {
    short: trapezoid(time, 0, 0, 1.5, 3.0),
    medium: trapezoid(time, 1.5, 2.5, 4.5, 6.0),
    long: trapezoid(time, 4.0, 5.5, 8.0, 8.0),
  };
}

function fuzzifyComplexity(complexity) {
  return {
    easy: trapezoid(complexity, 0, 0, 2.5, 4.5),
    moderate: trapezoid(complexity, 3.5, 4.5, 6.5, 8.0),
    hard: trapezoid(complexity, 6, 7.5, 10, 10),
  };
}

function applyRules(energy, time, complexity) {
  const output = { session_length: 0, focus_level: 0, rest_needed: 0 };
  const weight = { session_length: 0, focus_level: 0, rest_needed: 0 };

  function add(strength, session, focus, rest) {
    output.session_length += strength * session;
    output.focus_level += strength * focus;
    output.rest_needed += strength * rest;
    weight.session_length += strength;
    weight.focus_level += strength;
    weight.rest_needed += strength;
  }

  add(Math.min(energy.high, time.long, complexity.easy), 3.0, 90, 10);
  add(Math.min(energy.high, time.long, complexity.moderate), 2.5, 85, 15);
  add(Math.min(energy.medium, time.medium, complexity.moderate), 1.75, 75, 20);
  add(Math.min(energy.medium, time.short, complexity.easy), 1.0, 70, 25);
  add(Math.min(energy.low, time.short, complexity.hard), 0.5, 50, 40);
  add(Math.min(energy.low, time.medium, complexity.easy), 1.0, 55, 35);
  add(Math.min(energy.high, time.short, complexity.hard), 1.25, 80, 20);
  add(Math.min(energy.medium, time.long, complexity.hard), 1.75, 70, 30);
  add(Math.min(energy.low, time.long, complexity.moderate), 1.25, 60, 35);
  add(Math.min(energy.medium, time.short, complexity.hard), 0.75, 65, 30);

  return {
    session_length: output.session_length / Math.max(weight.session_length, 1e-6),
    focus_level: output.focus_level / Math.max(weight.focus_level, 1e-6),
    rest_needed: output.rest_needed / Math.max(weight.rest_needed, 1e-6),
  };
}

function inferPlan(energy, time, complexity) {
  const energyFuzz = fuzzifyEnergy(energy);
  const timeFuzz = fuzzifyTime(time);
  const complexityFuzz = fuzzifyComplexity(complexity);
  return applyRules(energyFuzz, timeFuzz, complexityFuzz);
}

function render() {
  energyValue.textContent = state.energy.toFixed(1);
  timeValue.textContent = state.time.toFixed(1);
  complexityValue.textContent = state.complexity.toFixed(1);

  const plan = inferPlan(state.energy, state.time, state.complexity);
  sessionOutput.textContent = plan.session_length.toFixed(2);
  focusOutput.textContent = plan.focus_level.toFixed(0);
  restOutput.textContent = plan.rest_needed.toFixed(0);
}

function handleInput(event) {
  const { id, value } = event.target;
  state[id] = parseFloat(value);
  render();
}

energyInput.addEventListener("input", handleInput);
timeInput.addEventListener("input", handleInput);
complexityInput.addEventListener("input", handleInput);

render();
