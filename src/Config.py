import json

def __get_config():
    config_file = open('./config/config.json', encoding='utf-8')
    config = json.load(config_file)
    config_file.close()
    
    return config

def get_settings():
    config = __get_config()
    return config['SETTINGS']

def get_layout_options():
    config = __get_config()
    return config['LAYOUT']