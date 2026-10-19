"use strict";

const searchInput = document.querySelector("#lesson-search");
const lessonList = document.querySelector("#lesson-list");
const emptyState = document.querySelector("#empty-state");
const resultsSummary = document.querySelector("#results-summary");
const filterButtons = [...document.querySelectorAll(".filter-button")];
let catalog;
let activeFilter = "all";
let topics = {};

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]);
}

function setStats(data) {
  const { totals } = data;
  document.querySelector("#stat-lessons").textContent = totals.lessons;
  document.querySelector("#stat-exercises").textContent = totals.exercises;
  document.querySelector("#stat-assembly").textContent = totals.assembly_files;
  document.querySelector("#stat-guides").textContent = totals.guides;
  document.querySelector("#filter-all-count").textContent = totals.assembly_files;
  const lessonNumbers = data.lessons.map((lesson) => lesson.number);
  const firstLesson = lessonNumbers.length ? Math.min(...lessonNumbers) : 0;
  const lastLesson = lessonNumbers.length ? Math.max(...lessonNumbers) : 0;
  document.querySelector("#diagram-lesson-range").textContent =
    lessonNumbers.length ? `${String(firstLesson).padStart(2, "0")}—${String(lastLesson).padStart(2, "0")}` : "00";
  document.querySelector("#diagram-exercise-count").textContent = `${totals.exercises} EXERCISES`;

  topics = Object.fromEntries(
    data.topics.map((topic) => [
      topic.id,
      topic.lessons.map((lesson) => lesson.number),
    ]),
  );
  for (const topic of data.topics) {
    const target = document.querySelector(`[data-topic-count="${topic.id}"]`);
    if (!target) continue;
    const count = topic.id === "labs"
      ? `${totals.assembly_files} FILES`
      : `${topic.lessons.length} LESSONS`;
    target.textContent = `${topic.label} / ${count}`;
  }
}

function renderActivity(activity, kind) {
  const kindLabel = kind === "exercise" ? "EXERCISE" : "SAMPLE";
  const guide = kind === "exercise"
    ? activity.guide
      ? `<a href="${escapeHtml(activity.guide)}">GUIDE</a>`
      : '<span class="missing-guide">NO GUIDE</span>'
    : "";
  return `<div class="activity-row">
    <span class="activity-kind">${kindLabel}</span>
    <span class="activity-name" title="${escapeHtml(activity.name)}">${escapeHtml(activity.name)}</span>
    <span class="activity-links"><a href="${escapeHtml(activity.source)}">ASM</a>${guide}</span>
  </div>`;
}

function renderLesson(lesson) {
  const exerciseCount = lesson.exercises.length;
  const sampleCount = lesson.samples.length;
  const badges = [
    exerciseCount ? `<span class="lesson-badge exercise">${exerciseCount} EXERCISE${exerciseCount === 1 ? "" : "S"}</span>` : "",
    sampleCount ? `<span class="lesson-badge sample">${sampleCount} SAMPLE${sampleCount === 1 ? "" : "S"}</span>` : "",
  ].join("");
  const activities = [
    ...lesson.exercises.map((activity) => renderActivity(activity, "exercise")),
    ...lesson.samples.map((activity) => renderActivity(activity, "sample")),
  ].join("");
  const searchable = [
    lesson.title,
    lesson.description,
    ...lesson.exercises.flatMap((activity) => [activity.name, activity.description]),
    ...lesson.samples.map((activity) => activity.name),
  ].join(" ").toLowerCase();

  return `<details class="lesson-card" data-lesson="${lesson.number}" data-exercises="${exerciseCount}" data-samples="${sampleCount}" data-search="${escapeHtml(searchable)}">
    <summary class="lesson-summary">
      <span class="lesson-number">${String(lesson.number).padStart(2, "0")}</span>
      <span class="lesson-copy">
        <span class="lesson-title-row"><span class="lesson-title">${escapeHtml(lesson.title)}</span><span class="lesson-counter">${exerciseCount} EXERCISE${exerciseCount === 1 ? "" : "S"} / ${sampleCount} SAMPLE${sampleCount === 1 ? "" : "S"}</span></span>
        <span class="lesson-description">${escapeHtml(lesson.description)}</span>
      </span>
      <span class="lesson-badges">${badges}</span>
    </summary>
    <div class="lesson-details">
      <div class="detail-rule"></div>
      <div class="activity-list">${activities || '<span class="activity-name">No assembly sources in this lesson yet.</span>'}</div>
      <a class="lesson-notes-link" href="${escapeHtml(lesson.path)}">Open lesson notes -&gt;</a>
    </div>
  </details>`;
}

function currentQuery() {
  return searchInput.value.trim().toLowerCase();
}

function applyFilters() {
  const query = currentQuery();
  const cards = [...lessonList.querySelectorAll(".lesson-card")];
  let visible = 0;

  for (const card of cards) {
    const exercises = Number(card.dataset.exercises);
    const samples = Number(card.dataset.samples);
    const hasActivity = activeFilter === "all"
      ? exercises + samples > 0
      : activeFilter === "exercises" ? exercises > 0 : samples > 0;
    const matches = hasActivity && card.dataset.search.includes(query);
    card.hidden = !matches;
    if (matches) visible += 1;
  }

  emptyState.hidden = visible > 0;
  resultsSummary.textContent = `${String(visible).padStart(2, "0")} LESSON${visible === 1 ? "" : "S"} SHOWN`;
}

function setFilter(button) {
  activeFilter = button.dataset.filter;
  for (const candidate of filterButtons) {
    const selected = candidate === button;
    candidate.classList.toggle("active", selected);
    candidate.setAttribute("aria-pressed", String(selected));
  }
  applyFilters();
}

async function initialize() {
  try {
    const response = await fetch("data.json");
    if (!response.ok) throw new Error(`Dashboard data returned HTTP ${response.status}`);
    catalog = await response.json();
    setStats(catalog);
    lessonList.innerHTML = catalog.lessons.map(renderLesson).join("");
    applyFilters();
  } catch (error) {
    lessonList.innerHTML = `<p class="empty-state">Could not load the lesson catalog. Run <code>python dashboard/dashboard.py</code> from the repository root, then open this page through a local web server.</p>`;
    resultsSummary.textContent = "CATALOG UNAVAILABLE";
    console.error("Unable to load the architecture dashboard catalog:", error);
  }
}

searchInput.addEventListener("input", applyFilters);
for (const button of filterButtons) button.addEventListener("click", () => setFilter(button));
document.addEventListener("keydown", (event) => {
  if (event.key === "/" && !["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)) {
    event.preventDefault();
    searchInput.focus();
  }
  if (event.key === "Escape" && document.activeElement === searchInput) {
    searchInput.value = "";
    applyFilters();
    searchInput.blur();
  }
});

for (const topic of document.querySelectorAll("[data-topic]")) {
  topic.addEventListener("click", () => {
    const topicName = topic.dataset.topic;
    const lessonNumbers = topics[topicName];
    activeFilter = "all";
    filterButtons[0].click();
    searchInput.value = "";
    applyFilters();
    if (lessonNumbers && catalog) {
      for (const lessonNumber of lessonNumbers) {
        const lesson = lessonList.querySelector(`[data-lesson="${lessonNumber}"]`);
        if (lesson) lesson.open = true;
      }
    }
  });
}

initialize();
