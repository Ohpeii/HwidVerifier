import discord
import json
import requests
from discord.ext import commands

config = json.load(open("../config.json", "r"))
client = commands.Bot(command_prefix=config["prefix"])
client.remove_command("help")

url =  "http://localhost:" + str(config["port"])

@client.event
async def on_connect():
    print(" User: {}".format(client.user))

@client.command("check")
async def check(ctx: commands.Context, *, message):
    with requests.Session() as req:
       f = req.get( url + f"/api/get/{message}")
       if f.json()["success"] == True:
           await ctx.send("`HWID Is in the database`")
       else:
           await ctx.send("`HWID Is not in the database`")

@client.command('help')
async def help(ctx: commands.Context):
    print(client.user.avatar_url)
    embed = discord.Embed(color=0x00ffff)
    embed.set_image(url=str(client.user.avatar_url))
    embed.add_field(name="hwids", value="`It shows all hwids that are in the database`", inline=False)
    embed.add_field(name="addHwid", value="`Gives you the option to add a hwid into the database`", inline=True)
    embed.add_field(name="removeHwid", value="`Gives you the optiont to a remove a specific hwid from the database`", inline=False)
    embed.add_field(name="check", value="`Allows you to check if a specific hwid is in the database`", inline=True)

    await ctx.send(embed=embed)

@client.command("addHwid")
async def addHwid(ctx: commands.Context, *, message):
    with requests.Session() as req:
        f = req.post(url + f"/api/addHwid/{message}", headers={"Authorization": "AWdhAOwdiaw3146IUHsd"})
        if f.json()["success"] == True:
            await ctx.send("`HWID Is in the database`")
        else:
            await ctx.send("`HWID Is not in the database`")

@client.command("removeHwid")
async def removeHwid(ctx: commands.Context, *, message):
    with requests.Session() as req:
        f = req.post(url + f"/api/removeHwid/{message}", headers={"Authorization": "AWdhAOwdiaw3146IUHsd"})
        if f.json()["success"] == True:
            await ctx.send("`The hwid has been removed.`")
        else:
            await ctx.send("`The Hwid is not in the database`")

@client.command("hwids")
async def hwids(ctx: commands.Context):
     with requests.Session() as req:
          f = req.get( url + f"/api/hwids", headers={"Authorization": "AWdhAOwdiaw3146IUHsd"})

          await ctx.send("```\n" + '\n'.join(f.text.split("\n")) + "```")

if __name__ == "__main__":
    
    if config["selfbot"] == True:
        client.run(config["token"], bot=False, reconnect=True)
    else:
        client.run(config["token"], reconnect=True)
