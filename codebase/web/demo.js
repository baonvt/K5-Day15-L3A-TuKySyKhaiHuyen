"use strict";

const form = document.querySelector("#review-form");
const input = document.querySelector("#review-input");
const pasteMode = document.querySelector("#paste-mode");
const manualMode = document.querySelector("#manual-mode");
const pasteFields = document.querySelector("#paste-fields");
const manualFields = document.querySelector("#manual-fields");
const productName = document.querySelector("#product-name");
const reviewFields = document.querySelector("#review-fields");
const reviewTemplate = document.querySelector("#review-row");
const addReviewButton = document.querySelector("#add-review");
const reviewCount = document.querySelector("#review-count");
const exampleButton = document.querySelector("#load-example");
const submitButton = document.querySelector("#submit-review");
const copyButton = document.querySelector("#copy-result");
const status = document.querySelector("#form-status");
const resultBody = document.querySelector("#result-body");
const emptyResult = document.querySelector("#empty-result");
const emptyTitle = document.querySelector("#empty-title");
const emptyMessage = document.querySelector("#empty-message");
const result = document.querySelector("#analysis-result");
const MAX_REVIEWS = 30;
const reviewPattern = /^\[([1-5?])\]\s*(.+)$/s;

const example = [
  "Sản phẩm: Tai nghe X",
  "[5] Pin dùng được 2 ngày",
  "[5] Shop uy tín, mua ngay nhé",
  "[1] Tai trái mất tiếng sau 3 ngày",
].join("\n");
const trustStyles = new Map([
  ["Độ tin cậy cao", "high"],
  ["Chưa rõ độ tin cậy", "unclear"],
  ["Độ tin cậy thấp", "low"],
]);
let lastOutput = "";

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function normalizedInput(value) {
  const lines = value.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  if (value.includes("||")) return lines.join(" ");
  if (lines.length === 1 && /^\[[1-5?]\]/.test(lines[0])) return "|| " + lines[0];
  return lines.join(" || ");
}

function setStatus(message, isError = false) {
  status.textContent = message;
  status.classList.toggle("error", isError);
}

function setInputMode(manual) {
  pasteMode.setAttribute("aria-pressed", String(!manual));
  manualMode.setAttribute("aria-pressed", String(manual));
  pasteFields.hidden = manual;
  manualFields.hidden = !manual;
  setStatus("");
}

function updateReviewRows() {
  const count = reviewFields.children.length;
  for (const [index, row] of Array.from(reviewFields.children).entries()) {
    const name = `Review ${index + 1}`;
    row.querySelector("legend").textContent = name;
    row.querySelector("textarea").setAttribute("aria-label", `Nội dung ${name.toLowerCase()}`);
    row.querySelector("select").setAttribute("aria-label", `Số sao ${name.toLowerCase()}`);
    const remove = row.querySelector(".remove-review");
    remove.setAttribute("aria-label", `Xóa ${name.toLowerCase()}`);
    remove.hidden = count === 1;
  }
  addReviewButton.disabled = count >= MAX_REVIEWS;
  reviewCount.textContent = `${count}/${MAX_REVIEWS} review`;
}

function appendReview(content = "", stars = "?") {
  const row = reviewTemplate.content.firstElementChild.cloneNode(true);
  const review = row.querySelector("textarea");
  review.value = content;
  row.querySelector("select").value = stars;
  row.querySelector(".remove-review").addEventListener("click", () => {
    const next = row.nextElementSibling || row.previousElementSibling;
    row.remove();
    updateReviewRows();
    next.querySelector("textarea").focus();
  });
  reviewFields.append(row);
  return review;
}

function splitInput(value) {
  const parts = normalizedInput(value).split("||").map((part) => part.trim()).filter(Boolean);
  let product = null;
  const reviews = [];
  for (const part of parts) {
    const title = part.match(/^sản phẩm:\s*(.*)$/i);
    if (title && product === null) {
      product = title[1].trim();
      continue;
    }
    const review = part.match(reviewPattern);
    if (!review) return null;
    reviews.push({ stars: review[1], content: review[2].trim() });
  }
  return product !== null || reviews.length ? { product: product || "", reviews } : null;
}

