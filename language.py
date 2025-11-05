import json
import os


class ConfigMeta(type):
    """Metaclass to ensure attributes always exist"""
    def __getattr__(cls, name):
        if name in cls._defaults:
            # If attribute doesn't exist, create it from defaults
            setattr(cls, name, cls._defaults[name])
            return cls._defaults[name]
        raise AttributeError(f"'{cls.__name__}' object has no attribute '{name}'")


class Config(metaclass=ConfigMeta):
    CONFIG_FILE = os.path.expanduser("~/.nocturne_config.json")

    _defaults = {
        "LANGUAGE": "english",
        "EMOJIS": False,
        "MAX_WORKERS": 200,
        "USE_TOR": True,
        "TOR_ROTATION_INTERVAL": 30,
    }
    
    # Initialize attributes with default values
    LANGUAGE = _defaults["LANGUAGE"]
    EMOJIS = _defaults["EMOJIS"]
    MAX_WORKERS = _defaults["MAX_WORKERS"]
    USE_TOR = _defaults["USE_TOR"]
    TOR_ROTATION_INTERVAL = _defaults["TOR_ROTATION_INTERVAL"]

    @classmethod
    def load_config(cls):
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, "r") as f:
                    config = json.load(f)
                for key, value in config.items():
                    if key in cls._defaults:
                        setattr(cls, key, value)
            except Exception as e:
                print(f"Error loading config: {e}")
                for key, value in cls._defaults.items():
                    setattr(cls, key, value)
        else:
            for key, value in cls._defaults.items():
                setattr(cls, key, value)

    @classmethod
    def save_config(cls):
        try:
            config = {}
            for key in cls._defaults:
                config[key] = getattr(cls, key, cls._defaults[key])

            with open(cls.CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")


class Translator:
    def __init__(self, language_file="LANGUAGE.txt"):
        if not os.path.isabs(language_file):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            language_file = os.path.join(base_dir, language_file)
        self.language_file = language_file
        self.messages = self.load_messages(self.language_file)

    def load_messages(self, language_file):
        try:
            with open(language_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Language file '{language_file}' not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{language_file}'.")
            return {}

    def reload(self):
        self.messages = self.load_messages(self.language_file)

    def get(self, key):
        lang = getattr(Config, "LANGUAGE", "english")
        return self.messages.get(lang, {}).get(
            key, self.messages.get("english", {}).get(key, key)
        )


# Load configuration when module is imported
Config.load_config()

t = Translator()
