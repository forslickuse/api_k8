from pydantic import BaseModel, Field

import constants

class Person(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str = Field(min_length=constants.MIN_EMAIL_LENGTH, max_lengh=constants.MAX_EMAIL_LENGTH)

class BasicPerson(BaseModel):
    first_name: str
    last_name: str
    email: str = Field(min_length=constants.MIN_EMAIL_LENGTH, max_lengh=constants.MAX_EMAIL_LENGTH)
