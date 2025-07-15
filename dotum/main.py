from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from dotum.core.settings import get_settings
from dotum.routes import account, token, user


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(user.router)
app.include_router(account.router)
app.include_router(token.router)
