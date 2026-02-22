# Setup & Explanation Guide — Customer Feedback Sentiment Analyzer

## Prerequisites

| Requirement | Details |
|---|---|
| **Python** | Version 3.7 or later. Check with `python --version`. |
| **pip** | Comes with Python. Check with `pip --version`. |
| **Azure subscription** | A free or paid Azure account. |
| **Language resource** | An "Azure AI Language" resource created in the Azure Portal. |

---

## Step 1 — Install the `requests` Library

Open PowerShell or Command Prompt and run:

```
pip install requests
```

> [!NOTE]
> `requests` is the **only** external dependency.  The other two imports
> (`json`, `sys`) ship with every Python installation (standard library).

### What does `requests` do? (C analogy)

| Python (`requests`) | C (`libcurl`) |
|---|---|
| `requests.post(url, headers=h, json=body)` | `curl_easy_setopt` + `curl_easy_perform` |
| `response.status_code` | Check `CURLINFO_RESPONSE_CODE` |
| `response.json()` | `cJSON_Parse(buffer)` |
| `response.text` | The raw `char *` buffer from your write callback |

---

## Step 2 — Create Your Azure Language Resource

1. Go to [https://portal.azure.com](https://portal.azure.com).
2. Click **Create a resource** → search for **Language** → select **Language service** → **Create**.
3. Fill in:
   - **Subscription**: your subscription
   - **Resource group**: create new or use existing
   - **Region**: pick the one closest to you
   - **Name**: a unique name (e.g. `my-language-svc`)
   - **Pricing tier**: **Free F0** is fine for testing
4. Click **Review + Create** → **Create**.
5. Once deployed, go to the resource → **Keys and Endpoint**.
6. Copy **Key 1** and the **Endpoint** URL.

---

## Step 3 — Plug In Your Credentials

Open `sentiment_analyzer.py` and replace the two placeholder strings:

```python
AZURE_ENDPOINT = "https://<YOUR-RESOURCE-NAME>.cognitiveservices.azure.com"
AZURE_KEY      = "<YOUR-SUBSCRIPTION-KEY>"
```

with your actual endpoint and key from Step 2.

> [!CAUTION]
> **Never commit your key to a public repository.**  For production code
> use environment variables or Azure Key Vault.

---

## Step 4 — Run the Script

```
cd C:\Users\Satyam\Documents\Azure_Project
python sentiment_analyzer.py
```

### Expected Output (example)

```
======================================================================
  Customer Feedback Sentiment Analyzer
  Using Azure AI Language Service — Sentiment Analysis API v3.1
======================================================================

[INFO] Sending request to Azure Sentiment Analysis endpoint...
[INFO] URL: https://<your-resource>.cognitiveservices.azure.com/text/analytics/v3.1/sentiment
[INFO] HTTP status code: 200

======================================================================
  SENTIMENT ANALYSIS RESULTS
======================================================================

--- Document 1 ---
  Text      : "The product quality is amazing and the customer service was very helpful!"
  Sentiment : POSITIVE
  Confidence:
    Positive : 0.98
    Neutral  : 0.01
    Negative : 0.01
  Sentence-level breakdown:
    • "The product quality is amazing and the customer service was very helpful!"
      → positive  (pos=0.98, neu=0.01, neg=0.01)

--- Document 2 ---
  Text      : "I am extremely disappointed. The item arrived broken and no one responded to my complaint."
  Sentiment : NEGATIVE
  Confidence:
    Positive : 0.00
    Neutral  : 0.01
    Negative : 0.99

--- Document 3 ---
  Text      : "The package arrived on time. It was okay, nothing special."
  Sentiment : MIXED
  Confidence:
    Positive : 0.30
    Neutral  : 0.50
    Negative : 0.20

======================================================================
  Analysis complete.
======================================================================
```

*(Exact numbers will vary based on the model version Azure is running.)*

---

## Key Python↔C Concept Map

| Python concept | C equivalent | Used in the script |
|---|---|---|
| `import requests` | `#include <curl/curl.h>` + linking `-lcurl` | Line 15 |
| `dict` (`{}`) | `struct` with named fields, or a hash-map | headers, request_body, each document |
| `list` (`[]`) | Dynamically-sized `void **` array | `documents_list`, `FEEDBACK_TEXTS` |
| `for x in list` | `for (int i=0; i<n; i++)` | Iterating documents & sentences |
| `enumerate()` | Manual index variable `i` alongside the loop | Building document IDs |
| `f"...{var}..."` | `printf("...%s...", var)` | All print statements |
| `str(n)` | `snprintf(buf, sz, "%d", n)` | Converting int ID to string |
| `dict["key"]` | `cJSON_GetObjectItem(obj, "key")` | Accessing JSON fields |
| `response.json()` | `cJSON_Parse(buffer)` | Parsing the API response |
| `try/except` | Checking return codes + `if/else` branches | Error handling around the POST call |
| `sys.exit(1)` | `exit(1)` from `<stdlib.h>` | Aborting on errors |

---

## Troubleshooting

| Error | Likely cause | Fix |
|---|---|---|
| `ConnectionError` | No internet or wrong endpoint URL | Verify the URL in the Azure portal |
| HTTP **401** | Wrong subscription key | Copy Key 1 again from the portal |
| HTTP **404** | Wrong URL path or resource name | Double-check AZURE_ENDPOINT |
| HTTP **429** | Too many requests (rate limit) | Wait a minute and retry |
| `ModuleNotFoundError: No module named 'requests'` | `requests` not installed | Run `pip install requests` |
