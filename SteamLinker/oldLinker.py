import discord
from discord.ext import commands
import re
import requests
import json
import hashlib
import hmac
import config
import time
from datetime import datetime, timedelta


# Discord Bot Token
bot_token = config.BOT_TOKEN

# Define the intents your bot requires
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Define the API rate limits
MAX_CALLS_PER_MINUTE = 30
CALLS_RESET_INTERVAL = 60  # 60 seconds (1 minute)
MAX_CALLS_PER_DAY = 5000

# Token bucket variables
tokens = MAX_CALLS_PER_MINUTE
last_refill_time = time.time()

# Daily API call counter variables
total_calls_today = 0
today = datetime.utcnow().date()

# TempURL API Keys
TEMPURL_PUBLIC_KEY = config.TEMPURL_PUBLIC_KEY
TEMPURL_PRIVATE_KEY = config.TEMPURL_PRIVATE_KEY
TEMPURL_API_URL = 'https://www.temporary-url.com/api/v1/'

# Function to convert the specified amount and time unit to an epoch Unix timestamp
def parse_time_to_epoch(amount, time_unit):
    time_unit = time_unit.lower()

    if time_unit not in ("min", "hr"):
        raise ValueError("Invalid time unit. Please use 'min' or 'hr'.")

    # Convert the time unit to minutes
    if time_unit == "hr":
        amount *= 60

    # Calculate the epoch Unix timestamp for the specified time from now
    timestamp = int(time.time()) + amount * 60

    return timestamp

def refill_tokens():
    global tokens, last_refill_time
    now = time.time()
    time_since_last_refill = now - last_refill_time

    if time_since_last_refill >= CALLS_RESET_INTERVAL:
        tokens = MAX_CALLS_PER_MINUTE
        last_refill_time = now

def shorten_url(url, duration, duration_type):
    global tokens, total_calls_today, today

    if tokens <= 0:
        refill_tokens()
        print("Minute API call limit exceeded. Try again in a minute.")
        return "Minute API call limit exceeded. Try again in a minute."

    # Check if it's a new day and reset the call count
    current_date = datetime.utcnow().date()
    if current_date != today:
        today = current_date
        total_calls_today = 0

    if total_calls_today >= MAX_CALLS_PER_DAY:
        print("Daily API call limit exceeded. Try again in a day.")
        return "Daily API call limit exceeded. Try again in a day."

    data = {
        'type': 'URL',
        'targetURL': url,
        'expirationType': 'duration',
        'duration': duration,
        'durationType': duration_type
    }

    data_json = json.dumps(data)
    ENCODE_PRIVATE_KEY = TEMPURL_PRIVATE_KEY.encode()
    encode_data = data_json.encode()
    hash_value = hmac.new(ENCODE_PRIVATE_KEY, encode_data, hashlib.sha256).hexdigest()

    headers = {
        'X-Auth': TEMPURL_PUBLIC_KEY,
        'X-Auth-Hash': hash_value
    }

    response = requests.post(TEMPURL_API_URL, data=data_json, headers=headers)
    if response.status_code == 200:
        result = response.json()
        tokens -= 1  # Consume a token for the API call
        total_calls_today += 1
        print(total_calls_today)
        return "https://www.temporary-url.com/" + result['shortArray'][0] if 'shortArray' in result else None
    else:
        print(f"API request failed with status code {response.status_code}")
        print(response)
        return None

# Create the bot with the specified intents and a command prefix of your choice (e.g., ! or ?)
bot = commands.Bot(command_prefix='!', intents = intents)

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
    steam_link_pattern = re.compile(r'^steam:\/\/joinlobby\/\d+\/\d+\/\d+(?:\s+(\d+)\s*(\w+))?', re.IGNORECASE)
    match = steam_link_pattern.match(message.content)

    if match:
        # Extract the duration and duration type from the match
        duration = int(match.group(1)) if match.group(1) else 60
        duration_type = match.group(2).lower() if match.group(2) else "min"

        print (duration_type)

        # Validate duration type
        valid_duration_types = ["min", "hr"]
        if duration_type not in valid_duration_types:
            sent_message = await message.channel.send(f"Invalid duration type. Please use one of the following: {', '.join(valid_duration_types)}.")
            # Store the original author ID and the bot's message ID for later reference
            message_data = {
                'original_author_id': message.author.id,
                'bot_message_id': sent_message.id
            }
            # Save the message_data dictionary using the bot's message ID as the key
            stored_messages[message.id] = message_data
            await bot.process_commands(message)
            return
        elif duration_type == "min":
            duration_type_api = "MINUTE"
        elif duration_type == "hr":
            duration_type_api = "HOUR"
            
        
        # Validate duration range (1 to 180 minutes)
        if not 1 <= duration <= 180:
            sent_message = await message.channel.send("Invalid duration. Please enter a value between 1 and 180.")
            # Store the original author ID and the bot's message ID for later reference
            message_data = {
                'original_author_id': message.author.id,
                'bot_message_id': sent_message.id
            }
            # Save the message_data dictionary using the bot's message ID as the key
            stored_messages[message.id] = message_data
            await bot.process_commands(message)
            return

        # Get the steam link
        steam_link = message.content.split(' ')[0]

        # Call the shorten_url function with the steam link and duration
        shortened_url = shorten_url(steam_link, duration, duration_type_api)

        if "Daily API call limit exceeded" in shortened_url:
            sent_message = await message.channel.send("Sorry, the daily API call limit has been exceeded. Try again in a day.")
            # Store the original author ID and the bot's message ID for later reference
            message_data = {
                'original_author_id': message.author.id,
                'bot_message_id': sent_message.id
            }
            # Save the message_data dictionary using the bot's message ID as the key
            stored_messages[message.id] = message_data
            await bot.process_commands(message)
            return
            
        elif "Minute API call limit exceeded" in shortened_url:
            sent_message = await message.channel.send("Sorry, the minute API call limit has been exceeded. Try again in a minute.")
            # Store the original author ID and the bot's message ID for later reference
            message_data = {
                'original_author_id': message.author.id,
                'bot_message_id': sent_message.id
            }
            # Save the message_data dictionary using the bot's message ID as the key
            stored_messages[message.id] = message_data
            await bot.process_commands(message)
            return

        elif shortened_url:
            # Sets the Expiration time to the time given to the API
            expirationTime = parse_time_to_epoch(duration, duration_type)

            # Create a clickable button
            class ButtonView(discord.ui.View):
                def __init__(self, link: str):
                    super().__init__()
                    self.link = link
                    self.add_item(discord.ui.Button(label='Click Here to Join the Lobby!', url=self.link))
            sent_message = await message.channel.send("*This is a temporary link. It will expire <t:" + str(expirationTime) + ":R>*", view=ButtonView((str(shortened_url))))
            
            # Store the original author ID and the bot's message ID for later reference
            message_data = {
                'original_author_id': message.author.id,
                'bot_message_id': sent_message.id
            }
            # Save the message_data dictionary using the bot's message ID as the key
            stored_messages[message.id] = message_data
            
        else:
            await message.channel.send(f"Sorry, couldn't create a shortened link for {message.content}")

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
