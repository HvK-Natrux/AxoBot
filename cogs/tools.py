import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
import json
from config import COLORS

class ToolsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}

    @app_commands.command(name="reminder", description="Définit un rappel")
    async def reminder(
        self,
        interaction: discord.Interaction,
        temps: str,
        message: str
    ):
        # Format temps attendu: 1h, 30m, 2h30m
        try:
            total_minutes = 0
            if 'h' in temps:
                hours = int(temps.split('h')[0])
                total_minutes += hours * 60
                temps = temps.split('h')[1]
            if 'm' in temps:
                minutes = int(temps.split('m')[0])
                total_minutes += minutes

            if total_minutes <= 0:
                raise ValueError()

            reminder_time = datetime.now() + timedelta(minutes=total_minutes)
            self.reminders[interaction.user.id] = {
                'time': reminder_time,
                'message': message
            }

            await interaction.response.send_message(
                f"⏰ Je vous rappellerai dans {temps} : {message}"
            )
        except ValueError:
            await interaction.response.send_message(
                "❌ Format de temps invalide. Utilisez par exemple: 1h, 30m, 2h30m",
                ephemeral=True
            )

    @app_commands.command(name="calculer", description="Effectue un calcul simple")
    async def calculer(self, interaction: discord.Interaction, expression: str):
        try:
            # Évaluation sécurisée de l'expression
            allowed = set('0123456789+-*/(). ')
            if not all(c in allowed for c in expression):
                raise ValueError("Caractères non autorisés")
            
            result = eval(expression)
            await interaction.response.send_message(f"📊 {expression} = {result}")
        except:
            await interaction.response.send_message(
                "❌ Expression invalide. Utilisez uniquement des nombres et les opérateurs +, -, *, /",
                ephemeral=True
            )

    @app_commands.command(name="traduire", description="Traduit un texte (bientôt disponible)")
    async def traduire(
        self,
        interaction: discord.Interaction,
        texte: str,
        langue_cible: str
    ):
        # Cette commande nécessiterait une API de traduction
        await interaction.response.send_message(
            "🌐 La traduction sera bientôt disponible!"
        )

    @app_commands.command(name="météo", description="Affiche la météo d'une ville (bientôt disponible)")
    async def meteo(self, interaction: discord.Interaction, ville: str):
        # Cette commande nécessiterait une API météo
        await interaction.response.send_message(
            "🌤️ La météo sera bientôt disponible!"
        )

    @app_commands.command(name="note", description="Enregistre une note personnelle")
    async def note(
        self,
        interaction: discord.Interaction,
        titre: str,
        contenu: str
    ):
        user_id = str(interaction.user.id)
        
        with open('data/notes.json', 'r+') as f:
            try:
                notes = json.load(f)
            except json.JSONDecodeError:
                notes = {}
            
            if user_id not in notes:
                notes[user_id] = []
                
            notes[user_id].append({
                'titre': titre,
                'contenu': contenu,
                'date': datetime.now().isoformat()
            })
            
            f.seek(0)
            json.dump(notes, f, indent=4)
            f.truncate()
            
        await interaction.response.send_message(
            f"📝 Note '{titre}' enregistrée avec succès!"
        )

async def setup(bot):
    await bot.add_cog(ToolsCommands(bot))
