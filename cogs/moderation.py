import discord
from discord import app_commands
from discord.ext import commands
import json
from config import COLORS
import datetime

class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log_action(self, guild, action, user, moderator, reason):
        with open('data/settings.json', 'r') as f:
            settings = json.load(f)

        log_channel_id = settings.get(str(guild.id), {}).get('log_channel')
        if log_channel_id:
            channel = guild.get_channel(log_channel_id)
            if channel:
                embed = discord.Embed(
                    title=f"Action de {action}",
                    color=COLORS['warning'],
                    timestamp=datetime.datetime.now()
                )
                embed.add_field(name="Utilisateur", value=f"{user.name} ({user.id})")
                embed.add_field(name="Modérateur", value=f"{moderator.name} ({moderator.id})")
                embed.add_field(name="Raison", value=reason or "Aucune raison fournie")
                await channel.send(embed=embed)

    @app_commands.command(name="kick", description="Expulse un utilisateur du serveur")
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("Vous ne pouvez pas expulser cet utilisateur en raison de la hiérarchie des rôles.", ephemeral=True)
            return

        confirm = discord.ui.Button(label="Confirmer", style=discord.ButtonStyle.danger)
        cancel = discord.ui.Button(label="Annuler", style=discord.ButtonStyle.secondary)

        async def confirm_callback(interaction: discord.Interaction):
            await member.kick(reason=reason)
            await self.log_action(interaction.guild, "Expulsion", member, interaction.user, reason)
            await interaction.response.send_message(f"Expulsé {member.name} pour: {reason or 'Aucune raison fournie'}")

        async def cancel_callback(interaction: discord.Interaction):
            await interaction.response.send_message("Expulsion annulée.", ephemeral=True)

        confirm.callback = confirm_callback
        cancel.callback = cancel_callback

        view = discord.ui.View()
        view.add_item(confirm)
        view.add_item(cancel)

        await interaction.response.send_message(
            f"Êtes-vous sûr de vouloir expulser {member.name} ?",
            view=view,
            ephemeral=True
        )

    @app_commands.command(name="ban", description="Bannit un utilisateur du serveur")
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("Vous ne pouvez pas bannir cet utilisateur en raison de la hiérarchie des rôles.", ephemeral=True)
            return

        await member.ban(reason=reason)
        await self.log_action(interaction.guild, "Bannissement", member, interaction.user, reason)
        await interaction.response.send_message(f"Banni {member.name} pour: {reason or 'Aucune raison fournie'}")

    @app_commands.command(name="warn", description="Avertit un utilisateur")
    @app_commands.default_permissions(moderate_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        with open('data/warnings.json', 'r') as f:
            warnings = json.load(f)

        guild_id = str(interaction.guild.id)
        user_id = str(member.id)

        if guild_id not in warnings:
            warnings[guild_id] = {}
        if user_id not in warnings[guild_id]:
            warnings[guild_id][user_id] = []

        warning = {
            'reason': reason,
            'moderator': interaction.user.id,
            'timestamp': datetime.datetime.now().isoformat()
        }

        warnings[guild_id][user_id].append(warning)

        with open('data/warnings.json', 'w') as f:
            json.dump(warnings, f, indent=4)

        await self.log_action(interaction.guild, "Avertissement", member, interaction.user, reason)
        await interaction.response.send_message(f"Averti {member.name} pour: {reason}")

        try:
            await member.send(f"Vous avez reçu un avertissement dans {interaction.guild.name} pour: {reason}")
        except:
            pass

    @app_commands.command(name="clear", description="Supprime des messages d'un canal")
    @app_commands.default_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        if amount < 1 or amount > 100:
            await interaction.response.send_message("Veuillez spécifier un nombre entre 1 et 100.", ephemeral=True)
            return

        await interaction.response.defer()
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Supprimé {len(deleted)} messages.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModerationCommands(bot))