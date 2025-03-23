import discord
from discord import app_commands
from discord.ext import commands
from config import VERSION, COLORS

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Vérifie si le bot est en ligne")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! Latence: {round(self.bot.latency * 1000)}ms")

    @app_commands.command(name="help", description="Affiche les commandes disponibles")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Commandes du Bot",
            description="Voici toutes les commandes disponibles:",
            color=COLORS['info']
        )

        # Commandes de Base
        embed.add_field(
            name="📋 Commandes de Base",
            value="""
            `/ping` - Vérifier le temps de réponse du bot
            `/help` - Afficher ce message d'aide
            `/info` - Afficher les informations du bot
            `/server` - Afficher les informations du serveur
            `/user` - Afficher les informations d'un utilisateur
            """,
            inline=False
        )

        # Commandes de Modération
        embed.add_field(
            name="🛡️ Commandes de Modération",
            value="""
            `/kick` - Expulser un utilisateur du serveur
            `/ban` - Bannir un utilisateur du serveur
            `/warn` - Avertir un utilisateur
            `/clear` - Supprimer des messages dans un canal
            """,
            inline=False
        )

        # Commandes d'Administration
        embed.add_field(
            name="⚙️ Commandes d'Administration",
            value="""
            `/role` - Ajouter ou retirer un rôle à un utilisateur
            `/setlogchannel` - Définir le canal des logs
            `/announce` - Envoyer une annonce
            """,
            inline=False
        )

        # Commandes Utilitaires
        embed.add_field(
            name="🔧 Commandes Utilitaires",
            value="""
            `/poll` - Créer un sondage
            `/userinfo` - Afficher les informations détaillées d'un utilisateur
            """,
            inline=False
        )

        # Commandes Fun
        embed.add_field(
            name="🎮 Commandes Fun",
            value="""
            `/8ball` - Poser une question à la boule magique
            `/choose` - Faire un choix aléatoire
            `/joke` - Raconter une blague
            `/meme` - Afficher un meme aléatoire
            `/cookie` - Donner un cookie
            `/hug` - Faire un câlin
            `/say` - Faire dire quelque chose au bot
            `/reverse` - Inverser le texte
            `/roll` - Lancer des dés
            `/flip` - Lancer une pièce
            """,
            inline=False
        )

        # Commandes d'Information
        embed.add_field(
            name="ℹ️ Commandes d'Information",
            value="""
            `/serverinfo` - Informations détaillées sur le serveur
            `/roleinfo` - Informations sur un rôle
            `/channelinfo` - Informations sur un canal
            `/botinfo` - Informations détaillées sur le bot
            `/avatar` - Afficher l'avatar d'un utilisateur
            """,
            inline=False
        )

        # Commandes de Configuration
        embed.add_field(
            name="🔧 Commandes de Configuration",
            value="""
            `/setwelcome` - Configurer le message de bienvenue
            `/setprefix` - Configurer le préfixe personnalisé
            `/setlang` - Configurer la langue du serveur
            `/togglecommand` - Activer/désactiver une commande
            `/autorole` - Configurer le rôle automatique
            `/setlogs` - Configurer les canaux de logs
            `/settings` - Afficher les paramètres actuels
            """,
            inline=False
        )

        embed.set_footer(text="Pour plus d'informations sur une commande, utilisez /help <commande>")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="info", description="Affiche les informations du bot")
    async def info(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Informations du Bot",
            color=COLORS['info']
        )
        embed.add_field(name="Version", value=VERSION)
        embed.add_field(name="Créateur", value="Your Name")
        embed.add_field(name="Bibliothèque", value="discord.py")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="server", description="Affiche les informations du serveur")
    async def server(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title=f"Informations du Serveur - {guild.name}",
            color=COLORS['info']
        )
        embed.add_field(name="Propriétaire", value=guild.owner)
        embed.add_field(name="Nombre de Membres", value=guild.member_count)
        embed.add_field(name="Créé le", value=guild.created_at.strftime("%Y-%m-%d"))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="user", description="Affiche les informations d'un utilisateur")
    async def user(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(
            title=f"Informations de l'Utilisateur - {member.name}",
            color=COLORS['info']
        )
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Rejoint le", value=member.joined_at.strftime("%Y-%m-%d"))
        embed.add_field(name="Rôles", value=", ".join([role.name for role in member.roles[1:]]))
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))