import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ================= READY =================
@bot.event
async def on_ready():
    print(f"✅ Rifo o Plomo connecté : {bot.user}")

# ================= ECONOMIE =================
user_money = {}

@bot.command()
async def money(ctx):
    user = ctx.author.id
    money = user_money.get(user, 0)
    await ctx.send(f"💰 Tu as {money} coins.")

@bot.command()
async def daily(ctx):
    user = ctx.author.id
    user_money[user] = user_money.get(user, 0) + 100
    await ctx.send("💰 +100 coins récupérés !")

# ================= MODERATION =================
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member} kické.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"⛔ {member} banni.")

# ================= WARN SYSTEM =================
warns = {}

@bot.command()
async def warn(ctx, member: discord.Member, *, reason="Aucune raison"):
    if member.id not in warns:
        warns[member.id] = []
    warns[member.id].append(reason)
    await ctx.send(f"⚠️ {member.mention} averti : {reason}")

@bot.command()
async def warnslist(ctx, member: discord.Member):
    w = warns.get(member.id, [])
    await ctx.send(f"📜 Warns de {member} : {w}")

# ================= SETUP =================
@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    guild = ctx.guild

    await guild.create_text_channel("📢-annonces")
    await guild.create_text_channel("💬-chat")
    await guild.create_text_channel("🎫-tickets")

    await guild.create_role(name="Recrue")

    await ctx.send("✅ Setup terminé Rifo o Plomo")

# ================= BIENVENUE =================
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Recrue")
    if role:
        await member.add_roles(role)

# ================= TICKETS (BOUTON) =================
class TicketView(discord.ui.View):
    @discord.ui.button(label="🎫 Ouvrir ticket", style=discord.ButtonStyle.green)
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}"
        )

        await channel.send(f"🎫 Ticket ouvert par {interaction.user.mention}")
        await interaction.response.send_message("Ticket créé !", ephemeral=True)

@bot.command()
async def ticket(ctx):
    view = TicketView()
    await ctx.send("Clique pour ouvrir un ticket 👇", view=view)

# ================= LOGS =================
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="📢-annonces")
    if channel:
        await channel.send(f"👋 {member} a quitté le serveur.")

# ================= TOKEN =================
bot.run(os.getenv("TOKEN"))
