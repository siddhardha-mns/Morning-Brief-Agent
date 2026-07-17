import boto3
import json
import urllib.request

# --- Configuration ---
SENDER = "sidcodeees@gmail.com"
RECIPIENT = "sidcodeees@gmail.com"
MODEL_ID = "amazon.nova-micro-v1:0"
AWS_REGION = "ap-southeast-2"

# Sydney coordinates - change if you want a different city
LAT = -33.8688
LON = 151.2093


def get_weather():
    """Fetch current temperature from Open-Meteo (free, no API key needed)."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={LAT}&longitude={LON}&current=temperature_2m,weather_code&timezone=auto"
    )
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    temp = data["current"]["temperature_2m"]
    return f"{temp}°C in Sydney"


def get_top_headlines():
    """Fetch top 3 trending headlines from Hacker News public API."""
    ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    with urllib.request.urlopen(ids_url) as response:
        ids = json.loads(response.read())[:3]

    headlines = []
    for story_id in ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        with urllib.request.urlopen(story_url) as response:
            story = json.loads(response.read())
            headlines.append(story.get("title", ""))
    return headlines


def lambda_handler(event, context):
    bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    ses = boto3.client("ses", region_name=AWS_REGION)

    weather = get_weather()
    headlines = get_top_headlines()
    headlines_text = "\n".join(f"- {h}" for h in headlines)

    prompt = (
        f"Write a short, friendly morning brief email body for me.\n\n"
        f"Today's weather: {weather}\n\n"
        f"Top tech headlines today:\n{headlines_text}\n\n"
        f"Summarize the weather in one sentence, then briefly mention the "
        f"headlines in 2-3 sentences total. End with one short motivating "
        f"line. Keep it under 100 words. No markdown formatting."
    )

    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 300, "temperature": 0.7},
    )

    brief_text = response["output"]["message"]["content"][0]["text"]

    ses.send_email(
        Source=SENDER,
        Destination={"ToAddresses": [RECIPIENT]},
        Message={
            "Subject": {"Data": "☀️ Your Morning Brief"},
            "Body": {"Text": {"Data": brief_text}},
        },
    )

    return {"statusCode": 200, "body": "Email sent!"}
