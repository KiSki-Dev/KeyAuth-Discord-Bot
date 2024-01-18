# CODE WRITTEN BY KiSki-Dev : https://github.com/KiSki-Dev

import discord
from discord import app_commands
import requests
import math
import datetime

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# Configuration
discord_token = ""
# KeyAuth
name = ""
owner_id = ""
sellerkey = ""
# Discord
log_id = 123
allowed_id = 123
customer_id = 123
guild_id = 123



@tree.command(
    name="register",
    description="Create your Account using your License.",
    guild=discord.Object(id=guild_id)
)
async def register_command(interaction, username: str, password: str, license: str):
    await interaction.response.send_message(embed=discord.Embed(title="Registration is currently in progress...", color=0xff9600), ephemeral=True)

    if interaction.channel.id == allowed_id:
        url = f"https://keyauth.win/api/1.2/?type=init&ver=1.0&name={name}&ownerid={owner_id}"
        response = requests.post(url)
        data = response.json()
        session_id = data.get("sessionid")

        url = f"https://keyauth.win/api/1.2/?type=register&username={username}&pass={password}&key={license}&sessionid={session_id}&name={name}&ownerid={owner_id}&email=email"
        response = requests.post(url)
        data = response.json()
        status = data["success"]

        if status == True:
            disc_id = interaction.user.id
            url = f"https://keyauth.win/api/seller/?sellerkey={sellerkey}&type=setvar&user={username}&var=DicordID&data={disc_id}"
            response = requests.post(url)

            dur_seconds = data["info"]["subscriptions"][0]["timeleft"]
            dur_days = dur_seconds / 86400
            rounded_dur_days = math.ceil(dur_days)
            dur_str = str(rounded_dur_days)

            log_channel = await interaction.guild.fetch_channel(log_id)

            embedComp=discord.Embed(title="Registration completed!", color=0x00ff00)
            embedComp.add_field(name="Username", value=username, inline=True)
            embedComp.add_field(name="Password", value=password, inline=True)
            embedComp.add_field(name="License", value=license, inline=False)
            embedComp.add_field(name="Duration", value=f"{dur_str} Days", inline=False)
            embedComp.set_footer(text="Made by KiSki-Dev with ❤")
            await interaction.followup.send(embed=embedComp, ephemeral=True)

            embedLog=discord.Embed(title="Registration made!", color=0x00aaff)
            embedLog.timestamp = datetime.datetime.now(datetime.UTC)
            embedLog.add_field(name="Username", value=username, inline=True)
            embedLog.add_field(name="Discord", value=f"<@{disc_id}>", inline=True)
            embedLog.add_field(name="License", value=license, inline=False)
            embedLog.add_field(name="Duration", value=f"{dur_str} Days", inline=False)

            await log_channel.send(embed=embedLog)

            role = interaction.guild.get_role(customer_id)
            await interaction.user.add_roles(role)

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
            elif "taken" in error_msg:
                embedErr=discord.Embed(title="Registration failed!", color=0xff0000)
                embedErr.add_field(name="Error:", value="This Username is already taken.", inline=True)
                await interaction.followup.send(embed=embedErr, ephemeral=True)
            elif "Session" in error_msg:
                embedErr=discord.Embed(title="Registration failed!", color=0xff0000)
                embedErr.add_field(name="Error:", value="Please try again later.", inline=True)
                await interaction.followup.send(embed=embedErr, ephemeral=True)
            elif "short" in error_msg:
                embedErr=discord.Embed(title="Registration failed!", color=0xff0000)
                embedErr.add_field(name="Error:", value="Username too short.", inline=True)
                await interaction.followup.send(embed=embedErr, ephemeral=True)
            else:
                embedErr=discord.Embed(title="Registration failed!", color=0xff0000)
                embedErr.add_field(name="Error:", value="Unkown Error happend. Please contact the [Developer](https://github.com/KiSki-Dev)", inline=True)
                await interaction.followup.send(embed=embedErr, ephemeral=True)
        else:
                embedErr=discord.Embed(title="Registration failed!", color=0xff0000)
                embedErr.add_field(name="Error:", value="Server Error. Please try again later.", inline=True)
                await interaction.followup.send(embed=embedErr, ephemeral=True)
    else:
        embedErr=discord.Embed(title="Wrong Channel!", color=0xff0000)
        embedErr.add_field(name="Please use the correct Channel.", value=f"Please use it in <#{allowed_id}>", inline=True)
        await interaction.followup.send(embed=embedErr, ephemeral=True)


@tree.command(
    name="status",
    description="Get the Status of the Cheats.",
    guild=discord.Object(id=guild_id)
)
@app_commands.choices(choices=[
    app_commands.Choice(name="All", value="all"),
    app_commands.Choice(name="Auth", value="Auth"),
    app_commands.Choice(name="CS2", value="CS2"),
    app_commands.Choice(name="Fortnite", value="Fortnite"),])
