import * as tf from '@tensorflow/tfjs';

const natural = require('natural');

//keywords might need to built more as fact checking websites have different ways of rating. Like four pinnochios means fake etc
//Define keywords for false or misleading claims. Tried my best to include all the keywords
const falseKeywords = ["false", "misleading", "inaccurate", "unsupported", "partly false", "partly inaccurate", "Four Pinocchios",
  "baseless", "fabricated", "deceptive", "incorrect", "unproven", "unsubstantiated", "unfounded", "untrue", "exaggerated"];

// Define keywords for true or mostly true claims
const trueKeywords = ["true", "mostly true", "correct", "accurate", "supported", "partly true", "partly accurate", "verifiable"];
<<<<<<< HEAD
let rssEntries = [];

//Define our RSS feeds
const rssFeeds = [
  "https://www.rfa.org/english/RSS",
  "https://thediplomat.com/feed",
  "https://e27.co/index_wp.php/feed/",
  "https://www.asianscientist.com/feed/?x=1",
  "http://www.asianage.com/rss_feed/",
  "https://www.newmandala.org/feed/",
  "https://www.asiasentinel.com/feed/",
  "https://asia.nikkei.com/rss/feed/nar",
  "http://www.scmp.com/rss/91/feed",
  "https://www.channelnewsasia.com/rssfeeds/8395986",
  "https://asean.org/feed/",
];

=======

async function loadModel() {
  // Load the model
  const model = await tf.loadLayersModel('trainer/FalseGuardianJSModel/model.json');
  // Preprocess the data
  const inputData = "Trump";

  // Make predictions
  const predictions = model.predict(inputData).array();

  // Display the predictions
  console.log(predictions);

}
>>>>>>> 7082843 (Added ModelConvert and Modified FactChecker)

// Function to label the rating as true, false or neutral
function labelRating(ratingText) {
  // Check if the rating text contains any false keywords
  //Convert both keywords  to lowercase and see whether it belongs to any of the categories
  for (let keyword of falseKeywords) {
    if (ratingText.toLowerCase().includes(keyword)) {
      return "false";
    }
  }
  for (let keyword of trueKeywords) {
    if (ratingText.toLowerCase().includes(keyword)) {
      return "true";
    }
  }

  // If none of the keywords are found, return "neutral"
  return "neutral";
}

// Function to check the current URL using the Chrome API
function getCurrentUrl(callback) {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const url = tabs[0].url;
    callback(url);
  });
}


// Handle the form submission
function handleFormSubmit(event) {
<<<<<<< HEAD
  let selectedText = "";

  console.log("Form submitted");
  event.preventDefault();
  //Send message to content script to get the selected text
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    chrome.tabs.sendMessage(tabs[0].id, { action: "getSelection", allFrames: true }, function (response) {
      selectedText = response.selection;
  
    // Get the selected text from the form
    // Encode the query for use in the URL
    console.log(selectedText);
    const query = encodeURIComponent(selectedText);
    // Define the API key and URL put in the API key and the query
    const apiKey = "AIzaSyAvMF2h0dGexw34zHgDz3rWob2FTYAC8tE";
    const urlTemplate = `https://factchecktools.googleapis.com/v1alpha1/claims:search?query=${query}&key=${apiKey}`;

    // Send a request to the Google Fact Check API
    fetch(urlTemplate)
      .then(response => response.json())
      .then(data => {
        // Initialize counters for true, false, and neutral responses for this query term
        let queryTrueCount = 0;
        let queryFalseCount = 0;
        let queryNeutralCount = 0;

        // Loop through each fact check result
        for (let claim of data.claims) {
          const ratingText = claim.claimReview[0].textualRating;

          // Map the rating text to a label
          const label = labelRating(ratingText);

          if (label === "true") {
            queryTrueCount++;
          } else if (label === "false") {
            queryFalseCount++;
          } else {
            queryNeutralCount++;
          }
        }

        // Compute the weighted score for this query term
        const totalCount = queryTrueCount + queryFalseCount + queryNeutralCount;
        const queryWeightedScore = totalCount > 0 ? (queryTrueCount - queryFalseCount) / totalCount : 0;

        // Display the results for this query term
        const resultDiv = document.getElementById("result");
        resultDiv.innerHTML = `<p>True: ${queryTrueCount}</p>
=======
  console.log("Form submitted");
  event.preventDefault();
  // const query = document.getElementById("query").value;

  // Get the current tweet text. DOM is hard to get. I used api instead i guess
  //const tweetText = document.querySelector("div[data-testid='tweet'] span").textContent;
  const tweetUrl = window.location.href;
  const tweetId = tweetUrl.substr(tweetUrl.lastIndexOf("/") + 1);
  console.log(tweetId);

  // To be DONE
  const Token = "";
  const options = {
    headers: {
      Authorization: `Bearer ${Token}`
    },
  };

  // Get the tweet text using the Twitter API
  // Need to fix this and add our access token. Currently will get 403 forbidden error

  fetch(`https://twitter.com/i/api/2/timeline/conversation/${tweetId}.json`, options)
    .then(response => response.json())
    .then(data => {
      // Get the tweet text from the response
      const tweetText = data.globalObjects.tweets[tweetId].full_text;
      // Call the fact check function
      factCheck(tweetText);
    })
    .catch(error => {
      const resultDiv = document.getElementById("result");
      resultDiv.innerHTML = "<p>Error: Unable to fetch data from the Twitter API</p>";
      console.error(error);
    });


  // Encode the query for use in the URL
  const query = encodeURIComponent(tweetText);
  // Define the API key and URL put in the API key and the query
  const apiKey = "AIzaSyAvMF2h0dGexw34zHgDz3rWob2FTYAC8tE";
  const urlTemplate = `https://factchecktools.googleapis.com/v1alpha1/claims:search?query=${query}&key=${apiKey}`;

  // Send a request to the Google Fact Check API
  fetch(urlTemplate)
    .then(response => response.json())
    .then(data => {
      // Initialize counters for true, false, and neutral responses for this query term
      let queryTrueCount = 0;
      let queryFalseCount = 0;
      let queryNeutralCount = 0;

      // Loop through each fact check result
      for (let claim of data.claims) {
        const ratingText = claim.claimReview[0].textualRating;

        // Map the rating text to a label
        const label = labelRating(ratingText);

        if (label === "true") {
          queryTrueCount++;
        } else if (label === "false") {
          queryFalseCount++;
        } else {
          queryNeutralCount++;
        }
      }

      // Compute the weighted score for this query term
      const totalCount = queryTrueCount + queryFalseCount + queryNeutralCount;
      const queryWeightedScore = totalCount > 0 ? (queryTrueCount - queryFalseCount) / totalCount : 0;

      // Display the results for this query term
      const resultDiv = document.getElementById("result");
      resultDiv.innerHTML = `<p>True: ${queryTrueCount}</p>
>>>>>>> 7082843 (Added ModelConvert and Modified FactChecker)
                               <p>False: ${queryFalseCount}</p>
                               <p>Neutral: ${queryNeutralCount}</p>
                               <p>Weighted score: ${queryWeightedScore}</p>`;

<<<<<<< HEAD
        if (totalCount < 3) {
          resultDiv.innerHTML += "<p>Not enough results to make a determination</p>";
          return;
        }

        if (queryWeightedScore < -0.5) {
          resultDiv.innerHTML += "<p>This sentence or speech is likely false</p>";
        } else if (queryWeightedScore > -0.5 && queryWeightedScore < 0) {
          resultDiv.innerHTML += "<p>This sentence or speech has false or misleading claims</p>";
        } else if (queryWeightedScore > 0 && queryWeightedScore < 0.5) {
          resultDiv.innerHTML += "<p>This sentence or speech has some true and some false or misleading claims</p>";
        } else {
          resultDiv.innerHTML += "<p>This sentence or speech is likely true or mostly true</p>";
        }
      })
      // If the API does not have any data, try searching Google for news articles
      .catch(error => {

        console.log("API does not have any data. Trying Other methods. Searching of Google")
        searchNewsAPI(selectedText);
      });
  });
  });


}

