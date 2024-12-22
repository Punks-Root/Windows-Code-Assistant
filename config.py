import json
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.config_path = Path('resources/config.json')
        self.default_config = {
            "language": "es-ES",
            "voice_engine": "espeak" if os.name != 'nt' else "sapi5",
            "log_level": "INFO",
            "model": "gpt4all"  # Usamos GPT4All como alternativa gratuita a OpenAI
        }
        self.load_config()

    def load_config(self):
        """Carga la configuración o crea una por defecto"""
        if not self.config_path.exists():
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.default_config, f, indent=4)
            self.config = self.default_config
        else:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)

    def get(self, key):
        """Obtiene un valor de configuración"""
        return self.config.get(key, self.default_config.get(key))

    def set(self, key, value):
        """Establece un valor de configuración"""
        self.config[key] = value
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
