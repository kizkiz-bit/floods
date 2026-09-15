import discord
from discord import app_commands, ui
import asyncio
import sys
import os

# --- CONFIG ---
# Automatically pulls from Railway Variables dashboard
TOKEN = os.getenv("BOT_TOKEN")
# Converts the ID to an integer for proper Discord comparison
OWNER_ID = int(os.getenv("ID_OWNER")) if os.getenv("ID_OWNER") else 0

class FloodButton(ui.View):
    def __init__(self, message_content):
        super().__init__(timeout=None)
        self.msg = message_content

    @ui.button(label="press2fludz (5x)", style=discord.ButtonStyle.danger)
    async def flood_button(self, interaction: discord.Interaction, button: ui.Button):
        # Tell Discord we received the click immediately to prevent timeout
        await interaction.response.defer(ephemeral=True)
        
        for _ in range(5):
            try:
                # Use followup for global external sending
                await interaction.followup.send(self.msg)
                await asyncio.sleep(0.02)
            except Exception:
                break

class MyBot(discord.Client):
    def __init__(self):
        # Using default intents + message_content is safer for most bots
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
        # Whitelist containing the owner and your specified friends
        self.whitelist = {
            OWNER_ID, 
            292895476485980161,
            980778884767318046,
            741607657521020989, 
            1251370888830390386, 
            1394753272492851322,
            586843272924626944,
            1373933519356563497,
            1135546221533077654,
            1492300393814950018,
            1500533166354468894,
            1377178406122291230,
            1012924730958950481,
            1477649211985100831,
            1493990056468152440,
            1350006862262571028,
            1370816091227689122,
            1507398961990733986,
            1515680395360993280,
            1423891285864874077,
            1533763576311971961,
            1274635023386935336
        } 

    async def setup_hook(self):
        # Syncs slash commands globally
        await self.tree.sync()
        print(f"Logged in as {self.user}")
        print(f"Online. Whitelisted users: {len(self.whitelist)}")

bot = MyBot()

def is_whitelisted(i: discord.Interaction):
    return i.user.id in bot.whitelist

@bot.tree.command(name="flood", description="cry")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def flood(i: discord.Interaction, message: str):
    if not is_whitelisted(i):
        return await i.response.send_message("luhh, no perms haha", ephemeral=True)
    
    view = FloodButton(message)
    await i.response.send_message(
        content="## Control Panel\nJoin for more:\nhttps://discord.gg/SYekAhU5NY", 
        view=view, 
        ephemeral=True
    )

@bot.tree.command(name="say", description="haha pasikat ohh")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def say(i: discord.Interaction, message: str):
    if not is_whitelisted(i): 
        return
    
    await i.response.send_message("...", ephemeral=True)
    try:
        await i.followup.send(message)
    except Exception:
        pass

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("CRITICAL ERROR: BOT_TOKEN is missing in Railway Variables!")
