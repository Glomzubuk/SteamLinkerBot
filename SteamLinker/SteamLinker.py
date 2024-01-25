import discord
from discord.ext import commands
import re
import config
import urllib.parse

# Discord Bot Token
bot_token = config.BOT_TOKEN

# Define the intents your bot requires
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Function to create a redirection URL
def create_redirection_url(url):
    try:
        # Encode the URL to make it safe for inclusion in the query string
        encoded_url = urllib.parse.quote(url, safe='')

        # Construct the redirection URL
        redirection_url = f"https://carterphan.github.io/UrlRedirector/?url={encoded_url}"

        return redirection_url
    except Exception as e:
        print(f"Error creating redirection URL: {str(e)}")
        return None

# Create the bot with the specified intents and a command prefix of your choice (e.g., ! or ?)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Dictionary to store the message data for the bot's messages
stored_messages = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Regular expression pattern to match a steam link with optional duration value and duration type
    steam_link_pattern = re.compile(r'(?:.*?steam:\/\/joinlobby\/\d+\/\d+\/\d+.*?)(?:<@&\d+>)?', re.IGNORECASE)
    match = steam_link_pattern.search(message.content)

    if match:
        # Get the steam link
        steam_link = match.group(0)

        # Create a clickable button
        redirection_url = create_redirection_url(steam_link)

        if redirection_url:
            class ButtonView(discord.ui.View):
                def __init__(self, link: str):
                    super().__init__()
                    self.link = link
                    self.add_item(discord.ui.Button(label='Click Here to Join the Lobby!', url=self.link))

            sent_message = await message.channel.send("*Click the button below to access the lobby!*", view=ButtonView(redirection_url))
            await message.delete()

            # Store the original author ID and the bot's message ID for later reference
            message_data = {
                'original_author_id': message.author.id,
                'bot_message_id': sent_message.id
            }
            # Save the message_data dictionary using the bot's message ID as the key
            stored_messages[message.id] = message_data
        else:
            await message.channel.send(f"Sorry, an error occurred while creating the redirection URL.")
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    # Check if the deleted message's ID matches any bot message in stored_messages
    if message.id in stored_messages:
        # Get the message_data for the bot's message that corresponds to the deleted message
        message_data = stored_messages[message.id]

        bot_message = await message.channel.fetch_message(message_data['bot_message_id'])
        await bot_message.delete()

        # Remove the message_data from stored_messages
        del stored_messages[message.id]

# Run the bot with the provided token
bot.run(bot_token)
