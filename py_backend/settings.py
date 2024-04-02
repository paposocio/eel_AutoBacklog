from configparser import ConfigParser


def extractConfig(seccion, atrib):
    config = ConfigParser()
    config.read("settings.ini", encoding="utf-8")
    return config[seccion][atrib]


def extractAllConfig():
    config = ConfigParser()
    config.read("settings.ini", encoding="utf-8")
    config = dict(config.items("ConfigFijo"))
    return config


def fijoTop(atrib, valor):
    valor = str(valor)
    config = ConfigParser()
    config.read("settings.ini", encoding="utf-8")
    config["ConfigFijo"][atrib] = valor

    with open("settings.ini", "w") as configfile:
        config.write(configfile)


def fijoOrden(valores):
    for valor in valores:
        valor = str(valor)
        config = ConfigParser()
        config.read("settings.ini", encoding="utf-8")
        config["ConfigFijo"][valor] = valores[valor]

        with open("settings.ini", "w") as configfile:
            config.write(configfile)
