from configparser import ConfigParser


def extractConfig(seccion, atrib):
    config = ConfigParser()
    config.read("settings.ini", encoding="utf-8")
    return config[seccion][atrib]


def extractAllConfig(seccion):
    config = ConfigParser()
    config.read("settings.ini", encoding="utf-8")
    config = dict(config.items(seccion))
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


def movilTop(atrib, valor):
    valor = str(valor)
    config = ConfigParser()
    config.read("settings.ini", encoding="utf-8")
    config["ConfigMovil"][atrib] = valor

    with open("settings.ini", "w") as configfile:
        config.write(configfile)


def movilOrden(valores):
    for valor in valores:
        valor = str(valor)
        config = ConfigParser()
        config.read("settings.ini", encoding="utf-8")
        config["ConfigMovil"][valor] = valores[valor]

        with open("settings.ini", "w") as configfile:
            config.write(configfile)
