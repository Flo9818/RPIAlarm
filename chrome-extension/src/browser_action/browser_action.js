document.getElementById("resetBtn").addEventListener("click", reset);
document.addEventListener("DOMContentLoaded", load);
document.getElementById("saveBtn").addEventListener("click", save);

var urlInput = document.getElementById("url");
var nameInput = document.getElementById("name");
var tokenInput = document.getElementById("token");

function load() {
  chrome.storage.local.get(["serverUrl"], function(result) {
    setValue(urlInput, result.serverUrl);
  });
  chrome.storage.local.get(["name"], function(result) {
    setValue(nameInput, result.name);
  });
  chrome.storage.local.get(["token"], function(result) {
    setValue(tokenInput, result.token);
  });
}

function save() {
    console.log('f')
  chrome.storage.local.set({ serverUrl: urlInput.value }, function() {});
  chrome.storage.local.set({ name: nameInput.value }, function() {});
  chrome.storage.local.set({ token: tokenInput.value }, function() {});
  M.toast({ html: "Settings saved" });
}

function setValue(input, value) {
  if (value) {
    input.value = value;
  } else {
    input.value = "";
  }
}

function reset() {
    console.log('ok')
  }
