import json
import os
from typing import Dict, List, Any, Optional
import asyncio
import datetime

class Database:
    def __init__(self):
        self.warnings_file = "data/warnings.json"
        self.settings_file = "data/settings.json"
        self.ensure_data_files()
        self.lock = asyncio.Lock()

    def ensure_data_files(self):
        os.makedirs("data", exist_ok=True)
        for file in [self.warnings_file, self.settings_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump({}, f)

    async def get_warnings(self, user_id: str) -> List[Dict[str, Any]]:
        async with self.lock:
            with open(self.warnings_file, 'r') as f:
                warnings = json.load(f)
                return warnings.get(str(user_id), [])

    async def add_warning(self, user_id: str, reason: str, mod_id: str):
        async with self.lock:
            with open(self.warnings_file, 'r') as f:
                warnings = json.load(f)

            if str(user_id) not in warnings:
                warnings[str(user_id)] = []

            warnings[str(user_id)].append({
                'reason': reason,
                'mod_id': str(mod_id),
                'timestamp': datetime.datetime.utcnow().isoformat()
            })

            with open(self.warnings_file, 'w') as f:
                json.dump(warnings, f, indent=4)

    async def get_setting(self, guild_id: str, key: str) -> Optional[Any]:
        async with self.lock:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                guild_settings = settings.get(str(guild_id), {})
                return guild_settings.get(key)

    async def set_setting(self, guild_id: str, key: str, value: Any):
        async with self.lock:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)

            if str(guild_id) not in settings:
                settings[str(guild_id)] = {}

            settings[str(guild_id)][key] = value

            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)

db = Database()