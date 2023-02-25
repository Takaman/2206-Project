import requests
import json

def label_rating(rating_text):
    #keywords might need to built more as fact checking websites have different ways of rating. Like four pinnochios means fake etc

    # Define keywords for false or misleading claims. Tried my best to include all the keywords
    false_keywords = ["false", "misleading", "inaccurate", "unsupported", "partly false", "partly inaccurate", "Four Pinocchios",
                      "baseless", "fabricated", "deceptive", "incorrect", "unproven", "unsubstantiated", "unfounded", "untrue", "exaggerated"]

    # Define keywords for true or mostly true claims this one is estimated only cause data varies
    true_keywords = ["true", "mostly true", "correct", "accurate", "supported", "partly true", "partly accurate" ,"verifiable"]

    #Convert both keywords  to lowercase and see whether it belongs to any of the categories


    for keyword in false_keywords:
        if keyword in rating_text.lower():
            return "false"

    for keyword in true_keywords:
        if keyword in rating_text.lower():
            return "true"

    #if nothing i just assume neutral
    return "neutral"

query_terms = ["vaccines cause autism", "The Earth revolves around the Sun.", "hydroxychloroquine is an effective treatment for COVID-19"]
api_key = "AIzaSyAvMF2h0dGexw34zHgDz3rWob2FTYAC8tE"
url_template = "https://factchecktools.googleapis.com/v1alpha1/claims:search?query={}&key={}"

# Initialize counters for true, false, and neutral responses
true_count = 0
false_count = 0
neutral_count = 0

# Loop through each query term
for query_term in query_terms:
    # Send a request to the Google Fact Checkera
    url = url_template.format(query_term, api_key)
    response = requests.get(url)

    # Parse the response as JSON
    if response.status_code == 200:
        results = json.loads(response.content)

        # Initialize counters for true, false, and neutral responses for this query term
        query_true_count = 0
        query_false_count = 0
        query_neutral_count = 0

        # Loop through each fact check result 
        for claim in results["claims"]:

            #publisher, url i guess not needed just the textualrating of the claim or sentence
            rating_text = claim["claimReview"][0]["textualRating"]

        
            # Map the rating text to a label
            label = label_rating(rating_text)

            if label == "true":
                query_true_count += 1
            elif label == "false":
                query_false_count += 1
            else:
                query_neutral_count += 1

        # Compute the weighted score for this query term
        total_count = query_true_count + query_false_count + query_neutral_count
        query_weighted_score = (query_true_count - query_false_count) / total_count if total_count > 0 else 0

        # Update the counters for true, false, and neutral responses
        true_count += query_true_count
        false_count += query_false_count
        neutral_count += query_neutral_count

        # Print the results for this query term
        print(f"Query term: {query_term}")
        print(f"True: {query_true_count}")
        print(f"False: {query_false_count}")
        print(f"Neutral: {query_neutral_count}")
        print(f"Weighted score: {query_weighted_score}")

        if total_count < 3:
            print("Not enough results to make a determination\n")
            continue
        
        # Print the overall results. Something like sentiment analysis but for fact checking of certain keywords
        if query_weighted_score < -0.5:
            print("This sentence or speech is likely false")
        elif query_weighted_score > -0.5 and query_weighted_score < 0:
            print("This sentence or speech has false or misleading claims")
        elif query_weighted_score > 0 and query_weighted_score < 0.5:
            print("This sentence or speech has some truth to it")
        elif query_weighted_score > 0.5:
            print("This sentence or speech is likely true")
        
        print()
    else:
        print(f"Error: {response.status_code} - {response.content}")
