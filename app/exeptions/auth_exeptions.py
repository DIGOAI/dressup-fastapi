from gotrue.errors import AuthApiError
from storage3.utils import StorageException


class SupabaseException(Exception):
    def __init__(self, error: AuthApiError) -> None:
        self.name = error.name
        self.message = error.message
        self.status_code = error.status
