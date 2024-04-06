import requests
from bs4 import BeautifulSoup
import discord
import time
import aiohttp

# Function to fetch MyNintendo webpage
def fetch_my_nintendo_page():
    url = 'https://www.nintendo.com/en-ca/store/exclusives/rewards/'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to fetch MyNintendo webpage. Status code:", response.status_code)
            return None
    except requests.RequestException as e:
        print("Error fetching MyNintendo webpage:", e)
        return None

# Function to parse HTML content
def parse_html_content(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    else:
        return None

# Function to send Discord notification
async def send_discord_notification(message, webhook_url):
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, session=session)
        try:
            # Split message into chunks if it exceeds 2000 characters
            for chunk in [message[i:i+2000] for i in range(0, len(message), 2000)]:
                await webhook.send(content=chunk)
            print("Notification sent to Discord.")
        except discord.errors.HTTPException as e:
            print("Error sending Discord notification:", e)


# Function to check for new rewards and send notifications
async def check_for_new_rewards(previous_rewards, current_rewards, rewards_with_points, webhook_url):
    if current_rewards:
        message = "Currently available rewards:\n"
        for reward in current_rewards:
            message += f"{reward} - {rewards_with_points[reward]} Platinum Points\n"
        await send_discord_notification(message, webhook_url)
        return current_rewards
    else:
        print("No rewards currently available.")
        return previous_rewards

# Function to print available rewards
def print_available_rewards(available_rewards, rewards_with_points):
    print("Available rewards:")
    for reward in available_rewards:
        print(f"- {reward} - {rewards_with_points[reward]} Platinum Points")

# Main function to check rewards availability and send notifications
async def main():
    # Discord Webhook URL
    WEBHOOK_URL = 'https://discord.com/api/webhooks/1225980341303509033/S8P51sbEiu-6XR6PX_kksX6Dl4UFIISrVEH9Dd9jX5DpNaq58-sF7xJgprJWaQwGVgpo'
    
    previous_rewards = []
    rewards_with_points = {}

    # Fetch MyNintendo webpage
    html_content = fetch_my_nintendo_page()
    if html_content:
        # Parse HTML content
        soup = parse_html_content(html_content)
        if soup:
            # Find available rewards and their corresponding platinum points
            rewards = soup.find_all(class_='sc-s17bth-0 bMmuUN sc-w55g5t-0 gSthvS sc-eg7slj-2 iiGOlC')
            points = soup.find_all(class_='sc-1f0n8u6-9 unbAu')
            for reward, point in zip(rewards, points):
                reward_text = reward.text.strip()
                point_text = point.text.strip()
                rewards_with_points[reward_text] = point_text

            available_rewards = list(rewards_with_points.keys())
            # Print available rewards (for testing)
            print_available_rewards(available_rewards, rewards_with_points)
            # Send current rewards on startup
            await check_for_new_rewards(previous_rewards, available_rewards, rewards_with_points, WEBHOOK_URL)
            previous_rewards = available_rewards
        else:
            print("Failed to parse HTML content.")
    else:
        print("Failed to fetch HTML content from MyNintendo webpage.")

    while True:
        # Fetch MyNintendo webpage
        html_content = fetch_my_nintendo_page()
        if html_content:
            # Parse HTML content
            soup = parse_html_content(html_content)
            if soup:
                # Find available rewards and their corresponding platinum points
                rewards = soup.find_all(class_='sc-s17bth-0 bMmuUN sc-w55g5t-0 gSthvS sc-eg7slj-2 iiGOlC')
                points = soup.find_all(class_='sc-1f0n8u6-9 unbAu')
                rewards_with_points = {}
                for reward, point in zip(rewards, points):
                    reward_text = reward.text.strip()
                    point_text = point.text.strip()
                    rewards_with_points[reward_text] = point_text

                available_rewards = list(rewards_with_points.keys())
                # Check for new rewards and send notifications
                previous_rewards = await check_for_new_rewards(previous_rewards, available_rewards, rewards_with_points, WEBHOOK_URL)
            else:
                print("Failed to parse HTML content.")
        else:
            print("Failed to fetch HTML content from MyNintendo webpage.")

        # Wait for a certain period before checking again (e.g., every hour)
        await asyncio.sleep(3600)

# Run the main function
import asyncio
asyncio.run(main())
