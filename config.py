# Liste des extensions à charger au démarrage
INITIAL_EXTENSIONS = [
    'cogs.basic',
    'cogs.moderation',
    'cogs.admin',
    'cogs.utils',
    'cogs.fun',
    'cogs.info',
    'cogs.config',
    'cogs.economy',
    'cogs.games',
    'cogs.tools'
]

# Version du bot
VERSION = "1.0.0"

# Couleurs pour les embeds
COLORS = {
    'success': 0x2ecc71,  # Vert
    'error': 0xe74c3c,    # Rouge
    'info': 0x3498db,     # Bleu
    'warning': 0xf1c40f   # Jaune
}

# Niveaux de permission
PERMISSION_LEVELS = {
    'user': 0,
    'moderator': 1,
    'admin': 2,
    'owner': 3
}