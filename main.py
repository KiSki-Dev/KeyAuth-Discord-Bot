import discord
from discord import app_commands
import requests
import math

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

discord_token = ""
name = ""
ownerid = ""

@tree.command(
    name="register",
    description="Create your Account using your License.",
    guild=discord.Object(id=1171187810162716673)
)
async def register_command(interaction, username: str, password: str, license: str):
    await interaction.response.send_message(embed=discord.Embed(title="Registration is currently in progress...", color=0xff9600), ephemeral=True)

    url = "https://keyauth.win/api/1.2/?type=init&ver=1.0&name={name}&ownerid={ownerid}"
    response = requests.post(url)
    data = response.json()
    session_id = data.get("sessionid")

    url = f"https://keyauth.win/api/1.2/?type=register&username={username}&pass={password}&key={license}&sessionid={session_id}&name={name}&ownerid={ownerid}&email=email"
    response = requests.post(url)
    data = response.json()
    status = data["success"]
    print(status)
    print(response.text)

    if status == True:
        dur_seconds = data["info"]["subscriptions"][0]["timeleft"]
        dur_days = dur_seconds / 86400
        rounded_dur_days = math.ceil(dur_days)
        dur_str = str(rounded_dur_days)

        embedComp=discord.Embed(title="Registration completed!", color=0x00ff00)
        embedComp.add_field(name="Username", value=username, inline=True)
        embedComp.add_field(name="Password", value=password, inline=True)
        embedComp.add_field(name="License", value=license, inline=False)
        embedComp.add_field(name="Duration", value=f"{dur_str} Days", inline=False)

        await interaction.followup.send(embed=embedComp, ephemeral=True)
    elif status == False:
        error = data["message"]
        error_msg = str(error)

        if "License" in error_msg:
            embedErr=discord.Embed(title="Registration failed!", color=0xff0000)
            embedErr.add_field(name="Error:", value="This License has been already used.", inline=True)
            await interaction.followup.send(embed=embedErr, ephemeral=True)
        elif "password" in error_msg:
            embedErr=discord.Embed(title="Registration failed!", color=0xff0000)
            embedErr.add_field(name="Error:", value="This Password is too bad. Please choose another one.", inline=True)
            await interaction.followup.send(embed=embedErr, ephemeral=True)
        elif "Username" in error_msg:
            embedErr=discord.Embed(title="Registration failed!", color=0xff0000)
            embedErr.add_field(name="Error:", value="This Username is already taken.", inline=True)
            await interaction.followup.send(embed=embedErr, ephemeral=True)
        elif "Session" in error_msg:
            embedErr=discord.Embed(title="Registration failed!", color=0xff0000)
            embedErr.add_field(name="Error:", value="Please try again later.", inline=True)
            await interaction.followup.send(embed=embedErr, ephemeral=True)
        else:
            embedErr=discord.Embed(title="Registration failed!", color=0xff0000)
            embedErr.add_field(name="Error:", value="Unkown Error happend. Please contact the [Developer](https://github.com/KiSki-Dev)", inline=True)
            await interaction.followup.send(embed=embedErr, ephemeral=True)
    else:
            embedErr=discord.Embed(title="Registration failed!", color=0xff0000)
            embedErr.add_field(name="Error:", value="Server Error. Please try again later.", inline=True)
            await interaction.followup.send(embed=embedErr, ephemeral=True)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1171187810162716673))
    print("Bot is ready!")

client.run(discord_token)