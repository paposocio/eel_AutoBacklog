from configparser import ConfigParser

def extractConfig(seccion,atrib):
    config = ConfigParser()
    config.read('settings.ini', encoding="utf-8")
    return config[seccion][atrib]
    
def fijoConfig(atrib,valor):
    valor=str(valor)
    config = ConfigParser()
    config.read('settings.ini', encoding="utf-8")
    config['ConfigFijo'][atrib]= valor

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)