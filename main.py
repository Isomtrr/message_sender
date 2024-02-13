#discord:@batmanthe
#githubisomtrr
#https://naobot.me
#discord.gg/tranime
#please only use this bot on your own guild
import time, typing, traceback, asyncio, sys, subprocess
try:
    import colorama
    from termcolor import colored, cprint
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "termcolor"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    import colorama
    from termcolor import colored, cprint
colorama.init()
try:
    import discord
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "discord.py"])
    import discord
import discord.app_commands.commands
from discord import app_commands
from discord.ext import tasks
async def send_everyone(guild:discord.Guild, message:str, embed:discord.Embed=None):
    for member in guild.members:
        try:
            if member.bot:
                continue
            if embed:
                await asyncio.create_task(member.send(content=message, embed=embed))
            else:
                await asyncio.create_task(member.send(content=message))
        except:
            pass
class MyClient(discord.Client):
    statuses = ["By @batmanthe", "naobot.me"]
    i = 0
    mytime = time.time()
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.messages = True
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def on_ready(self):
        print(f'logged as {self.user}(ID: {self.user.id})')
        print(f"Statuses:{len(self.statuses)}")
    @tasks.loop(seconds=10)
    async def my_background_task(self):
        try:
            if client.is_closed():
                return
            if type(self.i) != int:
                self.i = 0
            if self.i > len(self.statuses) - 1:
                self.i = 0
            try:
                status = self.statuses[self.i].replace("[lenguild]", str(len(client.guilds)))
            except Exception as e:
                status = "Calm down"
            await client.change_presence(activity=discord.Game(name=status), status="idle")
            if self.i < len(self.statuses) - 1:
                self.i += 1
            elif self.i == len(self.statuses) - 1:
                self.i = 0
        except Exception as e:
            cprint(f"Error in background task: {e}", "red")

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        await self.tree.sync()
        self.my_background_task.start()
client = MyClient()
class Contact():
    color = None

class EmbedModal(discord.ui.Modal, title='Embed'):
    embed_title = discord.ui.TextInput(
        label='Embed title',
        style=discord.TextStyle.short,
        placeholder='To here...',
        required=False,
        max_length=200,
        min_length=1,
    )
    embed_text = discord.ui.TextInput(
        label='Embed text',
        style=discord.TextStyle.long,
        placeholder='To here...',
        required=True,
        max_length=1999,
        min_length=1,
    )
    embed_url = discord.ui.TextInput(
        label='Embed URL',
        style=discord.TextStyle.short,
        placeholder='To here...',
        required=False,
        max_length=200,
        min_length=0,
    )
    image_url = discord.ui.TextInput(
        label='Image URL',
        style=discord.TextStyle.short,
        placeholder='To here...',
        required=False,
        max_length=200,
        min_length=0,
    )
    footer_url = discord.ui.TextInput(
        label='Footer URL',
        style=discord.TextStyle.short,
        placeholder='To here...',
        required=False,
        max_length=200,
        min_length=0,
    )
    footer_text = discord.ui.TextInput(
        label='Footer text',
        style=discord.TextStyle.short,
        placeholder='To here...',
        required=False,
        max_length=1999,
        min_length=0,
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.embed_title.value,
            description=self.embed_text.value,
        )
        if Contact.color:
            embed.colour = getattr(discord.Colour, Contact.color)()
        if self.embed_url.value:
            embed.url = self.embed_url.value
        if self.image_url.value:
            embed.set_image(url=self.image_url.value)
        if self.footer_url.value:
            embed.footer.icon_url = self.footer_url.value
        if self.footer_text.value:
            embed.set_footer(text=self.footer_text.value)
        await interaction.response.send_message("Sending message to all members...", ephemeral=True)
        await send_everyone(interaction.guild, "", embed)
        await interaction.followup.send("Message sent to all members", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        cprint("".join(traceback.format_exception(type(error), error, error.__traceback__))[:-1], "red")
        return
class TextModal(discord.ui.Modal, title='Text'):
    text = discord.ui.TextInput(
        label='Text',
        style=discord.TextStyle.long,
        placeholder='To here...',
        required=True,
        max_length=3900,
        min_length=3,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Sending message to all members...", ephemeral=True)
        await send_everyone(interaction.guild, self.text.value)
        await interaction.followup.send("Message sent to all members", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        cprint("".join(traceback.format_exception(type(error), error, error.__traceback__))[:-1], "red")
        return
@app_commands.guild_only
@client.tree.command(description="Send message to all members in the guild(only for admins)")
@app_commands.checks.cooldown(1, 5, key=lambda i: (i.guild.id))
@app_commands.choices(send_type=[
        app_commands.Choice(name="Embed", value="embed"),
        app_commands.Choice(name="Normal", value="normal")])
async def send_to_everyone(interaction: discord.Interaction, send_type: typing.Literal["embed", "normal"], color: typing.Literal["red","blue","green"] = None):
    if not interaction.user.guild_permissions.administrator:
        return interaction.response.send_message("You don't have permission(Administrator) to use this command", ephemeral=True)
    Contact.color = color
    if send_type == "embed":
        await interaction.response.send_modal(EmbedModal())
    else:
        await interaction.response.send_modal(TextModal())
    Contact.color = None
client.run('MTIwNzA0NDk5MTAwODg5OTExMg.G2bpEf.lqkOky9fV-HjgsNwcwoMzxKMxP27VNzLkl0D8A')