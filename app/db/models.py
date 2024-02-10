from typing import Optional
from pydantic import BaseModel, Field


class HashableBaseModel(BaseModel):
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

class User(HashableBaseModel):
    email: str
    name: str
    discord: str

class Pairing(HashableBaseModel):
    id: int
    user1_email: str
    user2_email: str
    question1_id: int
    question2_id: int

class Question(HashableBaseModel):
    id: int
    question_url: str

class Form(HashableBaseModel):
    id: str
    name: str
    email_response_id: str
    discord_response_id: str
    name_response_id: str

class FormResponse(HashableBaseModel):
    id: int
    form_id: int
    user_email: str

