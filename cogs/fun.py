import discord
from discord import app_commands
from discord.ext import commands
import random
import json
from config import COLORS
import asyncio
from datetime import datetime

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="8ball", description="Pose une question à la boule magique")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        responses = [
            "C'est certain.", "Sans aucun doute.", "Oui, définitivement.",
            "Probablement.", "Les signes disent que oui.", "C'est flou, réessayez.",
            "Demandez plus tard.", "Je ne peux pas prédire maintenant.",
            "N'y comptez pas.", "Ma réponse est non.", "Mes sources disent non.",
            "Les perspectives ne sont pas bonnes.", "Très douteux.", 
            "Les étoiles ne sont pas alignées.", "Concentrez-vous et demandez à nouveau."
        ]
        await interaction.response.send_message(f"🎱 Question: {question}\nRéponse: {random.choice(responses)}")

    @app_commands.command(name="choose", description="Fait un choix aléatoire parmi les options données")
    async def choose(self, interaction: discord.Interaction, options: str):
        choices = [opt.strip() for opt in options.split(',')]
        if len(choices) < 2:
            await interaction.response.send_message("Veuillez fournir au moins 2 options séparées par des virgules.")
            return
        await interaction.response.send_message(f"Je choisis: **{random.choice(choices)}**")

    @app_commands.command(name="joke", description="Raconte une blague")
    async def joke(self, interaction: discord.Interaction):
        jokes = [
            "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tombent dans le bateau !",
            "Qu'est-ce qu'un café qui ne veut pas se faire boire ? Un café qui s'échappe !",
            "Que fait un crocodile quand il rencontre une superbe femelle ? Il Lacoste !",
            "Pourquoi les poissons vivent dans l'eau salée ? Parce que dans l'eau poivrée, ils éternueraient !",
            "Que fait une fraise sur un cheval ? Tagada Tagada !",
            "Quel est le comble pour un électricien ? Ne pas être au courant !",
            "Pourquoi les abeilles se marient toujours à l'église ? Parce qu'elles ont une reine !",
            "Que disent deux chiens qui se rencontrent ? Salut, ça col-leg ?",
            "Quel est le fruit préféré des chats ? Le miaou-kiwi !",
            "Qu'est-ce qu'un hamster dans l'espace ? Un hamstéroïde !"
        ]
        await interaction.response.send_message(random.choice(jokes))

    @app_commands.command(name="meme", description="Affiche un meme aléatoire")
    async def meme(self, interaction: discord.Interaction):
        memes = [
            "https://i.imgur.com/rZk0RVf.jpg",  # Cat meme
            "https://i.imgur.com/X1QIR6P.jpg",  # Dog meme
            "https://i.imgur.com/gXSvGah.jpg",  # Gaming meme
            "https://i.imgur.com/KZu7agF.jpg",  # Programming meme
            "https://i.imgur.com/lMKuqxP.jpg"   # Discord meme
        ]
        embed = discord.Embed(title="Meme du jour", color=COLORS['info'])
        embed.set_image(url=random.choice(memes))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="cookie", description="Donne un cookie à quelqu'un")
    async def cookie(self, interaction: discord.Interaction, member: discord.Member):
        cookie_types = ["🍪", "🥠", "🍘"]
        cookie = random.choice(cookie_types)
        messages = [
            f"{interaction.user.name} offre un délicieux {cookie} à {member.name} !",
            f"{member.name} reçoit un {cookie} tout chaud de {interaction.user.name} !",
            f"Un {cookie} magique apparaît devant {member.name}, gracieuseté de {interaction.user.name} !"
        ]
        await interaction.response.send_message(random.choice(messages))

    @app_commands.command(name="hug", description="Fait un câlin à quelqu'un")
    async def hug(self, interaction: discord.Interaction, member: discord.Member):
        hug_emojis = ["🤗", "💝", "💖", "💕", "💓"]
        messages = [
            f"{interaction.user.name} fait un gros câlin à {member.name} {random.choice(hug_emojis)}",
            f"{member.name} reçoit un câlin chaleureux de {interaction.user.name} {random.choice(hug_emojis)}",
            f"*{interaction.user.name} envoie beaucoup d'amour à {member.name}* {random.choice(hug_emojis)}"
        ]
        await interaction.response.send_message(random.choice(messages))

    @app_commands.command(name="say", description="Fait dire quelque chose au bot")
    @app_commands.default_permissions(manage_messages=True)
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

    @app_commands.command(name="reverse", description="Inverse le texte donné")
    async def reverse(self, interaction: discord.Interaction, text: str):
        reversed_text = text[::-1]
        await interaction.response.send_message(f"🔄 Texte inversé : {reversed_text}")

    @app_commands.command(name="roll", description="Lance un ou plusieurs dés")
    async def roll(self, interaction: discord.Interaction, dice: str = "1d6"):
        try:
            number, sides = map(int, dice.lower().split('d'))
            if number < 1 or number > 100 or sides < 2 or sides > 100:
                await interaction.response.send_message("Format invalide. Utilisez par exemple: 1d6, 2d20, etc. (max 100 dés)")
                return

            results = [random.randint(1, sides) for _ in range(number)]
            total = sum(results)

            if number == 1:
                await interaction.response.send_message(f"🎲 Résultat: {total}")
            else:
                await interaction.response.send_message(
                    f"🎲 Résultats: {', '.join(map(str, results))}\nTotal: {total}"
                )
        except ValueError:
            await interaction.response.send_message("Format invalide. Utilisez par exemple: 1d6, 2d20, etc.")

    @app_commands.command(name="flip", description="Lance une pièce")
    async def flip(self, interaction: discord.Interaction):
        result = random.choice(["Pile", "Face"])
        await interaction.response.send_message(f"🪙 {result}!")

async def setup(bot):
    await bot.add_cog(FunCommands(bot))