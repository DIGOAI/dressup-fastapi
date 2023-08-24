import os

from dotenv import load_dotenv


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    def __init__(self):
        if os.getenv("ENV") == "dev":
            print("Loading DEV config")
            load_dotenv('.env.dev')
        else:
            print("Loading PROD config")
            load_dotenv()

        self.SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
        self.SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
        self.SUPABASE_BUCKET: str = os.getenv(
            "SUPABASE_BUCKET", "dressupbucket")
        self.X_API_KEY: str = os.getenv("X_API_KEY", "")
        self.X_API_KEY_NAME: str = os.getenv("X_API_KEY_NAME", "X-API-KEY")
        self.JWT_SECRET = os.getenv("JWT_SECRET", "")
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
        self.DEBUG = os.getenv("DEBUG", "False") == "True"
        self.ORDER_COST = float(os.getenv("ORDER_COST", "3.50"))
        self.ALLOWED_ORIGINS = [url.strip() for url in os.getenv(
            "ALLOWED_ORIGINS", "*").split(",")]
