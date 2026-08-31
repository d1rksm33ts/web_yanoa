"use strict";

if ("scrollRestoration" in history) {
  history.scrollRestoration = "manual";
}

if (window.location.hash) {
  history.replaceState(null, "", window.location.pathname + window.location.search);
}

const showHero = () => window.scrollTo({ top: 0, left: 0, behavior: "instant" });

showHero();
window.addEventListener("pageshow", showHero);
window.addEventListener("load", showHero);

const typedElement = document.querySelector(".typed");

if (typedElement && window.Typed) {
  const strings = typedElement.dataset.typedItems.split(",").map((item) => item.trim());

  new window.Typed(".typed", {
    strings,
    loop: true,
    typeSpeed: 100,
    backSpeed: 50,
    backDelay: 2000,
  });
}
