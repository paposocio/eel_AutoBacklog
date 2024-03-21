from configparser import ConfigParser

def fijoConfig(atrib,valor):
    valor=str(valor)
    config = ConfigParser()
    config.read('settings.ini', encoding="utf-8")
    config['ConfigFijo'][atrib]= valor

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

fijoConfig('topenodos',1061)