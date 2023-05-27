from typing import List

from fastapi import APIRouter, HTTPException

from dto import DetailNews, CreateNews, News
from services.news import NewsService

router = APIRouter(prefix='/api/v1/news')


@router.get('/',
            tags=['Новости'],
            summary='Получение всех новостей',
            status_code=200,
            response_model=List[DetailNews])
async def get_all_news():
    service = NewsService()
    data = service.get_all_news()
    service.down()
    return data


@router.get('/{uuid}',
            tags=['Новости'],
            summary='Получение одной записи',
            status_code=200,
            response_model=DetailNews)
async def get_one_news(uuid: str):
    service = NewsService()
    data = service.get_one_news(uuid)
    service.down()
    if data is None:
        raise HTTPException(status_code=404, detail='Запись не найдена!')
    return data


@router.post('/check',
             tags=['Новости'],
             summary='Проверка существования новости',
             status_code=200,
             response_model=News)
async def check_one_news(dto: CreateNews):
    service = NewsService()
    data = service.check_exists_news(dto)
    service.down()
    if data is None:
        raise HTTPException(status_code=404, detail='Запись не найдена!')
    return data


@router.post('/',
             tags=['Новости'],
             summary='Создание новой новости',
             status_code=200,
             response_model=News)
async def check_one_news(dto: CreateNews):
    service = NewsService()
    data = service.create_news(dto)
    service.down()
    if data is None:
        raise HTTPException(status_code=404, detail='Не удалось сгенерировать новость!')
    return data


@router.delete('/{uuid}',
               tags=['Новости'],
               summary='Удаление записи',
               status_code=204,
               response_model=None)
async def remove_news(uuid: str):
    service = NewsService()
    is_success = service.remove_news(uuid)
    service.down()
    if is_success:
        return
    raise HTTPException(status_code=404, detail='Указанная запись не найдена!')