function fillManualFields({ product, reviews }) {
  productName.value = product;
  reviewFields.replaceChildren();
  reviews.forEach(({ content, stars }) => appendReview(content, stars));
  if (!reviews.length) appendReview();
  updateReviewRows();
}

function convertPaste() {
  const draft = splitInput(input.value);
  if (!draft) {
    setStatus("Hãy dùng tên sản phẩm hoặc review có số sao ở đầu dòng để tách. Câu hỏi có thể gửi bằng nút Phân tích review.", true);
    input.focus();
    return;
  }
  if (draft.reviews.length > MAX_REVIEWS) {
    setStatus(`Chỉ tách được tối đa ${MAX_REVIEWS} review. Hãy bớt review hoặc phân tích từ ô dán.`, true);
    return;
  }
  fillManualFields(draft);
  setInputMode(true);
  setStatus(`Đã tách ${draft.reviews.length} review.`);
  productName.focus();
}

function manualInput() {
  const product = productName.value.trim();
  if (product.includes("||")) {
    setStatus("Tên sản phẩm không được chứa dấu ||.", true);
    productName.focus();
    return "";
  }
  const reviews = [];
  for (const row of reviewFields.children) {
    const field = row.querySelector("textarea");
    const content = field.value.trim();
    const stars = row.querySelector("select").value;
    if (!content && stars === "?") continue;
    if (!content || content.includes("||")) {
      setStatus(content ? "Nội dung review không được chứa dấu ||." : "Hãy nhập nội dung cho review đã chọn số sao.", true);
      field.focus();
      return "";
    }
    reviews.push(`[${stars}] ${content}`);
  }
  if (!reviews.length) {
    setStatus("Hãy nhập nội dung ít nhất một review.", true);
    reviewFields.querySelector("textarea").focus();
    return "";
  }
  const text = [product && `Sản phẩm: ${product}`, ...reviews].filter(Boolean).join(" || ");
  return normalizedInput(text);
}

function showPlaceholder(title, message) {
  emptyTitle.textContent = title;
  emptyMessage.textContent = message;
  emptyResult.hidden = false;
  result.hidden = true;
  copyButton.hidden = true;
}

function scoreCard(label, value, filtered = false) {
  const card = element("div", filtered ? "score filtered" : "score");
  const [amount, detail] = value.split(/\s+\((?=[^()]*\)$)/);
  const answer = element("strong", /^\d/.test(amount) ? "" : "unavailable", amount);
  card.append(element("span", "score-label", label), answer);
  if (detail) card.append(element("span", "score-detail", detail.replace(/\)$/, "")));
  return card;
}

function findingCard(title, items) {
  const section = element("section", "finding");
  section.append(element("h3", "", title));
  const findings = items
    .map((line) => line.replace(/^-\s+/, ""))
    .filter((line) => line !== "(không có)");
  if (!findings.length) {
    section.append(element("p", "no-finding", "Không có"));
    return section;
  }
  const list = element("ul");
  findings.forEach((finding) => list.append(element("li", "", finding)));
  section.append(list);
  return section;
}

function renderAnalysis(lines) {
  const labels = lines.indexOf("NHÃN TỪNG REVIEW:");
  const positives = lines.indexOf("ƯU ĐIỂM:");
  const negatives = lines.indexOf("NHƯỢC ĐIỂM:");
  const score = lines.findIndex((line) => line.startsWith("ĐIỂM SAO:"));
  const notice = lines.findIndex((line) => line.startsWith("LƯU Ý:"));
  if (labels !== 1 || positives <= labels || negatives <= positives || score <= negatives || notice <= score) {
    return false;
  }
  const starParts = lines[score].match(/^ĐIỂM SAO: gốc\s*:?\s*(.*?)\s*→\s*tính lại\s*:?\s*(.*)$/);
  const reviews = lines.slice(labels + 1, positives)
    .map((line) => line.match(/^(R\d+)\s*\|\s*([^|]+?)\s*\|\s*(.+)$/));
  if (!starParts || reviews.some((review) => !review)) return false;

  const title = element("h3", "product-title", lines[0].slice("SẢN PHẨM:".length).trim());
  const scores = element("div", "scores");
  scores.append(scoreCard("Điểm gốc", starParts[1]), scoreCard("Sau lọc", starParts[2], true));
  const list = element("ul", "review-list");
  for (const [, id, label, reason] of reviews) {
    const item = element("li", "review");
    const detail = element("div");
    detail.append(
      element("span", "review-label " + (trustStyles.get(label) || "unclear"), label),
      element("p", "", reason),
    );
    item.append(element("span", "review-id", id), detail);
    list.append(item);
  }
  const findings = element("div", "findings");
  findings.append(
    findingCard("Ưu điểm", lines.slice(positives + 1, negatives)),
    findingCard("Nhược điểm", lines.slice(negatives + 1, score)),
  );
  result.append(
    title, scores, element("h3", "review-heading", "Độ tin cậy từng review"),
    list, findings, element("p", "notice", lines[notice]),
  );
  return true;
}

