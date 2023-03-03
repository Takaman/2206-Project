// Define keywords for false or misleading claims
//keywords might need to built more as fact checking websites have different ways of rating. Like four pinnochios means fake etc

//Define keywords for false or misleading claims. Tried my best to include all the keywords
const falseKeywords = ["false", "misleading", "inaccurate", "unsupported", "partly false", "partly inaccurate", "Four Pinocchios",
                      "baseless", "fabricated", "deceptive", "incorrect", "unproven", "unsubstantiated", "unfounded", "untrue", "exaggerated"];

// Define keywords for true or mostly true claims
const trueKeywords = ["true", "mostly true", "correct", "accurate", "supported", "partly true", "partly accurate" ,"verifiable"];

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
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    const url = tabs[0].url;
    callback(url);
  });
}
// Handle the form submission
function handleFormSubmit(event) {
  let selectedText = "";
    console.log("Form submitted");
    event.preventDefault();
    // Get the selected text from the current tab
    chrome.tabs.executeScript( {
      code: "window.getSelection().toString();"
  }, function(selection) {
      selectedText = selection[0];   
      
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
                               <p>False: ${queryFalseCount}</p>
                               <p>Neutral: ${queryNeutralCount}</p>
                               <p>Weighted score: ${queryWeightedScore}</p>`;
  
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
  });

 
  } 

  // Add event listener 
  document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("check_tweet_button");
    form.addEventListener("submit", handleFormSubmit);
  });

  
  