import discord
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv
import requests
import shutil
from PIL import Image
from pytesseract import image_to_string

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVERTOK = os.getenv('SERVER_ID')

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    # print('Logged in as')
    # print(bot.user.name)
    # print(bot.user.id)
    # print('Invite: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'.format(bot.user.id))
    # print('------')
    for server in bot.guilds:
        if server == SERVERTOK:
            # print(f'{bot.user.name} is connected to the following guild:\n'f'{server.name}(id: {server.id})')
            break
    print(f'{bot.user.name} is connected to the following guild:\n'f'{server.name}(id: {server.id})')

@bot.event
async def on_member_join(member):
    role = get(member.guild.roles, name="just_joined")
    await member.add_roles(role)


@bot.command(name='upload', help='just attach your screenshot')
async def upload(ctx):
    if len(ctx.message.attachments) != 1:
        await ctx.send("make sure you only attach 1 screenshot, try again")
    else:
        attach_url = ctx.message.attachments[0].url
        r = requests.get(attach_url, stream=True)
        if r.status_code == 200:
            with open(f"tmp{ctx.message.id}.jpg", 'wb+') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            
            imgtxt = image_to_string(Image.open(f"tmp{ctx.message.id}.jpg"), lang='eng', config='--psm 11')
            print(imgtxt)
            member = ctx.message.author
            if "ANGELS" in imgtxt.upper():
                role = get(member.guild.roles, name="just_joined")
                await member.remove_roles(role)
                role = get(member.guild.roles, name="Angels")
                await member.add_roles(role)
            elif "DAEMONS" in imgtxt.upper():
                role = get(member.guild.roles, name="just_joined")
                await member.remove_roles(role)
                role = get(member.guild.roles, name="Demons")
                await member.add_roles(role)
            else:
                await ctx.send("IMG PARSE ERROR, ANGEL/DAEMON NOT DETECTED TRY DIFFERENT SCREENSHOT")
            os.remove(f"tmp{ctx.message.id}.jpg")
        else:
            await ctx.send("img get broken, try again")
            return


bot.run(TOKEN)