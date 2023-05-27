import dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import persons, places, weathers, items, news

tags_metadata = [
    {"name": "Участники", "description": "Методы взаимодействия с участниками"},
    {"name": "Места", "description": "Методы взаимодействия с местами"},
    {"name": "Погода", "description": "Методы взаимодействия с сущностью погода"},
    {"name": "Предметы", "description": "Методы взаимодействия с сущностью предмет"},
    {"name": "Новости", "description": "Методы взаимодействия с сущностью новость"},
]
description = "API предоставляющий возможность получения сущностей для базы знаний и формирования на их основе новостей"

dotenv.load_dotenv()

app = FastAPI(
    title="База знаний для формирования новостей",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(persons.router)
app.include_router(places.router)
app.include_router(weathers.router)
app.include_router(items.router)
app.include_router(news.router)
