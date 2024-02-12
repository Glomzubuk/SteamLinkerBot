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

    steam_link_pattern = re.compile(r'(?:steam:\/\/joinlobby\/\d+\/\d+\/\d+)', re.IGNORECASE)
    userping_pattern = re.compile(r'(?:<@\d+>)', re.IGNORECASE)
    steam_match = steam_link_pattern.search(message.content)
    userping_match = userping_pattern.search(message.content)

    if steam_match:
        steam_link = steam_match.group(0)
        redirection_url = create_redirection_url(steam_link)
        no_link = re.sub(steam_match.group(0), "", message.content)
        if userping_match != None:
            no_ping = re.sub(userping_match.group(0), "", no_link)
            extra_text = re.sub("  ", " ", no_ping)
        else:
            extra_text = re.sub("  ", " ", no_link)

        if redirection_url:
            author_name = message.author.display_name if message.author.display_name else message.author.name
            response  = f"*{author_name} has created a steam lobby link"
            response += "!*\n"
            # if not extra_text.isspace():
            #     response += f"With additional text: *{extra_text.strip()}*\n"
            response += f"[{steam_link}]({redirection_url})"

            sent = await message.channel.send(response, view=ButtonView(redirection_url))

            await message.delete()

            if userping_match != None:
                response  = f"*{author_name} has created a steam lobby link"
                response += f" for {userping_match.group(0)}"
                response += "!*\n"
                # if not extra_text.isspace():
                #     response += f"With additional text: *{extra_text.strip()}*\n"
                response += f"[{steam_link}]({redirection_url})"
                await sent.edit(content=response, view=ButtonView(redirection_url))

        else: await message.channel.send(f"Sorry, an error occurred while creating the redirection URL.")
    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


bot.run(bot_token)
