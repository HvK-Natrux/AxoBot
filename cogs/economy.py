import discord
from discord import app_commands
from discord.ext import commands
import json
from config import COLORS
import random
from datetime import datetime, timedelta

class EconomyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}

    @app_commands.command(name="daily", description="Récupère votre récompense quotidienne de pièces")
    async def daily(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        current_time = datetime.now()

        if user_id in self.cooldowns:
            time_diff = current_time - self.cooldowns[user_id]
            if time_diff < timedelta(days=1):
                remaining = timedelta(days=1) - time_diff
                hours = remaining.seconds // 3600
                minutes = (remaining.seconds // 60) % 60
                await interaction.response.send_message(
                    f"⏳ Vous devez attendre {hours}h {minutes}m avant de pouvoir récupérer votre récompense quotidienne.",
                    ephemeral=True
                )
                return

        amount = random.randint(100, 200)
        self.cooldowns[user_id] = current_time

        await interaction.response.send_message(f"💰 Vous avez reçu {amount} pièces !")

    @app_commands.command(name="balance", description="Affiche votre solde de pièces")
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        # Ici, vous devriez normalement récupérer le solde depuis une base de données
        balance = 1000  # Exemple de solde
        
        embed = discord.Embed(
            title="💰 Porte-monnaie",
            color=COLORS['info']
        )
        embed.add_field(name="Utilisateur", value=target.name)
        embed.add_field(name="Solde", value=f"{balance} pièces")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shop", description="Affiche la boutique du serveur")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🏪 Boutique du Serveur",
            description="Voici les articles disponibles :",
            color=COLORS['info']
        )
        
        # Exemple d'articles
        items = {
            "VIP": {"prix": 5000, "description": "Rôle VIP avec accès à des canaux exclusifs"},
            "Couleur": {"prix": 1000, "description": "Personnalisation de la couleur de votre nom"},
            "Badge": {"prix": 2000, "description": "Badge spécial à côté de votre nom"}
        }
        
        for item, details in items.items():
            embed.add_field(
                name=f"{item} - {details['prix']} pièces",
                value=details['description'],
                inline=False
            )
            
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pay", description="Envoie des pièces à un autre utilisateur")
    async def pay(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if amount <= 0:
            await interaction.response.send_message("❌ Le montant doit être supérieur à 0.", ephemeral=True)
            return
            
        if member == interaction.user:
            await interaction.response.send_message("❌ Vous ne pouvez pas vous envoyer de l'argent à vous-même.", ephemeral=True)
            return
            
        # Ici, vous devriez vérifier le solde et effectuer le transfert dans la base de données
        await interaction.response.send_message(
            f"💸 Vous avez envoyé {amount} pièces à {member.name}!"
        )

    @app_commands.command(name="work", description="Travaille pour gagner des pièces")
    async def work(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        current_time = datetime.now()
        
        if user_id in self.cooldowns:
            time_diff = current_time - self.cooldowns[user_id]
            if time_diff < timedelta(hours=1):
                remaining = timedelta(hours=1) - time_diff
                minutes = remaining.seconds // 60
                await interaction.response.send_message(
                    f"⏳ Vous devez vous reposer encore {minutes} minutes avant de retravailler.",
                    ephemeral=True
                )
                return
                
        jobs = [
            "Vous avez livré des pizzas",
            "Vous avez promené des chiens",
            "Vous avez fait du jardinage",
            "Vous avez nettoyé la ville",
            "Vous avez aidé à la bibliothèque"
        ]
        
        amount = random.randint(50, 100)
        self.cooldowns[user_id] = current_time
        
        await interaction.response.send_message(
            f"💼 {random.choice(jobs)} et gagné {amount} pièces!"
        )

async def setup(bot):
    await bot.add_cog(EconomyCommands(bot))
