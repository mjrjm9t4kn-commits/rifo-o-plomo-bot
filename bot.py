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

    # ================= SALONS =================
    rules_channel = await guild.create_text_channel("📜-règlement-rp", category=cat_info)
    await guild.create_text_channel("📢-annonces", category=cat_info)

    await guild.create_text_channel("🏙️-ville-rp", category=cat_rp)
    await guild.create_text_channel("🚓-police-rp", category=cat_rp)
    await guild.create_text_channel("🧾-missions-rp", category=cat_rp)

    await guild.create_text_channel("💀-base-rifo", category=cat_gang)
    await guild.create_text_channel("🔫-plans", category=cat_gang)
    await guild.create_text_channel("💰-business", category=cat_gang)

    await guild.create_text_channel("🎫-tickets", category=cat_support)
    await guild.create_text_channel("📋-recrutement", category=cat_support)

    await guild.create_voice_channel("🔊 Discussion RP", category=cat_voice)
    await guild.create_voice_channel("💀 Réunion gang", category=cat_voice)
    await guild.create_voice_channel("🚓 Police RP", category=cat_voice)

    await guild.create_text_channel("📜-logs", category=cat_logs)

    # ================= RÈGLEMENT AUTOMATIQUE =================
    rules_text = """
🔥 **RÈGLEMENT RIFO O PLOMO RP**

1️⃣ Respect obligatoire entre joueurs (RP sérieux)
2️⃣ Pas de triche, hack ou exploit
3️⃣ Le FearRP doit être respecté (peur réaliste)
4️⃣ Pas de meta-gaming (infos hors RP interdites)
5️⃣ Pas de troll RP inutile
6️⃣ Kill RP uniquement logique (pas gratuit)
7️⃣ Respect des rôles (Police / Gang / Civils)
8️⃣ Interdiction de spawn kill / revenge kill abusif
9️⃣ Le staff a toujours le dernier mot
🔟 Amuse-toi mais reste RP sérieux

💀 **Règle du gang Rifo o Plomo :**
- Trahison = expulsion immédiate
- Respect du Boss obligatoire
- Missions doivent être respectées
"""

    await rules_channel.send(rules_text)

    await ctx.send("🔥 Serveur RP + règlement créé avec succès !")
