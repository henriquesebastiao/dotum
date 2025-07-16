from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from dotum.core.settings import get_settings
from dotum.routes import account, token, user


def custom_generate_unique_id(route: APIRoute):
    return f'{route.tags[0]}-{route.name}'


settings = get_settings()

description = f"""
[![CI](https://github.com/henriquesebastiao/dotum/actions/workflows/test.yml/badge.svg)](https://github.com/henriquesebastiao/dotum/actions/workflows/test.yml)
[![coverage](https://coverage-badge.samuelcolvin.workers.dev/henriquesebastiao/dotum.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/henriquesebastiao/dotum)
[![fastapi](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![postgresql](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

#### Documentação alternativa: [Redoc]({settings.APP_URL}/redoc)

Este projeto é uma solução para um desafio de programação back-end,
cujo objetivo é desenvolver uma aplicação para o controle de contas a pagar e contas a receber.
A proposta foca na construção de uma lógica sólida,
estrutura de código bem organizada e cumprimento dos requisitos funcionais.

Veja o código fonte deste projeto no GitHub [henriquesebastiao/dotum](https://github.com/henriquesebastiao/dotum/).
"""

app = FastAPI(
    docs_url='/',
    generate_unique_id_function=custom_generate_unique_id,
    title='Dotum - Sistema de contas a pagar e contas a receber',
    description=description,
    version=settings.VERSION,
    terms_of_service='https://github.com/henriquesebastiao/dotum/blob/main/LICENSE',
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
