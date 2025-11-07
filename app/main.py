from fastapi import FastAPI

from app.transport.activity import activity_router
from app.transport.building import building_router
from app.transport.company import company_router
from app.transport.functional import functional_router
from app.transport.telephone import telephone_router

app = FastAPI()

app.include_router(company_router)
app.include_router(building_router)
app.include_router(activity_router)
app.include_router(telephone_router)
app.include_router(functional_router)