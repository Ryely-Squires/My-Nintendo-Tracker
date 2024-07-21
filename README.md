# MyNintendo Tracker!
![usethisfinalmynintendomaybe](https://github.com/Ryely-Squires/My-Nintendo-Tracker/assets/95175586/b1e895ec-752e-444b-a9aa-681e27439757)
(font from https://www.textstudio.com)
# Why'd I make this?

This is a test of my python web scraping utilities! MyNintendo is a service I use frequently, so I thought I'd develop a tracker! There is one currently,
but it lacks discord webhook integration, which is something I value.
Luckily, Nintendo conveniently stores all platinum point values and reward names in specific classes on the HTML, so scraping all of them is a snap!

# Notice

This script is for Canadian and American MyNintendo users only. Other regions are not supported at this time, but will probably be added eventually. I'm going to say the script runs pretty perfectly now! No issues, and I've done lots of testing (even mirrored the webpage and added test rewards).

I'm not responsible for any damage your system incurs (running a web scraping .py file...?) with use of this script. This is my first real project, so I have no idea how conventions work concerning code in github and whatnot.
Portions of this code are also made with AI...you can probably tell which ones.  

Note, remember .json functionality. The file should only have [] on first run. If it does not, add it. If the file does not exist, the script will create one and populate it anyway.

# Guide for Regular Use(ADDING FULLY SOON!)
1. Download the source code. A proper release will be made when the project fully functions, but for now, just do that.

2. Extract the source code, and navigate into the project folder. Enter the terminal.

3. Use command "pip install -r requirements.txt" to install all the necessary dependencies. Make sure you have the necessary privileges.

4. Enter the mynintendo.py file's code with your favourite text editor. Look for the URL field near the top of the code, and paste the URL of your country's rewards page. For convenience, the two URLs are available in
comments.

5. Find the "PathToDriver" line. Now, copy a version of chromedriver that matches your browser's version. You can find chromedrivers at (https://googlechromelabs.github.io/chrome-for-testing/). Once downloaded, place it in the directory where the script is located. For example, "C:\Users\User\Documents\My-Nintendo-Tracker-main\My-Nintendo-Tracker-main\chromedriver.exe".

6. Find the "# Discord Webhook URL" line. Now, navigate to a server you have admin permissions on discord. Right click on the channel,
click "edit channel", navigate to "integrations" on the left side menu, and click webhooks. Create a webhook, edit it as you'd like, and copy its URL.
Paste the URL in the URL field within the .py file.

7. Run the script! You should get a list on startup detailing available rewards, and from then on, every hour, it'll send a notification if it finds a new reward, along with a then updated list of rewards.
The logic to remember what is previously available is stored in the previous_rewards.json file, with logs available when notifications are sent.

# Docker

Want to use Docker? Supported!

1. Download the Docker branch source code. A proper release will be made when the project fully functions, but for now, just do that.

2. Extract the files and enter the project folder.

3. Navigate to a server you have admin permissions on discord. Right click on the channel,
click "edit channel", navigate to "integrations" on the left side menu, and click webhooks. Create a webhook, edit it as you'd like (might I suggest the provided profile picture?), and copy its URL.

4. In the docker-compose.yml file, place your webhook and region URL.

5. Build the image using the provided dockerfile. For default, the command is "docker build -t mynintendo-tracker .".

6. Launch the container! Run it detached..."docker compose up -d".

7. Should you need to access the logs, run "docker logs mynintendo".

# TODO 
1. Add multi region support (Only supports CA and US right now).
2. Clean up the code. It's a little ugly at the moment.
3. Scrape image URLs so you can see the actual reward when a new one comes out.

