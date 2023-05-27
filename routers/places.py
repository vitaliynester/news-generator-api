from typing import List

from fastapi import APIRouter, HTTPException

from dto import CreatePlace, UpdatePlace, Place
from services.places import PlacesService

router = APIRouter(prefix='/api/v1/places')


@router.get('/',
            tags=['Места'],
            summary='Получение всех мест',
            status_code=200,
            response_model=List[Place])
async def get_all_places():
    service = PlacesService()
    data = service.get_all_places()
    service.down()
    return data


@router.get('/{uuid}',
            tags=['Места'],
            summary='Получение одной записи',
            status_code=200,
            response_model=Place)
async def get_one_place(uuid: str):
    service = PlacesService()
    data = service.get_one_place(uuid)
    service.down()
    if data is None:
        raise HTTPException(status_code=404, detail='Запись не найдена!')
    return data


@router.post('/',
             tags=['Места'],
             summary='Создание новой записи',
             status_code=201,
             response_model=Place)
async def create_place(place: CreatePlace):
    service = PlacesService()
    data = service.create_place(place)
    service.down()
    if data is None:
        raise HTTPException(status_code=400, detail='Не удалось создать запись!')
    return data


@router.patch('/{uuid}',
              tags=['Места'],
              summary='Обновление одной записи',
              status_code=200,
              response_model=Place)
async def update_place(uuid: str, place: UpdatePlace):
    service = PlacesService()
    data = service.update_place(uuid, place)
    service.down()
    if data is None:
        raise HTTPException(status_code=404, detail='Запись не найдена!')
    return data


@router.delete('/{uuid}',
               tags=['Места'],
               summary='Удаление записи',
               status_code=204,
               response_model=None)
async def remove_place(uuid: str):
    service = PlacesService()
    is_success = service.remove_place(uuid)
    service.down()
    if is_success:
        return
    raise HTTPException(status_code=404, detail='Указанная запись не найдена!')
