import yaml,os
def read_data():
    currentDirectory = os.path.dirname(__file__)
    file_path = currentDirectory +"\data.yml"
    # file_path = r"data/data.yml"
    file_data = open(file_path, 'r', encoding='utf-8')
    conf_data = yaml.load(file_data)
    file_data.close()
    return conf_data

