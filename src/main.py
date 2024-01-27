import discord
from discord.ext import commands
import re
import config
import urllib.parse

bot_token = config.BOT_TOKEN

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


class ButtonView(discord.ui.View):
    def __init__(self, link: str):
        super().__init__()
        self.link = link
        self.add_item(discord.ui.Button(label='Click here to join the lobby!', url=self.link))


def create_redirection_url(url):
    try:
        encoded_url = urllib.parse.quote(url, safe='')
        return f"https://carterphan.github.io/UrlRedirector/?url={encoded_url}"
    except Exception as e:
        print(f"Error creating redirection URL: {str(e)}")
        return None


@bot.event
async def on_message(message):
    if message.author.bot: return

    steam_link_pattern = re.compile(r'(?:.*?steam:\/\/joinlobby\/\d+\/\d+\/\d+.*?)(?:<@&\d+>)?', re.IGNORECASE)
    match = steam_link_pattern.search(message.content)

    if match:
        steam_link = match.group(0)
        redirection_url = create_redirection_url(steam_link)

        if redirection_url:
            #await message.channel.send(f"{message.author.nick}: {message.content}", view=ButtonView(redirection_url))
            author_name = message.author.nick if message.author.nick else message.author.name
            await message.channel.send(f"*{author_name} has created a steam lobby link!*\n[{steam_link}]({redirection_url})", view=ButtonView(redirection_url))

            await message.delete()
        else: await message.channel.send(f"Sorry, an error occurred while creating the redirection URL.")
    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


bot.run(bot_token)
