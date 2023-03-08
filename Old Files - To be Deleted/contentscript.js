chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === "getSelection") {
    sendResponse({ selection: window.getSelection().toString() });
  }
});
