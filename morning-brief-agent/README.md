# ☀️ Morning Brief Agent

An always-on AI agent that wakes up every morning on its own, checks the weather and top headlines, writes a short natural-language brief using Amazon Bedrock (Nova Micro), and emails it to you — before you even open your phone.

Built for the **AWS Build an Always-On Agent Weekend Challenge**.

---

## What It Does

- Triggers automatically every day at a scheduled time (no button click, no manual invocation)
- Fetches live weather data for a given location (Open-Meteo API — free, no key required)
- Fetches the top 3 trending headlines (Hacker News public API — free, no key required)
- Sends both to **Amazon Nova Micro** via Amazon Bedrock to generate a short, friendly morning brief
- Emails the finished brief via **Amazon SES**

The result: a personalized morning summary sitting in your inbox before you're even awake.

---

## Architecture

```
EventBridge Scheduler (daily cron trigger)
        │
        ▼
   AWS Lambda (lambda_function.py)
   ├── fetches live weather (Open-Meteo)
   ├── fetches top headlines (Hacker News API)
   ├── sends both to Amazon Bedrock (Nova Micro) for summarization
   └── sends final brief via Amazon SES
        │
        ▼
      Your Inbox
```

**AWS Services used:**
- **Amazon EventBridge Scheduler** — triggers the Lambda daily on a cron schedule
- **AWS Lambda** — runs the core agent logic
- **Amazon Bedrock (Nova Micro)** — generates the natural-language brief
- **Amazon SES** — delivers the email

Entirely serverless — no persistent infrastructure, runs for a few seconds once a day.

---

## Setup Instructions

### 1. Verify an email identity in SES
- AWS Console → SES → Verified identities → Create identity → Email address
- Verify via the confirmation link sent to your inbox

### 2. Deploy the Lambda function
- Create a new Lambda function (Python 3.12 runtime)
- Paste in `lambda_function.py`
- Update `SENDER` and `RECIPIENT` in the code with your verified email
- Set the region in `AWS_REGION` to one where Nova Micro is available on-demand (e.g. `ap-southeast-2`)
- Set function timeout to 60 seconds (Configuration → General configuration)

### 3. Attach IAM permissions
Attach these policies to the Lambda's execution role:
- `AmazonBedrockFullAccess`
- `AmazonSESFullAccess`

*(For production use, scope these down to only the specific actions needed.)*

### 4. Create the EventBridge schedule
- EventBridge → Scheduler → Create schedule
- Cron expression: `0 8 * * ? *` (8:00 AM daily)
- Execution time zone: set to your local time zone (e.g. `Australia/Sydney`)
- Target: AWS Lambda → Invoke → select your function

### 5. Test
- Manually invoke the Lambda once via the **Test** tab to confirm it works end-to-end
- Check your inbox for the "☀️ Your Morning Brief" email

---

## Customization

- Change `LAT` / `LON` in `lambda_function.py` to your own city's coordinates
- Swap the Hacker News API for any other free news source if you want general news instead of tech news
- Adjust the Bedrock prompt to change the tone or length of the brief

---

## Built With

- Python 3.12
- AWS Lambda
- Amazon Bedrock (Nova Micro)
- Amazon SES
- Amazon EventBridge Scheduler
- [Open-Meteo API](https://open-meteo.com/) (weather)
- [Hacker News API](https://github.com/HackerNews/API) (headlines)

---

## License

MIT
