import discord
from discord import app_commands
from discord.ext import commands
import json
from config import COLORS

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="poll", description="Crée un sondage")
    async def poll(
        self,
        interaction: discord.Interaction,
        question: str,
        option1: str,
        option2: str,
        option3: str = None,
        option4: str = None
    ):
        options = [option1, option2]
        if option3:
            options.append(option3)
        if option4:
            options.append(option4)

        embed = discord.Embed(
            title="📊 Sondage",
            description=question,
            color=COLORS['info']
        )

        emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]

        for i, option in enumerate(options):
            embed.add_field(
                name=f"Option {emoji_numbers[i]}",
                value=option,
                inline=False
            )

        poll_message = await interaction.channel.send(embed=embed)

        for i in range(len(options)):
            await poll_message.add_reaction(emoji_numbers[i])

        await interaction.response.send_message(
            "Sondage créé avec succès !",
            ephemeral=True
        )

    @app_commands.command(name="userinfo", description="Affiche les informations détaillées d'un utilisateur")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user

        # Get user warnings
        with open('data/warnings.json', 'r') as f:
            warnings = json.load(f)

        user_warnings = warnings.get(str(interaction.guild.id), {}).get(str(member.id), [])

        embed = discord.Embed(
            title=f"Informations Détaillées de l'Utilisateur - {member.name}",
            color=COLORS['info']
        )

        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Surnom", value=member.nick or "Aucun")
        embed.add_field(name="Compte Créé le", value=member.created_at.strftime("%Y-%m-%d"))
        embed.add_field(name="Rejoint le Serveur le", value=member.joined_at.strftime("%Y-%m-%d"))
        embed.add_field(name="Rôles", value=", ".join([role.name for role in member.roles[1:]]))
        embed.add_field(name="Nombre d'Avertissements", value=len(user_warnings))

        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utils(bot))