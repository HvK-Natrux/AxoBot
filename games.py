
import discord
from discord import app_commands
from discord.ext import commands
import random
from config import COLORS

class GamesCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rps_emojis = {"pierre": "🪨", "feuille": "📄", "ciseaux": "✂️"}

    @app_commands.command(name="rps", description="Joue à pierre-feuille-ciseaux contre le bot")
    async def rps(self, interaction: discord.Interaction, choix: str):
        choix = choix.lower()
        if choix not in self.rps_emojis:
            await interaction.response.send_message("❌ Choix invalide. Utilisez 'pierre', 'feuille' ou 'ciseaux'.")
            return
            
        bot_choice = random.choice(list(self.rps_emojis.keys()))
        
        # Déterminer le gagnant
        if choix == bot_choice:
            result = "Égalité!"
        elif (
            (choix == "pierre" and bot_choice == "ciseaux") or
            (choix == "feuille" and bot_choice == "pierre") or
            (choix == "ciseaux" and bot_choice == "feuille")
        ):
            result = "Vous avez gagné!"
        else:
            result = "J'ai gagné!"
            
        await interaction.response.send_message(
            f"{self.rps_emojis[choix]} vs {self.rps_emojis[bot_choice]}\n{result}"
        )

    @app_commands.command(name="deviner", description="Joue au jeu du nombre à deviner")
    async def deviner(self, interaction: discord.Interaction, nombre: int):
        if nombre < 1 or nombre > 100:
            await interaction.response.send_message("❌ Le nombre doit être entre 1 et 100.", ephemeral=True)
            return
            
        target = random.randint(1, 100)
        if nombre == target:
            await interaction.response.send_message("🎉 Bravo! Vous avez deviné le bon nombre!")
        else:
            hint = "plus grand" if target > nombre else "plus petit"
            await interaction.response.send_message(f"Le nombre était {target}. C'est {hint} que votre proposition.")

    @app_commands.command(name="pendu", description="Joue au jeu du pendu")
    async def pendu(self, interaction: discord.Interaction, lettre: str):
        if len(lettre) != 1:
            await interaction.response.send_message("❌ Veuillez entrer une seule lettre.", ephemeral=True)
            return
            
        # Ici, vous devriez implémenter la logique du jeu du pendu
        # Cette version est simplifiée
        await interaction.response.send_message("🎯 Le jeu du pendu sera bientôt disponible!")

    @app_commands.command(name="quiz", description="Lance un quiz avec des questions variées")
    async def quiz(self, interaction: discord.Interaction):
        questions = [
            {
                "question": "Quelle est la capitale de la France?",
                "reponse": "Paris"
            },
            {
                "question": "Combien font 2+2?",
                "reponse": "4"
            }
        ]
        
        question = random.choice(questions)
        embed = discord.Embed(
            title="❓ Quiz",
            description=question["question"],
            color=COLORS['info']
        )
        
        await interaction.response.send_message(embed=embed)

    class TicTacToeButton(discord.ui.Button):
        def __init__(self, x: int, y: int):
            super().__init__(style=discord.ButtonStyle.green, label="\u200b", row=y)
            self.x = x
            self.y = y

        async def callback(self, interaction: discord.Interaction):
            view: TicTacToeView = self.view
            if interaction.user not in (view.player1, view.player2):
                return
            if interaction.user != view.current_player:
                await interaction.response.send_message("Ce n'est pas votre tour!", ephemeral=True)
                return
            
            if self.label != "\u200b":
                await interaction.response.send_message("Cette case est déjà prise!", ephemeral=True)
                return

            self.label = "X" if view.current_player == view.player1 else "O"
            self.style = discord.ButtonStyle.red
            self.disabled = True

            view.board[self.y][self.x] = self.label
            
            if view.check_winner():
                for child in view.children:
                    child.disabled = True
                await interaction.response.edit_message(content=f"{interaction.user.mention} a gagné! 🎉", view=view)
                return
            
            if view.is_board_full():
                for child in view.children:
                    child.disabled = True
                await interaction.response.edit_message(content="Match nul! 🤝", view=view)
                return

            view.current_player = view.player2 if view.current_player == view.player1 else view.player1
            await interaction.response.edit_message(content=f"C'est au tour de {view.current_player.mention}!", view=view)

    class TicTacToeView(discord.ui.View):
        def __init__(self, player1: discord.Member, player2: discord.Member):
            super().__init__(timeout=180)
            self.player1 = player1
            self.player2 = player2
            self.current_player = player1
            self.board = [[" " for _ in range(3)] for _ in range(3)]

            for y in range(3):
                for x in range(3):
                    self.add_item(GamesCommands.TicTacToeButton(x, y))

        def check_winner(self):
            # Vérification des lignes et colonnes
            for i in range(3):
                if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                    return True
                if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                    return True
            
            # Vérification des diagonales
            if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
                return True
            if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
                return True
            
            return False

        def is_board_full(self):
            return all(cell != " " for row in self.board for cell in row)

    @app_commands.command(name="morpion", description="Joue au morpion contre un autre joueur")
    async def morpion(self, interaction: discord.Interaction, adversaire: discord.Member):
        if adversaire == interaction.user:
            await interaction.response.send_message("❌ Vous ne pouvez pas jouer contre vous-même.", ephemeral=True)
            return
            
        if adversaire.bot:
            await interaction.response.send_message("❌ Vous ne pouvez pas jouer contre un bot.", ephemeral=True)
            return

        view = GamesCommands.TicTacToeView(interaction.user, adversaire)
        await interaction.response.send_message(
            f"🎮 Partie de morpion entre {interaction.user.mention} (X) et {adversaire.mention} (O)\n"
            f"C'est au tour de {interaction.user.mention}!",
            view=view
        )

async def setup(bot):
    await bot.add_cog(GamesCommands(bot))
