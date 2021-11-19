"use strict";
function checkAndChange() {
    if (window.matchMedia("(prefers-color-scheme: dark)")) {
        //reader prefers dark mode
    } else if (window.matchMedia("(prefers-color-scheme: light)")) {
        //reader prefers light mode 🤨
    } else {
        //reader's browser is old
    }
}
checkAndChange();
window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", checkAndChange);
window.matchMedia("(prefers-color-scheme: light)").addEventListener("change", checkAndChange);
