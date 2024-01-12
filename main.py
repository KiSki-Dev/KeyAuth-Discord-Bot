import discord
from discord import app_commands
import requests
import math

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

discord_token = ""
name = ""
owner_id = ""

@tree.command(
    name="register",
    description="Create your Account using your License.",
    guild=discord.Object(id=1171187810162716673)
)
async def register_command(interaction, username: str, password: str, license: str):
    await interaction.response.send_message(embed=discord.Embed(title="Registration is currently in progress...", color=0xff9600), ephemeral=True)

    url = f"https://keyauth.win/api/1.2/?type=init&ver=1.0&name={name}&ownerid={owner_id}"
    response = requests.post(url)
    data = response.json()
    session_id = data.get("sessionid")

    url = f"https://keyauth.win/api/1.2/?type=register&username={username}&pass={password}&key={license}&sessionid={session_id}&name={name}&ownerid={owner_id}&email=email"
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

@tree.command(
    name="status",
    description="Get the Status of the Cheats.",
    guild=discord.Object(id=1171187810162716673)
)
@app_commands.choices(choices=[
    app_commands.Choice(name="All", value="all"),
    app_commands.Choice(name="Auth", value="Auth"),
    app_commands.Choice(name="CS2", value="CS2"),
    app_commands.Choice(name="Fortnite", value="Fortnite"),])
async def status_command(interaction, choices: app_commands.Choice[str]):        
    await interaction.response.send_message(embed=discord.Embed(title="Recieving Status is currently in progress...", color=0xff9600), ephemeral=True)

    choice = choices.value

    a_state, a_full_state, a_color = status("Auth")
    cs_state, cs_full_state, cs_color = status("CS2")
    fn_state, fn_full_state, fn_color = status("Fortnite")

    if choice == "all":
        embedComp=discord.Embed(title="All Statuses!", color=0x0000ff)
        embedComp.add_field(name="Auth", value=a_state, inline=False)
        embedComp.add_field(name="CS2", value=cs_state, inline=False)
        embedComp.add_field(name="Fortnite", value=fn_state, inline=False)

        await interaction.followup.send(embed=embedComp)
    elif choice == "Auth":
        embedComp=discord.Embed(title=a_full_state, color=a_color)
        await interaction.followup.send(embed=embedComp)
    elif choice == "CS2":
        embedComp=discord.Embed(title=cs_full_state, color=cs_color)
        await interaction.followup.send(embed=embedComp)
    elif choice == "Fortnite":
        embedComp=discord.Embed(title=fn_full_state, color=fn_color)
        await interaction.followup.send(embed=embedComp)



def status(program):
    p = program.lower()
    url = f"http:///status/get/{p}"
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
    else:
        full_state = f"🔴 : A Error happend while recieving the Error of {program}."
        state = "🔴 : Unkown"
        color = 0xff0000

    return state, full_state, color


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1171187810162716673))
    print("Bot is ready!")

client.run(discord_token)