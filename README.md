# MyNintendo Tracker!
![MyNintendoTracker](https://github.com/Ryely-Squires/My-Nintendo-Tracker/assets/95175586/02def791-a64f-4559-bc05-6db5c25aa13f)
# Why'd I make this?

This is a test of my python web scraping utilities! MyNintendo is a service I use frequently, so I thought I'd develop a tracker! There is one currently,
but it lacks discord webhook integration, which is something I value.
Luckily, Nintendo conveniently stores all platinum point values and reward names in specific classes on the HTML, so scraping all of them is a snap!

# Disclaimer

This script is for Canadian MyNintendo users only. Other regions are not supported at this time, but will probably be added eventually. And as of this initial commit, the script is not currently working (needs some tweaks),
but can indeed give you a list of available rewards on startup!

I'm not responsible for any damage your system incurs (running a web scraping .py file...?) with use of this script. This is my first real project, so I have no idea how conventions work concerning code in github and whatnot.
Portions of this code are also made with AI...you can probably tell which ones.  

Note, remember .json functionality. The file should only have [] on first run. If it does not, or you lack the file for some reason, the script will create one and populate it anyway.

# Guide (ADDING FULLY SOON!)
1. Download the source code. A proper release will be made when the project fully functions, but for now, just do that.

2. Extract the source code, and navigate into the project folder. Enter the terminal.

3. Use command "pip install -r requirements.txt" to install all the necessary dependencies. Make sure you have the necessary privileges.

4. Enter the mynintendo.py file, and find the " # Discord Webhook URL" line. Now, navigate to a server you have admin permissions on discord. Right click on the channel,
click "edit channel", navigate to "integrations" on the left side menu, and click webhooks. Create a webhook, edit it as you'd like, and copy it's URL.
Paste the URL in the URL field within the .py file.

5. Run the script! You should get a list on startup detailing available rewards, and from then on, every hour, it'll send a notification if it finds a new reward, along with a then updated list of rewards.
The logic to remember what is previously available is stored in the previous_rewards.json file, with logs available when notifications are sent.

# TODO 

1. Make sure the thing actually works (probably pretty high priority).
2. Add multi region support.
3. Add docker method (in compose).
4. Clean up the code. It's a little ugly at the moment.
