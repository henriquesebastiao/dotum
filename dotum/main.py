from fastapi import FastAPI
from fastapi.routing import APIRoute

from dotum.core.settings import get_settings


def custom_generate_unique_id(route: APIRoute):
    return f'{route.tags[0]}-{route.name}'


settings = get_settings()

description = f"""
Dotum
#### Documentação alternativa: [Redoc]({settings.APP_URL}/redoc)
"""

app = FastAPI(
    docs_url='/',
    generate_unique_id_function=custom_generate_unique_id,
    title='Dotum',
    description=description,
    version=settings.VERSION,
    terms_of_service='https://github.com/henriquesebastiao/dotum/',
    contact={
        'name': 'Dotum',
        'url': 'https://github.com/henriquesebastiao/dotum',
        'email': 'contato@henriquesebastiao.com',
    },
)
