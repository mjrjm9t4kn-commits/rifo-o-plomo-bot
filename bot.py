import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= READY =================
@bot.event
async def on_ready():
    print(f"🔥 Rifo o Plomo RP ONLINE : {bot.user}")

# ================= SETUP COMPLET RP =================
@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):

    guild = ctx.guild

    # ================= ROLES =================
    roles = [
        "👑 Boss Rifo",
        "💀 Bras droit",
        "🔫 Soldat",
        "⚠️ Recrue",
        "🚓 Police RP"
    ]

    for r in roles:
        await guild.create_role(name=r)

    # ================= CATEGORIES =================
    cat_info = await guild.create_category("📢 INFO RIFO O PLOMO")
    cat_rp = await guild.create_category("🏙️ RP CITY")
    cat_gang = await guild.create_category("💀 BASE RIFO")
    cat_support = await guild.create_category("🎫 SUPPORT / RECRUTEMENT")
    cat_voice = await guild.create_category("🔊 VOCAL RP")
    cat_logs = await guild.create_category("📜 LOGS")

    # ================= INFO =================
    await guild.create_text_channel("📜-règlement-rp", category=cat_info)
    await guild.create_text_channel("📢-annonces", category=cat_info)

    # ================= RP =================
    await guild.create_text_channel("🏙️-ville-rp", category=cat_rp)
    await guild.create_text_channel("🚓-police-rp", category=cat_rp)
    await guild.create_text_channel("🧾-missions-rp", category=cat_rp)

    # ================= BASE GANG =================
    await guild.create_text_channel("💀-base-rifo", category=cat_gang)
    await guild.create_text_channel("🔫-plans", category=cat_gang)
    await guild.create_text_channel("💰-business", category=cat_gang)

    # ================= SUPPORT =================
    await guild.create_text_channel("🎫-tickets", category=cat_support)
    await guild.create_text_channel("📋-recrutement", category=cat_support)

    # ================= VOCAL =================
    await guild.create_voice_channel("🔊 Discussion RP", category=cat_voice)
    await guild.create_voice_channel("💀 Réunion gang", category=cat_voice)
    await guild.create_voice_channel("🚓 Police RP", category=cat_voice)

    # ================= LOGS =================
    await guild.create_text_channel("📜-logs", category=cat_logs)

    await ctx.send("🔥 Serveur Rifo o Plomo RP créé entièrement !")

# ================= TICKETS =================
class TicketView(discord.ui.View):
    @discord.ui.button(label="🎫 Ouvrir un ticket", style=discord.ButtonStyle.green)
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}"
        )

        await channel.send(
            f"🎫 Ticket ouvert par {interaction.user.mention}\n"
            "Explique ta demande (recrutement / support / problème RP)."
        )

        await interaction.response.send_message("🎫 Ticket créé !", ephemeral=True)

@bot.command()
async def ticket(ctx):
    await ctx.send("Clique pour ouvrir un ticket 👇", view=TicketView())

# ================= BASE COMMANDES =================
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong !")

@bot.command()
async def rifo(ctx):
    await ctx.send("🔥 Rifo o Plomo est actif !")

# ================= BIENVENUE =================
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="⚠️ Recrue")
    if role:
        await member.add_roles(role)

    channel = discord.utils.get(member.guild.text_channels, name="🏙️-ville-rp")
    if channel:
        await channel.send(f"👋 Bienvenue {member.mention} dans le RP Rifo o Plomo !")

# ================= RUN =================
bot.run(TOKEN)
