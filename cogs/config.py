import discord
from discord import app_commands
from discord.ext import commands
import json
from config import COLORS
import asyncio

class ConfigCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def load_settings(self, guild_id: str):
        with open('data/settings.json', 'r') as f:
            settings = json.load(f)
            return settings.get(str(guild_id), {})

    async def save_settings(self, guild_id: str, settings_data: dict):
        with open('data/settings.json', 'r') as f:
            settings = json.load(f)
        
        if str(guild_id) not in settings:
            settings[str(guild_id)] = {}
        
        settings[str(guild_id)].update(settings_data)
        
        with open('data/settings.json', 'w') as f:
            json.dump(settings, f, indent=4)

    @app_commands.command(name="setwelcome", description="Configure le message de bienvenue")
    @app_commands.default_permissions(administrator=True)
    async def setwelcome(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        message: str
    ):
        await self.save_settings(interaction.guild.id, {
            "welcome_channel": channel.id,
            "welcome_message": message
        })
        await interaction.response.send_message(
            f"Message de bienvenue configuré dans {channel.mention}\nMessage: {message}"
        )

    @app_commands.command(name="setprefix", description="Configure le préfixe personnalisé")
    @app_commands.default_permissions(administrator=True)
    async def setprefix(self, interaction: discord.Interaction, prefix: str):
        if len(prefix) > 5:
            await interaction.response.send_message("Le préfixe doit faire moins de 5 caractères.")
            return
        
        await self.save_settings(interaction.guild.id, {"prefix": prefix})
        await interaction.response.send_message(f"Préfixe configuré sur: {prefix}")

    @app_commands.command(name="setlang", description="Configure la langue du serveur")
    @app_commands.default_permissions(administrator=True)
    async def setlang(self, interaction: discord.Interaction, lang: str):
        supported_langs = ['fr', 'en']
        if lang not in supported_langs:
            await interaction.response.send_message(
                f"Langue non supportée. Languages disponibles: {', '.join(supported_langs)}"
            )
            return
        
        await self.save_settings(interaction.guild.id, {"language": lang})
        await interaction.response.send_message(f"Langue configurée sur: {lang}")

    @app_commands.command(name="togglecommand", description="Active/désactive une commande")
    @app_commands.default_permissions(administrator=True)
    async def togglecommand(self, interaction: discord.Interaction, command: str):
        settings = await self.load_settings(interaction.guild.id)
        disabled_commands = settings.get("disabled_commands", [])
        
        if command in disabled_commands:
            disabled_commands.remove(command)
            status = "activée"
        else:
            disabled_commands.append(command)
            status = "désactivée"
        
        await self.save_settings(interaction.guild.id, {"disabled_commands": disabled_commands})
        await interaction.response.send_message(f"Commande {command} {status}.")

    @app_commands.command(name="autorole", description="Configure le rôle automatique")
    @app_commands.default_permissions(administrator=True)
    async def autorole(self, interaction: discord.Interaction, role: discord.Role):
        await self.save_settings(interaction.guild.id, {"auto_role": role.id})
        await interaction.response.send_message(f"Rôle automatique configuré sur: {role.name}")

    @app_commands.command(name="setlogs", description="Configure les différents canaux de logs")
    @app_commands.default_permissions(administrator=True)
    async def setlogs(
        self,
        interaction: discord.Interaction,
        moderation: discord.TextChannel = None,
        messages: discord.TextChannel = None,
        members: discord.TextChannel = None
    ):
        settings = {}
        if moderation:
            settings["mod_log_channel"] = moderation.id
        if messages:
            settings["msg_log_channel"] = messages.id
        if members:
            settings["member_log_channel"] = members.id
            
        if not settings:
            await interaction.response.send_message("Veuillez spécifier au moins un canal de logs.")
            return
            
        await self.save_settings(interaction.guild.id, settings)
        await interaction.response.send_message("Canaux de logs configurés avec succès.")

    @app_commands.command(name="settings", description="Affiche les paramètres actuels du serveur")
    @app_commands.default_permissions(administrator=True)
    async def settings(self, interaction: discord.Interaction):
        settings = await self.load_settings(interaction.guild.id)
        
        embed = discord.Embed(
            title="Paramètres du Serveur",
            color=COLORS['info']
        )
        
        # Ajout des paramètres à l'embed
        for key, value in settings.items():
            if key.endswith('_channel'):
                channel = interaction.guild.get_channel(value)
                value = channel.mention if channel else "Non configuré"
            elif key.endswith('_role'):
                role = interaction.guild.get_role(value)
                value = role.name if role else "Non configuré"
            
            embed.add_field(
                name=key.replace('_', ' ').title(),
                value=str(value),
                inline=False
            )
            
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ConfigCommands(bot))
