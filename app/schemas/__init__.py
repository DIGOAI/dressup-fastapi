from pydantic import BaseModel
from pydantic.networks import Email


class Login(BaseModel):
    email: Email
    password: int

class Author(BaseModel):
    name: str
    age: int
