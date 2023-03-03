// Define keywords for false or misleading claims
//keywords might need to built more as fact checking websites have different ways of rating. Like four pinnochios means fake etc

//Define keywords for false or misleading claims. Tried my best to include all the keywords
const falseKeywords = ["false", "misleading", "inaccurate", "unsupported", "partly false", "partly inaccurate", "Four Pinocchios",
  "baseless", "fabricated", "deceptive", "incorrect", "unproven", "unsubstantiated", "unfounded", "untrue", "exaggerated"];

// Define keywords for true or mostly true claims
const trueKeywords = ["true", "mostly true", "correct", "accurate", "supported", "partly true", "partly accurate", "verifiable"];

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

// Handle the form submission
function handleFormSubmit(event) {
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
}

// Add event listener 
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("check_tweet_button");
  form.addEventListener("submit", handleFormSubmit);
});

