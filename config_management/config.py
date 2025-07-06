import json
import os

class Config:
    def __init__(self, path="config.json"):
        self._path = path
        self._defaults = {
            "discord_integration_status": False,
            "discord_integration_link": ""
        }
        self._config = {}

        self._load_or_create()

    def _load_or_create(self):
        if not os.path.exists(self._path):
            self._config = self._defaults.copy()
            self._save()
        else:
            with open(self._path, "r") as f:
                self._config = json.load(f)

            # Ensure all default keys exist
            for key, value in self._defaults.items():
                self._config.setdefault(key, value)
            self._save()

    def _save(self):
        with open(self._path, "w") as f:
            json.dump(self._config, f, indent=4)

    # Dot access to config values
    def __getattr__(self, name):
        if name in self._config:
            return self._config[name]
        raise AttributeError(f"No such config option: {name}")

    def __setattr__(self, name, value):
        if name.startswith("_"):  # internal attributes
            super().__setattr__(name, value)
        else:
            self._config[name] = value
            self._save()

    # Optional helper method to change a value
    def update(self, key, value):
        setattr(self, key, value)

# Instantiate globally
config = Config()
