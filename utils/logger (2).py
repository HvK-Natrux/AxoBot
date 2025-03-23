
import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure main logger
logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.INFO)
wavelink_logger = logging.getLogger('wavelink')
wavelink_logger.setLevel(logging.INFO)

# File handler for detailed logs
file_handler = logging.FileHandler(
    filename=f'logs/bot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    encoding='utf-8',
    mode='w'
)
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
logger.addHandler(console_handler)

def log_command(interaction, command_name, success=True, error=None):
    if success:
        logger.info(f"Command '{command_name}' executed by {interaction.user} (ID: {interaction.user.id})")
    else:
        logger.error(f"Command '{command_name}' failed for {interaction.user} (ID: {interaction.user.id}). Error: {error}")