async def status_command(interaction, choices: app_commands.Choice[str]):        
    await interaction.response.send_message(embed=discord.Embed(title="Recieving Status is currently in progress...", color=0xff9600), ephemeral=True)
    await client.change_presence(activity=discord.Game(name="github.com/KiSki-Dev"))

    choice = choices.value

    a_state, a_full_state, a_color = status("Auth")
    cs_state, cs_full_state, cs_color = status("CS2")
    fn_state, fn_full_state, fn_color = status("Fortnite")

    if choice == "all":
        embedComp=discord.Embed(title="All Statuses!", color=0x0000ff)
        embedComp.add_field(name="Auth", value=a_state, inline=False)
        embedComp.add_field(name="CS2", value=cs_state, inline=False)
        embedComp.add_field(name="Fortnite", value=fn_state, inline=False)

        await interaction.followup.send(embed=embedComp, ephemeral=True)
    elif choice == "Auth":
            embedComp=discord.Embed(title=a_full_state, color=a_color)
            await interaction.followup.send(embed=embedComp, ephemeral=True)
    elif choice == "CS2":
        embedComp=discord.Embed(title=cs_full_state, color=cs_color)
        await interaction.followup.send(embed=embedComp, ephemeral=True)
    elif choice == "Fortnite":
        embedComp=discord.Embed(title=fn_full_state, color=fn_color)
        await interaction.followup.send(embed=embedComp, ephemeral=True)


def status(program):
    p = program.lower()
    url = f"http://37.221.92.85:1337/status/get/{p}"
    response = requests.get(url)
    data = response.json()

    status = data["status"]

    if status.lower() == "detected":
        full_state = f"🔴 : {program} is Detected. Be careful."
        state = "🔴 : Detected"
        color = 0xff0000
    elif status.lower() == "undetected":
        full_state = f"🟢 : {program} is Undetected."
        state = "🟢 : Undetected"
        color = 0x00ff00
    elif status.lower() == "online":
        full_state = f"🟢 : {program} is currently Online."
        state = "🟢 : Online"
        color = 0x00ff00
    elif status.lower() == "offline":
        full_state = f"🔴 : {program} is currently offline."
        state = "🔴 : Offline"
        color = 0xff0000
    elif status.lower() == "testing":
        full_state = f"🟠 : We are Testing {program} at the moment."
        state = "🟠 : Testing"
        color = 0xff6400
    elif status.lower() == "updating":
        full_state = f"🟠 : We are Updating {program} at the moment."
        state = "🟠 : Updating"
        color = 0xff6400
    elif status.lower() == "unkown":
        full_state = f"🟠 : We are checking the Status of {program} at the moment."
        color = 0xff6400
    else:
        full_state = f"🔴 : A Error happend while recieving the Status of {program}."
        state = "🔴 : Unkown"
        color = 0xff0000

    return state, full_state, color



embedRegister=discord.Embed(title="Help - Register", color=0x009dff)
embedRegister.add_field(name="Create a Account", value="using the Register Command.", inline=False)
embedRegister.add_field(name="Requirements:", value="Unique Username, Good Password, Working License", inline=False)
embedRegister.add_field(name="Instructions", value='Write "**/register**". You should get a Suggestion for the Command. Enter your desired Username, then enter a strong Password. Now you enter your bought License-Key.', inline=False)
embedRegister.add_field(name="Lost Login Data?", value="If you lost any Login-Data or you want to reset your HWID, then contact our Support. We can proof that you actually own a Account.", inline=True)
embedStatus=discord.Embed(title="Help - Status", color=0xff00d0)
embedStatus.add_field(name="Get the Status", value="using the Status Command.", inline=False)
embedStatus.add_field(name="You cant login? Or the Cheat doesnt work?", value="Then you should run the Status Command. Using the Status Command you can see what in our System works and what does not.", inline=False)
embedMore=discord.Embed(title="Help - More", color=0xff9600)
embedMore.add_field(name="Any Other Informations", value="you can see here.", inline=False)
embedMore.add_field(name="Found a Bug?", value='If you found a Bug please directly report it to the Support or the [Bot Developer "KiSki-Dev"](https://github.com/KiSki-Dev).', inline=False)
embedMore.add_field(name="Like the Bot?", value='If you like the Bot, the Bot-Developer "KiSki-Dev" would really appreciate, if you check out his [GitHub](https://github.com/KiSki-Dev).', inline=False)
embedMore.add_field(name="Missing some Features?", value="We are working to constantly adding and upgrading Features. If you miss any Feature, contact the Support and tell them your Idea.", inline=False)

@tree.command(
    name="help",
    description="List all Commands.",
    guild=discord.Object(id=guild_id))
async def help_command(interaction):        
    await interaction.response.send_message(embed=embedRegister, ephemeral=True)
    await interaction.followup.send(embed=embedStatus, ephemeral=True)
    await interaction.followup.send(embed=embedMore, ephemeral=True)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id))
    print("Bot is ready!")

client.run(discord_token)