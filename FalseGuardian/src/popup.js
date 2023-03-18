//keywords might need to built more as fact checking websites have different ways of rating. Like four pinnochios means fake etc
//Define keywords for false or misleading claims. Tried my best to include all the keywords based on Google Fact Check API labelling
const falseKeywords = ["false", "misleading", "inaccurate", "unsupported", "partly false", "partly inaccurate", "Four Pinocchios",
  "baseless", "fabricated", "deceptive", "incorrect", "unproven", "unsubstantiated", "unfounded", "untrue", "exaggerated"];

// Define keywords for true or mostly true claims
const trueKeywords = ["true", "mostly true", "correct", "accurate", "supported", "partly true", "partly accurate", "verifiable"];
let rssEntries = [];


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
async function handleFormSubmit(event) {
  let selectedText = "";

  console.log("Form submitted");
  event.preventDefault();
  //Send message to content script to get the selected text
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    chrome.tabs.sendMessage(tabs[0].id, { action: "getSelection", allFrames: true }, async function (response) {
      selectedText = response.selection;

      // Get the selected text from the form
      // Encode the query for use in the URL
      console.log(selectedText);

      const parsedText = await sendQuery(selectedText);
      console.log(parsedText.tokens);

      const query = encodeURIComponent(parsedText.tokens);
      console.log(query)
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
          if (data && data.claims)
          {
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
        }
        else{
          console.error("No data found in Google fact check API")
          console.log("API does not have any data. Trying Other methods. Searching of Google")

          searchNewsAPI(selectedText);
        }

          // Compute the weighted score for this query term
          const totalCount = queryTrueCount + queryFalseCount + queryNeutralCount;
          const queryWeightedScore = totalCount > 0 ? (queryTrueCount - queryFalseCount) / totalCount : 0;

          // Display the results for this query term
          const resultDiv = document.getElementById("result");
          resultDiv.innerHTML = `<p>True: ${queryTrueCount}</p>
                               <p>False: ${queryFalseCount}</p>
                               <p>Neutral: ${queryNeutralCount}</p>
                               <p>Weighted score: ${queryWeightedScore}</p>`;

          if (totalCount == 0) {
            resultDiv.innerHTML += "<p>Not enough results to make a determination. Trying Google News. Please be patient!</p>";
            searchNewsAPI(selectedText);
            return;
          }

          if (queryWeightedScore < -0.5) {
            resultDiv.innerHTML += "<p>This sentence or speech is likely false</p>";
          } else if (queryWeightedScore >= -0.5 && queryWeightedScore < 0) {
            resultDiv.innerHTML += "<p>This sentence or speech has false or misleading claims</p>";
          } else if (queryWeightedScore > 0 && queryWeightedScore < 0.5) {
            resultDiv.innerHTML += "<p>This sentence or speech has some true and some false or misleading claims</p>";
          } 
          else if (queryWeightedScore > 0.5)
          {
            resultDiv.innerHTML += "<p>This sentence or speech is likely true or mostly true</p>";
          }
          else {
            resultDiv.innerHTML += "<p>This sentence or speech is inconclusive</p>";
          }
        })
        // If the API does not have any data, try searching using of NewsApi for news articles
        .catch(error => {
          console.log("API does not have any data. Trying Other methods. Searching of Google")

          searchNewsAPI(selectedText);
        });
    });
  });


}

function analyzeText(text) {
  const csrfToken = getCookie('csrftoken');
  return fetch("http://127.0.0.1:8000/analyze/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ text: text }),
  })
    .then((response) => response.json())
    .then((result) => {

      return result["compound"];
    })
    .catch((error) => {
      console.log("error", error);
      return null;
    });
}

function addToModel(articleText)
{
  const csrfToken = getCookie('csrftoken');
  return fetch("http://127.0.0.1:8000/addArticleText/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ articleText: articleText }),
    })
    .then((response) => response.json())
    .then((result) => {
      console.log(result);
      return result;
    })
    .catch((error) => {
      console.log("error", error);
    });
}

function trainModel(query) {
  const csrfToken = getCookie('csrftoken');
  return fetch("http://127.0.0.1:8000/train/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({query: query}),
  })
    .then((response) => response.json())
    .then((result) => {
      console.log(result);
      const resultString = JSON.stringify(result);
      return resultString;
      // Do something with the training result
    })
    .catch((error) => {
      console.log("error", error);
    });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function sendQuery(query) {
  const csrfToken = getCookie('csrftoken');
  return fetch("http://127.0.0.1:8000/extract/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ query: query }),
  })
    .then((response) => response.json())
    .then((result) => {
      console.log(result);
      return result;
    })
    .catch((error) => {
      console.log("error", error);
      return null;
    });
}


function searchNewsAPI(query) {
  const newsAPIKey = "307ec301188c402080a825919ece8621";
  const urlTemplate2 = 'https://newsapi.org/v2/everything?q=' + query + '&apiKey=' + newsAPIKey + '&language=en&sortBy=publishedAt&pageSize=100&summaryType=short';

  fetch(urlTemplate2)
    .then(response => response.json())
    .then(data => {
      const items = data.articles;
      const resultDiv = document.getElementById("result");

      if (items.length === 0) {
        resultDiv.innerHTML += "<p>No Results from Google news sources</p>";
        return;
      }
      
      let resultHtml = "<p>Predictions from Google news sources</p><ul>";

      // Create an array to store addToModel promises
      let addToModelPromises = [];

      items.forEach(item => {
        //resultHtml += `<li><a href="${item.url}" target="_blank">${item.title}</a></li>`;
        const articletext = item.description;
        console.log(articletext);
        
        // Push the addToModel promise into the array
        addToModelPromises.push(addToModel(articletext));
      });

      // Wait for all addToModel promises to resolve
      Promise.all(addToModelPromises).then(() => {
        console.log("Query is:", query);
        // After all promises have resolved, call the trainModel function
        trainModel(query).then(result => {
          console.log("Training ", result);

          resultHtml += "</ul>";
          resultHtml += "<p>Prediction: " + result + "</p>";
          resultDiv.innerHTML = resultHtml;
        })
        .catch(error => {
          console.log("Error: ", error);
        });
      })
      .catch(error => {
        console.log("Error: ", error);
      });

    })
    .catch(error => {
      console.log("Error fetching Google news API. No News Found ", error);
    });
}


// Add event listener 
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("check_fact");
  form.addEventListener("submit", handleFormSubmit);
  var b = document.getElementById('LoadModel');
  b.addEventListener('onclick', myFunction, false);
});
