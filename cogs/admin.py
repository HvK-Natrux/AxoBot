import discord
from discord import app_commands
from discord.ext import commands
import json
from config import COLORS

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="role", description="Ajoute ou retire un rôle à un utilisateur")
    @app_commands.default_permissions(manage_roles=True)
    async def role(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        role: discord.Role,
        action: str = "add"
    ):
        if role >= interaction.user.top_role:
            await interaction.response.send_message(
                "Vous ne pouvez pas gérer ce rôle en raison de la hiérarchie des rôles.",
                ephemeral=True
            )
            return

        try:
            if action.lower() == "add":
                await member.add_roles(role)
                await interaction.response.send_message(
                    f"Ajouté le rôle {role.name} à {member.name}",
                    ephemeral=True
                )
            elif action.lower() == "remove":
                await member.remove_roles(role)
                await interaction.response.send_message(
                    f"Retiré le rôle {role.name} de {member.name}",
                    ephemeral=True
                )
        except discord.Forbidden:
            await interaction.response.send_message(
                "Je n'ai pas la permission de gérer ce rôle.",
                ephemeral=True
            )

    @app_commands.command(name="setlogchannel", description="Définit le canal des logs")
    @app_commands.default_permissions(administrator=True)
    async def setlogchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        with open('data/settings.json', 'r') as f:
            settings = json.load(f)

        if str(interaction.guild.id) not in settings:
            settings[str(interaction.guild.id)] = {}

        settings[str(interaction.guild.id)]['log_channel'] = channel.id

        with open('data/settings.json', 'w') as f:
            json.dump(settings, f, indent=4)

        await interaction.response.send_message(f"Canal des logs défini sur {channel.mention}")

    @app_commands.command(name="announce", description="Envoie une annonce")
    @app_commands.default_permissions(administrator=True)
    async def announce(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        title: str,
        message: str
    ):
        embed = discord.Embed(
            title=title,
            description=message,
            color=COLORS['info']
        )
        embed.set_footer(text=f"Annonce par {interaction.user.name}")

        await channel.send(embed=embed)
        await interaction.response.send_message(
            "Annonce envoyée avec succès !",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))