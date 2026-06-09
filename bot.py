import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ================= READY =================
@bot.event
async def on_ready():
    print(f"✅ Rifo o Plomo connecté : {bot.user}")

# ================= COMMANDES =================

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong !")

@bot.command()
async def rifo(ctx):
    await ctx.send("🔥 Rifo o Plomo est actif !")

# ================= SETUP SERVEUR =================
@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):

    guild = ctx.guild

    await guild.create_text_channel("📢-annonces")
    await guild.create_text_channel("💬-chat")
    await guild.create_text_channel("🎫-tickets")

    await guild.create_role(name="Recrue")

    await ctx.send("✅ Setup Rifo o Plomo terminé !")

# ================= CLEAR =================
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"🧹 {amount} messages supprimés")

# ================= BIENVENUE =================
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Recrue")
    if role:
        await member.add_roles(role)

    channel = discord.utils.get(member.guild.text_channels, name="💬-chat")
    if channel:
        await channel.send(f"👋 Bienvenue {member.mention} sur Rifo o Plomo !")

# ================= TOKEN =================
bot.run("TON_TOKEN_ICI")
