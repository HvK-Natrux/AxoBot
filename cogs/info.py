import discord
from discord import app_commands
from discord.ext import commands
from config import COLORS, VERSION
import platform
import psutil
import time
from datetime import datetime

class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @app_commands.command(name="serverinfo", description="Affiche des informations détaillées sur le serveur")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"Informations sur {guild.name}", color=COLORS['info'])
        
        # Informations générales
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Propriétaire", value=guild.owner)
        embed.add_field(name="Région", value=str(guild.preferred_locale))
        
        # Statistiques des membres
        embed.add_field(name="Membres", value=guild.member_count)
        embed.add_field(name="Humains", value=len([m for m in guild.members if not m.bot]))
        embed.add_field(name="Bots", value=len([m for m in guild.members if m.bot]))
        
        # Statistiques des canaux
        channels = guild.channels
        embed.add_field(name="Catégories", value=len([c for c in channels if isinstance(c, discord.CategoryChannel)]))
        embed.add_field(name="Textuels", value=len([c for c in channels if isinstance(c, discord.TextChannel)]))
        embed.add_field(name="Vocaux", value=len([c for c in channels if isinstance(c, discord.VoiceChannel)]))
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="roleinfo", description="Affiche des informations sur un rôle")
    async def roleinfo(self, interaction: discord.Interaction, role: discord.Role):
        embed = discord.Embed(title=f"Informations sur le rôle {role.name}", color=role.color)
        
        # Informations générales
        embed.add_field(name="ID", value=role.id)
        embed.add_field(name="Couleur", value=str(role.color))
        embed.add_field(name="Position", value=role.position)
        embed.add_field(name="Mentionnable", value="Oui" if role.mentionable else "Non")
        embed.add_field(name="Affiché séparément", value="Oui" if role.hoist else "Non")
        embed.add_field(name="Membres", value=len(role.members))
        
        # Permissions
        perms = []
        for perm, value in role.permissions:
            if value:
                perms.append(perm.replace('_', ' ').title())
        
        if perms:
            embed.add_field(name="Permissions", value=", ".join(perms[:10]) + "..." if len(perms) > 10 else ", ".join(perms), inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="channelinfo", description="Affiche des informations sur un canal")
    async def channelinfo(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = channel or interaction.channel
        embed = discord.Embed(title=f"Informations sur #{channel.name}", color=COLORS['info'])
        
        # Informations générales
        embed.add_field(name="ID", value=channel.id)
        embed.add_field(name="Type", value=str(channel.type))
        embed.add_field(name="Catégorie", value=channel.category.name if channel.category else "Aucune")
        
        # Statistiques
        embed.add_field(name="Position", value=channel.position)
        embed.add_field(name="NSFW", value="Oui" if channel.is_nsfw() else "Non")
        embed.add_field(name="Créé le", value=channel.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="botinfo", description="Affiche des informations détaillées sur le bot")
    async def botinfo(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Informations sur le Bot", color=COLORS['info'])
        
        # Informations générales
        embed.add_field(name="Version", value=VERSION)
        embed.add_field(name="Discord.py", value=discord.__version__)
        embed.add_field(name="Python", value=platform.python_version())
        
        # Statistiques
        embed.add_field(name="Serveurs", value=len(self.bot.guilds))
        embed.add_field(name="Utilisateurs", value=len(self.bot.users))
        embed.add_field(name="Commandes", value=len(self.bot.tree.get_commands()))
        
        # Performance
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 / 1024  # En MB
        embed.add_field(name="Utilisation Mémoire", value=f"{memory_usage:.2f} MB")
        
        uptime = time.time() - self.start_time
        hours, remainder = divmod(int(uptime), 3600)
        minutes, seconds = divmod(remainder, 60)
        embed.add_field(name="Temps de Fonctionnement", value=f"{hours}h {minutes}m {seconds}s")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="Affiche l'avatar d'un utilisateur")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(title=f"Avatar de {member.name}", color=COLORS['info'])
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(InfoCommands(bot))
