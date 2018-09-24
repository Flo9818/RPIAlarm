//example of using a message handler from the inject scripts
chrome.extension.onMessage.addListener(
  function(request, sender, sendResponse) {
  	chrome.pageAction.show(sender.tab.id);
    sendResponse();
  });

  console.log(chrome)

chrome.audio.onMuteChanged.addListener(function(event) {
  console.log(event);
});