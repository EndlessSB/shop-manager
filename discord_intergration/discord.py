import requests
import json
from config_management.config import config
from datetime import datetime

def send_webhook_embed(
    webhook_url,
    title=None,
    description=None,
    color=0x3498db,  # Default: Blue
    fields=None,     # List of dicts: [{"name": "Field1", "value": "Some value", "inline": False}, ...]
    footer_text=None,
    footer_icon_url=None,
    author_name=None,
    author_icon_url=None,
    author_url=None,
    thumbnail_url=None,
    image_url=None,
    timestamp=None    # ISO8601 string or None
):
    embed = {}

    if title:
        embed["title"] = title
    if description:
        embed["description"] = description
    if color:
        embed["color"] = color
    if fields:
        embed["fields"] = fields
    if footer_text:
        embed["footer"] = {"text": footer_text}
        if footer_icon_url:
            embed["footer"]["icon_url"] = footer_icon_url
    if author_name:
        embed["author"] = {"name": author_name}
        if author_icon_url:
            embed["author"]["icon_url"] = author_icon_url
        if author_url:
            embed["author"]["url"] = author_url
    if thumbnail_url:
        embed["thumbnail"] = {"url": thumbnail_url}
    if image_url:
        embed["image"] = {"url": image_url}
    if timestamp:
        embed["timestamp"] = timestamp

    payload = {
        "embeds": [embed]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code in (200, 204):
        print("Webhook embed sent successfully!")
    else:
        print(f"Failed to send webhook embed: {response.status_code} - {response.text}")


def product_create_alert(product, price):
    send_webhook_embed(
        webhook_url= config.discord_integration_link,
        title=f"{product} Has been added to the products",
        description="",
        color=0xff0000,  # red
        fields=[
            {"name": "Price", "value": f"${price}", "inline": False},
        ],
        footer_text="Store Manager Intergration",
        author_name="Managing",
        timestamp=datetime.now().isoformat()
    )
