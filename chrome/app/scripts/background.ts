// Enable chromereload by uncommenting this line:
// import 'chromereload/devonly'

chrome.runtime.onInstalled.addListener((details) => {
  console.log('previousVersion', details.previousVersion);
});

chrome.browserAction.setBadgeText({
  text: `'Allo`
});

chrome.runtime.onInstalled.addListener((details) => {
  chrome.tabs.create({
    url: chrome.extension.getURL("pages/requestMicPermission.html"),
    active: true
  })
})

navigator.mediaDevices.getUserMedia({ audio: true })
  .then(function (stream) {
    console.log(stream.getAudioTracks());
    stream.getAudioTracks()[0].onmute = event => {
      console.log(event);
    };

    stream.getAudioTracks()[0].onunmute = event => {
      console.log(event);
    };
  })
  .catch(function (err) {
    /* handle the error */
    console.log(err);
  });
