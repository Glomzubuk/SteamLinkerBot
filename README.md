# SteamLinkerBot
A Discord bot made in Python that takes a link with a steam header, passes it through the API of Temporary-URL.com, and returns a button that contains the link, allowing the user to click and join a lobby without having to copy paste to their browser.

If you want to create a variant of the bot yourself, you will need a Temporary URL premium account in order to get the keys to use their API. Their API also only allows 30 API calls a minute and 5000 API calls a day, which the code accounts for.

# Usage

![ ](https://github.com/CarterPhan/SteamLinkerBot/tree/main/images/steamlinker.gif)

Simply copy and paste your steam link into any channel that the bot can see, and the bot will put a message underneath with a clickable button!

If you are done with your lobby, feel free to delete the link message. The bot will read this and delete its own message too!

![ ](https://github.com/CarterPhan/SteamLinkerBot/tree/main/images/steamlinkerformat.png)

You can also pass parameters into the bot, anywhere from 1 to 180 for a duration and either **min** or **hr** for the duration type. So, something like "steam://joinlobby/.../..../.... 20 hr" would create a clickable button for a temporary link that lasts 20 hours. This is good for people who have long sets with many people coming in and out, so they can control the time that the link is up for. By default the links are up for 4 hours.

![ ](https://github.com/CarterPhan/SteamLinkerBot/blob/main/images/SteamLinkerFormatting.PNG)

If you want to @ a certain role or something, please do so **AFTER** the link, in your message. The bot will respond to any message that starts with the steam link, but will not detect any message that does not start with said steam link.

# Adding the Bot to your Server:

By default, the bot requires the permissions to Send Messages, Manage Messages, and Embed Links. The Send Messages and Embed Links permission is to send the link into the chat, while the Manage Messages permission is so that the bot can delete its own message once it sees the original message deleted. Outside of that, the bot does nothing more to your messages. If you are still afraid of this however, feel free to modify your channel permissions such that the bot is unable to read or access any channel other than the one that steam links are fed through.
