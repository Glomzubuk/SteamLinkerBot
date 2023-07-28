# SteamLinkerBot
A Discord bot made in Python that takes a link with a steam header, passes it through the API of Temporary-URL.com, and returns a button that contains the link, allowing the user to click and join a lobby without having to copy paste to their browser.

If you are done with your lobby, feel free to delete the link message. The bot will read this and delete its own message too!

The bot will only look for chat messages that only have the lobby link inside. If you want to @ a certain role to let them know about the lobby, you need to send a seperate message containing it.

You need a Temporary URL premium account in order to get the keys to use their API. Their API also only allows 30 API calls a minute and 5000 API calls a day, which the code accounts for.

You can now pass parameters into the bot, anywhere from 1 to 180 for a duration and either min or hr for the duration type. So, something like "steam://joinlobby/.../..../.... 20 hr" would create a clickable button for a temporary link that lasts 20 hours. This is good for people who have long sets with many people coming in and out, so they can control the time that the link is up for. By default the links are up for 1 hour.

By default, the bot requires the permissions to Send Messages, Manage Messages, and Embed Links. The Send Messages and Embed Links permission is to send the link into the chat, while the Manage Messages permission is so that the bot can delete its own message once it sees the original message deleted. Outside of that, the bot does nothing more to your messages. If you are still afraid of this however, feel free to modify your channel permissions such that the bot is unable to read or access any channel other than the one that steam links are fed through.
