import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= XP / LEVEL SYSTEM =================
xp = {}
level = {}

def add_xp(user_id):
    xp[user_id] = xp.get(user_id, 0) + 10
    lvl = level.get(user_id, 1)

    if xp[user_id] >= lvl * 100:
        level[user_id] = lvl + 1
        return lvl + 1
    return None

# ================= READY =================
@bot.event
async def on_ready():
    print(f"🔥 Rifo o Plomo RP ONLINE : {bot.user}")

# ================= XP ON MESSAGE =================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    new_level = add_xp(message.author.id)

    if new_level:
        await message.channel.send(
            f"🏆 {message.author.mention} passe niveau **{new_level}** dans le gang Rifo !"
        )

    await bot.process_commands(message)

# ================= SETUP SERVEUR RP =================
@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):

    guild = ctx.guild

    # ROLES
    roles = [
        "👑 Boss Rifo",
        "💀 Bras droit",
        "🔫 Soldat",
        "⚠️ Recrue",
        "🚓 Police RP"
    ]

    for r in roles:
        await guild.create_role(name=r)

    # CATEGORIES
    cat_info = await guild.create_category("📢 INFO RIFO O PLOMO")
    cat_rp = await guild.create_category("🏙️ RP CITY")
    cat_gang = await guild.create_category("💀 BASE RIFO")
    cat_support = await guild.create_category("🎫 SUPPORT & RECRUTEMENT")
    cat_voice = await guild.create_category("🔊 VOCAL RP")
    cat_logs = await guild.create_category("📜 LOGS")

    # INFO
    rules = await guild.create_text_channel("📜-règlement-rp", category=cat_info)
    await guild.create_text_channel("📢-annonces", category=cat_info)

    # RP
    await guild.create_text_channel("🏙️-ville-rp", category=cat_rp)
    await guild.create_text_channel("🚓-police-rp", category=cat_rp)
    await guild.create_text_channel("🧾-missions-rp", category=cat_rp)

    # GANG
    await guild.create_text_channel("💀-base-rifo", category=cat_gang)
    await guild.create_text_channel("🔫-plans", category=cat_gang)
    await guild.create_text_channel("💰-business", category=cat_gang)

    # SUPPORT
    await guild.create_text_channel("🎫-tickets", category=cat_support)
    await guild.create_text_channel("📋-recrutement", category=cat_support)

    # VOCAL
    await guild.create_voice_channel("🔊 Discussion RP", category=cat_voice)
    await guild.create_voice_channel("💀 Réunion gang", category=cat_voice)
    await guild.create_voice_channel("🚓 Police RP", category=cat_voice)

    # LOGS
    await guild.create_text_channel("📜-logs", category=cat_logs)

    # REGLEMENT AUTO
    await rules.send("""
🔥 RÈGLEMENT RIFO O PLOMO RP

1️⃣ Respect obligatoire
2️⃣ No meta-gaming
3️⃣ FearRP obligatoire
4️⃣ Pas de troll RP
5️⃣ Kill RP logique uniquement
6️⃣ Respect Police / Gang
7️⃣ Pas de cheat
8️⃣ Staff décision finale

💀 Gang :
- Trahison = expulsion
- Respect Boss obligatoire
""")

    await ctx.send("🔥 Serveur Rifo o Plomo RP créé !")

# ================= TICKETS =================
class CloseTicketView(discord.ui.View):
    @discord.ui.button(label="🔒 Fermer ticket", style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🗑️ Ticket fermé", ephemeral=True)
        await interaction.channel.delete()

class TicketView(discord.ui.View):
    @discord.ui.button(label="🎫 Ouvrir ticket", style=discord.ButtonStyle.green)
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        channel = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}"
        )

        await channel.send(
            f"🎫 Ticket de {interaction.user.mention}\n"
            "Explique ta demande (recrutement / support RP)."
        )

        await channel.send("🔒 Ferme le ticket ici :", view=CloseTicketView())

        await interaction.response.send_message("🎫 Ticket créé !", ephemeral=True)

@bot.command()
async def ticket(ctx):
    await ctx.send("Clique pour ouvrir un ticket 👇", view=TicketView())

# ================= LOCK SERVER =================
@bot.command()
@commands.has_permissions(administrator=True)
async def lock(ctx):

    for channel in ctx.guild.text_channels:
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    await ctx.send("🔒 Serveur verrouillé (mode lockdown RP)")

# ================= COMMANDES =================
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong")

@bot.command()
async def rifo(ctx):
    await ctx.send("🔥 Rifo o Plomo domine le RP")

# ================= JOIN =================
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="⚠️ Recrue")
    if role:
        await member.add_roles(role)

# ================= RUN =================
bot.run(TOKEN)
