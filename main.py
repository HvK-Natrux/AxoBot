import os
import discord
from discord.ext import commands
import logging
import json
from config import INITIAL_EXTENSIONS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')

class DiscordBot(commands.Bot):
    def __init__(self):
        # Configure tous les intents nécessaires
        intents = discord.Intents.all()

        super().__init__(
            command_prefix='/',
            intents=intents,
            application_id=os.getenv('APPLICATION_ID')
        )

        # Initialize data files
        self.initialize_data_files()

    async def setup_hook(self):
        for extension in INITIAL_EXTENSIONS:
            try:
                await self.load_extension(extension)
                print(f'Loaded extension: {extension}')
            except Exception as e:
                print(f'Failed to load extension {extension}. Error: {e}')

        # Synchronize slash commands
        try:
            print('Synchronizing slash commands...')
            commands = await self.tree.fetch_commands()
            print(f'Current commands: {[cmd.name for cmd in commands]}')

            await self.tree.sync()
            print('Slash commands synchronized successfully!')

            commands = await self.tree.fetch_commands()
            print(f'Commands after sync: {[cmd.name for cmd in commands]}')
        except Exception as e:
            print(f'Failed to sync commands: {e}')

    def initialize_data_files(self):
        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')

        # Initialize warnings.json
        if not os.path.exists('data/warnings.json'):
            with open('data/warnings.json', 'w') as f:
                json.dump({}, f)

        # Initialize settings.json
        if not os.path.exists('data/settings.json'):
            with open('data/settings.json', 'w') as f:
                json.dump({
                    "log_channel": None,
                    "welcome_channel": None,
                    "language": "en"
                }, f)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_error(self, event_method: str, *args, **kwargs):
        logger.error(f'Error in {event_method}:', exc_info=True)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        logger.error(f'Error in command {ctx.command}:', exc_info=error)

def main():
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("⚠️ Erreur: Token Discord non trouvé!")
        print("Assurez-vous d'avoir défini la variable d'environnement DISCORD_TOKEN")
        return

    try:
        bot = DiscordBot()
        print("🔄 Tentative de connexion au bot Discord...")
        bot.run(token)
    except discord.errors.LoginFailure as e:
        print("❌ Échec de la connexion: Token invalide")
        print("Veuillez vérifier que le token est correct et a les permissions nécessaires")
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")

if __name__ == '__main__':
    main()
