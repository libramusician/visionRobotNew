from pathlib import Path


def get_project_root_path() -> Path:
    """
    get the root path of this project
    :return: path of the root dir
    """
    return Path(__file__).parent.parent


def rel_path_2_abs(path):
    """
    create the absolute path given relative path
    :param path: the relative path from project root
    :return: absolute path
    """
    root = get_project_root_path()
    return root.joinpath(path)
