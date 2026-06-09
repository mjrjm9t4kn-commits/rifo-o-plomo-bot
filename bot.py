@bot.command()
@commands.has_permissions(administrator=True)
async def reset(ctx, confirm=None):

    if confirm != "CONFIRMER":
        return await ctx.send("⚠️ Tape `!reset CONFIRMER` pour supprimer tout le serveur.")

    guild = ctx.guild

    await ctx.send("💥 Reset du serveur en cours...")

    # ================= DELETE CHANNELS =================
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

    # ================= DELETE ROLES =================
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
            except:
                pass

    await ctx.send("🔥 Reset terminé (salons + rôles supprimés)")


# ================= AJOUT RESET RP (SANS TOUCHER AU PREMIER) =================
@bot.command()
@commands.has_permissions(administrator=True)
async def reset_rp(ctx):

    guild = ctx.guild

    await ctx.send("🔄 Reset RP en cours...")

    for channel in guild.channels:
        if channel.name in ["🏙️-ville-rp", "💀-base-rifo", "🧾-missions-rp"]:
            try:
                await channel.delete()
            except:
                pass

    await ctx.send("✅ Reset RP terminé (zones RP uniquement)")
