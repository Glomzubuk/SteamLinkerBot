# SteamLinkerBot
A Discord bot made in Python that takes a link with a steam header, passes it through the API of Temporary-URL.com, and returns a button that contains the link, allowing the user to click and join a lobby without having to copy paste to their browser.

You need a Temporary URL premium account in order to get the keys to use their API. Their API also only allows 30 API calls a minute and 5000 API calls a day, which the code accounts for.

You can now pass parameters into the bot, anywhere from 1 to 180 for a duration and either min or hr for the duration type. So, something like "steam://joinlobby/.../..../.... 20 hr" would create a clickable button for a temporary link that lasts 20 hours. This is good for people who have long sets with many people coming in and out, so they can control the time that the link is up for. By default the links are up for 15 minutes.
