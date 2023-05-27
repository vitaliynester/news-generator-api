from typing import List

from fastapi import APIRouter, HTTPException

from dto import CreateWeather, UpdateWeather, Weather
from services.weathers import WeathersService

router = APIRouter(prefix='/api/v1/weathers')


@router.get('/',
            tags=['Погода'],
            summary='Получение всех записей',
            status_code=200,
            response_model=List[Weather])
async def get_all_weathers():
    service = WeathersService()
    data = service.get_all_weathers()
    service.down()
    return data


@router.get('/{uuid}',
            tags=['Погода'],
            summary='Получение одной записи',
            status_code=200,
            response_model=Weather)
async def get_one_weather(uuid: str):
    service = WeathersService()
    data = service.get_one_weather(uuid)
    service.down()
    if data is None:
        raise HTTPException(status_code=404, detail='Запись не найдена!')
    return data


@router.post('/',
             tags=['Погода'],
             summary='Создание новой записи',
             status_code=201,
             response_model=Weather)
async def create_weather(weather: CreateWeather):
    service = WeathersService()
    data = service.create_weather(weather)
    service.down()
    if data is None:
        raise HTTPException(status_code=400, detail='Не удалось создать запись!')
    return data


@router.patch('/{uuid}',
              tags=['Погода'],
              summary='Обновление одной записи',
              status_code=200,
              response_model=Weather)
async def update_weather(uuid: str, weather: UpdateWeather):
    service = WeathersService()
    data = service.update_weather(uuid, weather)
    service.down()
    if data is None:
        raise HTTPException(status_code=404, detail='Запись не найдена!')
    return data


@router.delete('/{uuid}',
               tags=['Погода'],
               summary='Удаление записи',
               status_code=204,
               response_model=None)
async def remove_weather(uuid: str):
    service = WeathersService()
    is_success = service.remove_weather(uuid)
    service.down()
    if is_success:
        return
    raise HTTPException(status_code=404, detail='Указанная запись не найдена!')
