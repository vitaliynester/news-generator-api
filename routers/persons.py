from typing import List

from fastapi import APIRouter, HTTPException

from dto import Person, UpdatePerson, CreatePerson
from services.persons import PersonsService

router = APIRouter(prefix='/api/v1/persons')


@router.get("/",
            tags=['Участники'],
            summary='Получение всех людей',
            status_code=200,
            response_model=List[Person])
async def get_all_persons():
    service = PersonsService()
    data = service.get_all_persons()
    service.down()
    return data


@router.get("/{uuid}",
            tags=['Участники'],
            summary='Получение одной записи',
            status_code=200,
            response_model=Person)
async def get_one_person(uuid: str):
    service = PersonsService()
    data = service.get_one_person(uuid)
    service.down()
    if data is None:
        raise HTTPException(status_code=404, detail='Запись не найдена!')
    return data


@router.post("/",
             tags=['Участники'],
             summary='Создание новой записи',
             status_code=201,
             response_model=Person)
async def create_person(person: CreatePerson):
    service = PersonsService()
    data = service.create_person(person)
    service.down()
    if data is None:
        raise HTTPException(status_code=400, detail='Не удалось создать запись!')
    return data


@router.patch("/{uuid}",
              tags=['Участники'],
              summary='Обновление одной записи',
              status_code=200,
              response_model=Person)
async def update_person(uuid: str, person: UpdatePerson):
    service = PersonsService()
    data = service.update_person(uuid, person)
    service.down()
    if data is None:
        raise HTTPException(status_code=404, detail='Запись не найдена!')
    return data


@router.delete("/{uuid}",
               tags=['Участники'],
               summary='Удаление записи',
               status_code=204,
               response_model=None)
async def remove_person(uuid: str):
    service = PersonsService()
    is_success = service.remove_person(uuid)
    service.down()
    if is_success:
        return
    raise HTTPException(status_code=404, detail='Указанная запись не найдена!')
