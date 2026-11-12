/* global document */
"use strict";

// Progressive enhancement: show how many characters remain in a review.
document.addEventListener("DOMContentLoaded", () => {
  const review = document.querySelector("#review");
  if (!review) return;

  const counter = document.createElement("small");
  counter.className = "form-text";
  counter.setAttribute("aria-live", "polite");
  review.insertAdjacentElement("afterend", counter);

  const updateCount = () => {
    const limit = Number(review.maxLength);
    counter.textContent = `${limit - review.value.length} characters remaining`;
  };
  review.addEventListener("input", updateCount);
  updateCount();
});
