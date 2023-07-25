import os


def read_file(filename: str) -> list:
    """Функция чтения из файла"""

    path = os.path.join(os.path.dirname(os.getcwd()), 'configs', filename)

    with open(path, 'r') as f:
        data = f.read().splitlines()
        f.close()

    return data
