import os
import sqlite3
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

import constants, tasks
from models import BasicPerson, Person

# clean test.db on [re]start for testing purposes
# if os.path.isfile('./test.db'):
#    os.remove('./test.db')

DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

persons = sqlalchemy.Table('persons', metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column('first_name', sqlalchemy.String, nullable=False, index=True),
    sqlalchemy.Column('last_name', sqlalchemy.String, nullable=False, index=True),
    sqlalchemy.Column('email', sqlalchemy.String(constants.MAX_EMAIL_LENGTH), index=True, nullable=False, unique=True),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Routes
async def get_person_data(id):
    query = persons.select().where(persons.c.id == id)
    res = await database.fetch_one(query)
    if res == -1 or not res or len(res) == 0:
        return None

    return dict(res)


@app.get("/")
async def root():
    return {"message": "Server is alive"}


@app.get('/person/{id}')
async def read_person(id: int):
    data = await get_person_data(id)
    if not data:
        raise HTTPException(status_code=404, detail="Person not found")

    return {'id': id, 'email': data['email']}


@app.post('/person/', response_model=Person)
async def create_person(person: BasicPerson, background_tasks: BackgroundTasks):
    f_name = person.first_name
    l_name = person.last_name
    email = person.email

    # Create person
    try:
        query = persons.insert().values(first_name=f_name,last_name=l_name, email=email)
        created_id = await database.execute(query)
    except sqlite3.IntegrityError as e:
        print('Error:', e)  # log error for internal purposes
        raise HTTPException(status_code=409, detail="Account already exists.")

    # Background task
    background_tasks.add_task(tasks.send_email, email, f_name, l_name)

    return {**person.dict(), 'id': created_id}


@app.put('/person/{id}', response_model=Person)
async def update_person(id: int, person: BasicPerson):
    f_name = person.first_name
    l_name = person.last_name
    email = person.email

    # Update only if account exists
    data = await get_person_data(id)
    if data:
        query = persons.update()\
            .where(persons.c.id == id)\
            .values(first_name=f_name,last_name=l_name, email=email)  # should decide which fields can be updated
        last_record_id = await database.execute(query)
    else:
        raise HTTPException(status_code=404, detail="Person not found")

    return {**person.dict(), 'id': last_record_id}
