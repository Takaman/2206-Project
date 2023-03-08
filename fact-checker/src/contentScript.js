'use strict';

// Content script file will run in the context of web page.
// With content script you can manipulate the web pages using
// Document Object Model (DOM).
// You can also pass information to the parent extension.

// We execute this script by making an entry in manifest.json file
// under `content_scripts` property

// For more information on Content Scripts,
// See https://developer.chrome.com/extensions/content_scripts

// Log `title` of current active web page
const pageTitle = document.head.getElementsByTagName('title')[0].innerHTML;
console.log(
  `Page title is: '${pageTitle}' - evaluated by Chrome extension's 'contentScript.js' file`
);

// Communicate with background file by sending a message
chrome.runtime.sendMessage(
  {
    type: 'GREETINGS',
    payload: {
      message: 'Initial message from contentScript.js',
    },
  },
  (response) => {
    console.log(response.message);
  }
);

// Listen for message this is for selection of text
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === "getSelection") {
    sendResponse({ selection: window.getSelection().toString() });
  }
});
