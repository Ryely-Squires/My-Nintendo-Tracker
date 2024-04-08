import requests
from bs4 import BeautifulSoup
import discord
import time
import aiohttp
import json
import asyncio
from datetime import datetime

# Function to fetch MyNintendo webpage
def fetch_my_nintendo_page():
    url = 'https://www.nintendo.com/en-ca/store/exclusives/rewards/'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            log_message = f"[{datetime.now()}] Failed to fetch MyNintendo webpage. Status code: {response.status_code}\n"
            print(log_message, end='')  # Print to console
            log_to_file(log_message)
            return None
    except requests.RequestException as e:
        log_message = f"[{datetime.now()}] Error fetching MyNintendo webpage: {e}\n"
        print(log_message, end='')  # Print to console
        log_to_file(log_message)
        return None

# Function to send Discord notification
async def send_discord_notification(message, webhook_url):
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, session=session)
        try:
            # Initialize chunk list
            message_chunks = []

            # Split message into chunks if it exceeds 2000 characters
            current_chunk = ''
            for line in message.split('\n'):
                if len(current_chunk + line) <= 2000:
                    current_chunk += line + '\n'
                else:
                    # Add current chunk to list
                    message_chunks.append(current_chunk)
                    # Start new chunk with current line
                    current_chunk = line + '\n'
            # Add last chunk to list
            message_chunks.append(current_chunk)

            # Send each chunk separately
            for chunk in message_chunks:
                await webhook.send(content=chunk)

            log_message = f"[{datetime.now()}] Notification sent to Discord.\n"
            print(log_message, end='')  # Print to console
            log_to_file(log_message)
        except discord.errors.HTTPException as e:
            log_message = f"[{datetime.now()}] Error sending Discord notification: {e}\n"
            print(log_message, end='')  # Print to console
            log_to_file(log_message)

# Function to check for new rewards and send notifications
async def check_for_new_rewards(previous_rewards, current_rewards, rewards_with_points, webhook_url, initial_run=False):
    if current_rewards:
        new_rewards = []
        removed_rewards = []

        # Compare current rewards with previous rewards
        for reward in current_rewards:
            if reward not in previous_rewards:
                new_rewards.append(reward)
        
        for reward in previous_rewards:
            if reward not in current_rewards:
                removed_rewards.append(reward)

        if new_rewards and not initial_run:
            message = ""
            for reward in new_rewards:
                message += f"New reward available! {reward} - {rewards_with_points[reward]} Platinum Points\n"
            await send_discord_notification(message, webhook_url)
            return current_rewards
        elif removed_rewards and not initial_run:
            message = ""
            for reward in removed_rewards:
                message += f"Reward removed: {reward}\n"
            await send_discord_notification(message, webhook_url)
            return current_rewards
        elif not initial_run:
            return previous_rewards
    else:
        log_message = f"[{datetime.now()}] No rewards currently available.\n"
        print(log_message, end='')
        log_to_file(log_message)
        return previous_rewards

# Function to print available rewards
def print_available_rewards(available_rewards, rewards_with_points):
    print("Available rewards:")
    for reward in available_rewards:
        print(f"- {reward} - {rewards_with_points[reward]} Platinum Points")

# Function to log messages to file
def log_to_file(message):
    with open('logs.txt', 'a') as f:
        f.write(message)

# Main function to check rewards availability and send notifications
async def main():
    # Discord Webhook URL
    WEBHOOK_URL = 'https://discord.com/api/webhooks/1225980341303509033/S8P51sbEiu-6XR6PX_kksX6Dl4UFIISrVEH9Dd9jX5DpNaq58-sF7xJgprJWaQwGVgpo'
    
    # JSON file to store previous rewards
    previous_rewards_file = 'previous_rewards.json'
    
    previous_rewards = []

    # Fetch MyNintendo webpage
    html_content = fetch_my_nintendo_page()
    if html_content:
        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
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
            # Print available rewards (for testing)
            print_available_rewards(available_rewards, rewards_with_points)
            # Send current rewards on startup
            message = "Thanks for using my script! Available rewards:\n"
            for reward in available_rewards:
                message += f"- {reward} - {rewards_with_points[reward]} Platinum Points\n"
            await send_discord_notification(message, WEBHOOK_URL)
            previous_rewards = available_rewards
        else:
            log_message = f"[{datetime.now()}] Failed to parse HTML content.\n"
            print(log_message, end='')  # Print to console
            log_to_file(log_message)
    else:
        log_message = f"[{datetime.now()}] Failed to fetch HTML content from MyNintendo webpage.\n"
        print(log_message, end='')  # Print to console
        log_to_file(log_message)

    while True:
        # Fetch MyNintendo webpage
        html_content = fetch_my_nintendo_page()
        if html_content:
            # Parse HTML content
            soup = BeautifulSoup(html_content, 'html.parser')
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
                
                # Write current rewards to the JSON file
                with open(previous_rewards_file, 'w') as f:
                    json.dump(previous_rewards, f)
            else:
                log_message = f"[{datetime.now()}] Failed to parse HTML content.\n"
                print(log_message, end='')  # Print to console
                log_to_file(log_message)
        else:
            log_message = f"[{datetime.now()}] Failed to fetch HTML content from MyNintendo webpage.\n"
            print(log_message, end='')  # Print to console
            log_to_file(log_message)

        # Wait for a certain period before checking again (e.g., every hour)
        await asyncio.sleep(3600)

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())

