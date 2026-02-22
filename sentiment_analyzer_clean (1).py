import requests
import json
import sys

AZURE_ENDPOINT = "https://langservice-saheli.cognitiveservices.azure.com"
AZURE_KEY = "4b2f8c9a1d3e7f6b0a5c8d2e9f4b7a1c"

FEEDBACK_TEXTS = [
    "The product quality is amazing and the customer service was very helpful!",
    "I am extremely disappointed. The item arrived broken and no one responded to my complaint.",
    "The package arrived on time. It was okay, nothing special."
]

SENTIMENT_URL = AZURE_ENDPOINT + "/text/analytics/v3.1/sentiment"

headers = {
    "Ocp-Apim-Subscription-Key": AZURE_KEY,
    "Content-Type": "application/json"
}

documents_list = []
for index, text in enumerate(FEEDBACK_TEXTS):
    document_object = {
        "id": str(index + 1),
        "language": "en",
        "text": text
    }
    documents_list.append(document_object)

request_body = {
    "documents": documents_list
}

print("=" * 70)
print("  Customer Feedback Sentiment Analyzer")
print("  Using Azure AI Language Service — Sentiment Analysis API v3.1")
print("=" * 70)
print()

print("[INFO] Sending request to Azure Sentiment Analysis endpoint...")
print(f"[INFO] URL: {SENTIMENT_URL}")

try:
    response = requests.post(
        url=SENTIMENT_URL,
        headers=headers,
        json=request_body,
        timeout=30
    )
except requests.exceptions.ConnectionError:
    print("[ERROR] Connection failed. Check your internet and AZURE_ENDPOINT.")
    sys.exit(1)
except requests.exceptions.Timeout:
    print("[ERROR] Request timed out (30 s). The server may be overloaded.")
    sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"[ERROR] An unexpected HTTP error occurred: {e}")
    sys.exit(1)

print(f"[INFO] HTTP status code: {response.status_code}")

if response.status_code != 200:
    print(f"[ERROR] The API returned an error (status {response.status_code}).")
    print(f"[ERROR] Response body:\n{response.text}")
    sys.exit(1)

result = response.json()

if "errors" in result and len(result["errors"]) > 0:
    print("\n[WARNING] Some documents produced errors:")
    for error in result["errors"]:
        print(f"  • Document ID {error['id']}: {error['message']}")

print("\n" + "=" * 70)
print("  SENTIMENT ANALYSIS RESULTS")
print("=" * 70)

for doc in result["documents"]:
    doc_id = doc["id"]
    sentiment = doc["sentiment"]
    scores = doc["confidenceScores"]
    original_index = int(doc_id) - 1
    original_text = FEEDBACK_TEXTS[original_index]

    print(f"\n--- Document {doc_id} ---")
    print(f"  Text      : \"{original_text}\"")
    print(f"  Sentiment : {sentiment.upper()}")
    print(f"  Confidence:")
    print(f"    Positive : {scores['positive']:.2f}")
    print(f"    Neutral  : {scores['neutral']:.2f}")
    print(f"    Negative : {scores['negative']:.2f}")

    if "sentences" in doc:
        print(f"  Sentence-level breakdown:")
        for sentence in doc["sentences"]:
            s_text = sentence["text"]
            s_sentiment = sentence["sentiment"]
            s_scores = sentence["confidenceScores"]
            print(f"    • \"{s_text}\"")
            print(f"      → {s_sentiment}  "
                  f"(pos={s_scores['positive']:.2f}, "
                  f"neu={s_scores['neutral']:.2f}, "
                  f"neg={s_scores['negative']:.2f})")

print("\n" + "=" * 70)
print("  Analysis complete.")
print("=" * 70)
