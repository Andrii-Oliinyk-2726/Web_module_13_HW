from datetime import date, timedelta
from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy import extract
from sqlalchemy.orm import Session

from src.schemas import ClientResponse, ClientModel
from src.database.db import get_db
from src.database.models import Client, User, Role
from src.repository import clients as repository_clients
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix="/clients", tags=['clients'])

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator])
allowed_operation_remove = RoleAccess([Role.admin])


@router.get("/", response_model=List[ClientResponse], name="All clients:",
            dependencies=[Depends(allowed_operation_get), Depends(RateLimiter(times=2, seconds=5))])
async def get_clients(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    clients = await repository_clients.get_clients(db)
    return clients


@router.get("/birthday", response_model=List[ClientResponse], name="Congratulate:",
            dependencies=[Depends(allowed_operation_get)])
async def get_clients_by_birth_date(start_date: date = Query(default=date.today()),
                                    end_date: date = Query(default=(date.today() + timedelta(days=7))),
                                    db: Session = Depends(get_db),
                                    current_user: User = Depends(auth_service.get_current_user)):
    clients = db.query(Client).filter(extract('day', Client.birthday) >= start_date.day,
                                      extract('month', Client.birthday) >= start_date.month,
                                      extract('day', Client.birthday) <= end_date.day,
                                      extract('month', Client.birthday) <= end_date.month).all()
    return clients


@router.get("/{client_id}", response_model=ClientResponse, dependencies=[Depends(allowed_operation_get)])
async def get_client(client_id: int = Path(ge=1), db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    client = await repository_clients.get_client_by_id(client_id, db)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return client


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_operation_create)], description='Only moderators and admin')
async def create_client(body: ClientModel, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    client = await repository_clients.get_client_by_email(body.email, db)
    if client:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is exists!')
    client = await repository_clients.create(body, db)
    return client


@router.put("/{client_id}", response_model=ClientResponse, dependencies=[Depends(allowed_operation_update)])
async def update_client(body: ClientModel, client_id: int = Path(ge=1), db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    # user = db.query(User).filter_by(id=user_id).first()
    client = await repository_clients.update(client_id, body, db)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allowed_operation_remove)])
async def remove_client(client_id: int = Path(ge=1), db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    client = await repository_clients.remove(client_id, db)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return client