function searchNewsAPI(query) {
    const newsAPIKey = "307ec301188c402080a825919ece8621";
    const urlTemplate2 = 'https://newsapi.org/v2/everything?q=' + query + '&apiKey=' + newsAPIKey + '&language=en&sortBy=publishedAt&pageSize=100';

    fetch(urlTemplate2)
        .then(response => response.json())
        .then(data => {
            const items = data.articles;
            const resultDiv = document.getElementById("result");

            if (items.length === 0) {
                resultDiv.innerHTML += "<p>No Results from Google news sources</p>";
                return;
            }

            let resultHtml = "<p>Search results from Google news sources</p><ul>";
            // Display search results
            items.forEach(item => {
                resultHtml += `<li><a href="${item.url}" target="_blank">${item.title}</a></li>`;
                fetch(item.url)
                .then(response => response.text())
                .then(html => {
                  //Process article content with NLP
                  const articletext= new DOMParser().parseFromString(html, "text/html").documentElement.textContent;
                  const tokenizer = new natural.WordTokenizer();
                  const tokens = tokenizer.tokenize(articletext);
                  console.log(tokens);
                })
                .catch(error => {
                    console.log(error);
                    console.log("Google link broken");
                });
            });

            resultHtml += "</ul>";
            resultDiv.innerHTML = resultHtml;
        })
        .catch(error => {
            console.log("No results from Google news sources");
        });
}


=======
      if (totalCount < 3) {
        resultDiv.innerHTML += "<p>Not enough results to make a determination</p>";
        return;
      }

      if (queryWeightedScore < -0.5) {
        resultDiv.innerHTML += "<p>This sentence or speech is likely false</p>";
      } else if (queryWeightedScore > -0.5 && queryWeightedScore < 0) {
        resultDiv.innerHTML += "<p>This sentence or speech has false or misleading claims</p>";
      } else if (queryWeightedScore > 0 && queryWeightedScore < 0.5) {
        resultDiv.innerHTML += "<p>This sentence or speech has some true and some false or misleading claims</p>";
      } else {
        resultDiv.innerHTML += "<p>This sentence or speech is likely true or mostly true</p>";
      }
    })
    .catch(error => {
      const resultDiv = document.getElementById("result");
      resultDiv.innerHTML = "<p>Error: Unable to fetch data from the Google Fact Check API</p>";
      console.error(error);
    });
}

>>>>>>> 7082843 (Added ModelConvert and Modified FactChecker)
// Add event listener 
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("check_tweet_button");
  form.addEventListener("submit", handleFormSubmit);
});

<<<<<<< HEAD

=======
>>>>>>> 7082843 (Added ModelConvert and Modified FactChecker)