function renderResult(data) {
  const lines = data.output.split(/\r?\n/).filter(Boolean);
  result.replaceChildren();
  if (!lines[0].startsWith("SẢN PHẨM:") || !renderAnalysis(lines)) {
    const message = element("div", "result-message");
    const colon = lines[0].indexOf(":");
    if (colon !== -1) {
      message.append(
        element("h3", "", lines[0].slice(0, colon)),
        element("p", "", [lines[0].slice(colon + 1).trim(), ...lines.slice(1)].join("\n")),
      );
    } else {
      message.append(element("p", "", data.output));
    }
    result.append(message);
  }
  const usage = data.usage;
  if (usage.models.length) {
    const model = usage.models.join(", ");
    result.append(element("p", "usage", `${model} · Token vào ${usage.tokens_in} · Token ra ${usage.tokens_out}`));
  }
  lastOutput = data.output;
  emptyResult.hidden = true;
  result.hidden = false;
  copyButton.hidden = false;
  copyButton.textContent = "Sao chép";
}

pasteMode.addEventListener("click", () => setInputMode(false));
manualMode.addEventListener("click", () => setInputMode(true));
document.querySelector("#split-reviews").addEventListener("click", convertPaste);
input.addEventListener("keydown", (event) => {
  if (event.key !== "Enter" || event.shiftKey || event.isComposing || event.keyCode === 229) return;
  event.preventDefault();
  convertPaste();
});
addReviewButton.addEventListener("click", () => {
  const field = appendReview();
  updateReviewRows();
  field.focus();
  setStatus("");
});
appendReview();
updateReviewRows();

exampleButton.addEventListener("click", () => {
  if (manualFields.hidden) {
    input.value = example;
    input.focus();
  } else {
    fillManualFields(splitInput(example));
    productName.focus();
  }
  setStatus("");
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (submitButton.disabled) return;
  const isManual = !manualFields.hidden;
  const text = isManual ? manualInput() : normalizedInput(input.value);
  if (!text) {
    if (!isManual) {
      setStatus("Hãy nhập bộ review hoặc câu hỏi.", true);
      input.focus();
    }
    return;
  }
  submitButton.disabled = true;
  submitButton.textContent = "Đang phân tích…";
  resultBody.setAttribute("aria-busy", "true");
  setStatus("Đang phân tích review.");
  showPlaceholder("Đang phân tích", "Kết quả sẽ hiển thị tại đây.");
  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    if (!response.ok) {
      showPlaceholder("Phân tích chưa hoàn tất", data.error);
      setStatus(data.error, true);
      return;
    }
    renderResult(data);
    setStatus("Đã có kết quả.");
  } catch {
    const message = "Không nhận được kết quả. Kiểm tra terminal đang chạy demo rồi thử lại.";
    showPlaceholder("Phân tích chưa hoàn tất", message);
    setStatus(message, true);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Phân tích review";
    resultBody.setAttribute("aria-busy", "false");
  }
});

copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(lastOutput);
    copyButton.textContent = "Đã sao chép";
    setStatus("Đã sao chép kết quả.");
  } catch {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(result);
    selection.removeAllRanges();
    selection.addRange(range);
    setStatus("Đã chọn kết quả. Nhấn Ctrl+C hoặc ⌘+C để sao chép.");
  }
});
