from typing import List

from fastapi import APIRouter, HTTPException

from dto import Item, CreateItem, UpdateItem
from services.items import ItemsService

router = APIRouter(prefix='/api/v1/items')


@router.get('/',
            tags=['Предметы'],
            summary='Получение всех предметов',
            status_code=200,
            response_model=List[Item])
async def get_all_items():
    service = ItemsService()
    data = service.get_all_items()
    service.down()
    return data


@router.get('/{uuid}',
            tags=['Предметы'],
            summary='Получение одной записи',
            status_code=200,
            response_model=Item)
async def get_one_item(uuid: str):
    service = ItemsService()
    data = service.get_one_item(uuid)
    service.down()
    if data is None:
        raise HTTPException(status_code=404, detail='Запись не найдена!')
    return data


@router.post('/',
             tags=['Предметы'],
             summary='Создание новой записи',
             status_code=201,
             response_model=Item)
async def create_place(place: CreateItem):
    service = ItemsService()
    data = service.create_item(place)
    service.down()
    if data is None:
        raise HTTPException(status_code=400, detail='Не удалось создать запись!')
    return data


@router.patch('/{uuid}',
              tags=['Предметы'],
              summary='Обновление одной записи',
              status_code=200,
              response_model=Item)
async def update_place(uuid: str, place: UpdateItem):
    service = ItemsService()
    data = service.update_item(uuid, place)
    service.down()
    if data is None:
        raise HTTPException(status_code=404, detail='Запись не найдена!')
    return data


@router.delete('/{uuid}',
               tags=['Предметы'],
               summary='Удаление записи',
               status_code=204,
               response_model=None)
async def remove_place(uuid: str):
    service = ItemsService()
    is_success = service.remove_item(uuid)
    service.down()
    if is_success:
        return
    raise HTTPException(status_code=404, detail='Указанная запись не найдена!')
