from language import Translator, Config

Config.LANGUAGE = "spanish"
t = Translator()
print(t.get("banner"))
