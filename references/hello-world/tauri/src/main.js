const { invoke } = window.__TAURI__.core;

window.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#button").addEventListener("click", () => {
    // Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
    invoke("clicked");
  });
});
