import os


def join_normalize(*args):
    return os.path.normpath(os.path.join(*args))


def get_backend_base():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_root_dir():
    return os.path.dirname(get_backend_base())


def get_data_dir():
    return join_normalize(get_backend_base(), "data")


def get_tmp_dir():
    return join_normalize(get_data_dir(), "tmp")


def default_env_file():
    return join_normalize(get_root_dir(), ".env.defaults")


def default_secrets_file():
    return join_normalize(get_root_dir(), ".env.secrets_defaults")


def secrets_file():
    return join_normalize(get_root_dir(), ".env.secrets")


def load_env():
    import dotenv

    # Loads the secrets of the .env.secrets
    dotenv.load_dotenv(default_env_file(), override=False)
    dotenv.load_dotenv(default_secrets_file(), override=True)
    dotenv.load_dotenv(secrets_file(), override=True)

    return True
