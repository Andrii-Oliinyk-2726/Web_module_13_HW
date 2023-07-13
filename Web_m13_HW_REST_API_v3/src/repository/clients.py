from sqlalchemy.orm import Session

from src.schemas import ClientResponse, ClientModel
# from src.database.models import User
from src.database.models import Client


async def get_clients(db: Session):
    clients = db.query(Client).all()
    return clients


async def get_client_by_id(client_id: int, db: Session):
    client = db.query(Client).filter_by(id=client_id).first()
    return client


async def get_client_by_email(email: str, db: Session):
    client = db.query(Client).filter_by(email=email).first()
    return client


async def create(body: ClientModel, db: Session):
    client = Client(**body.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


async def update(client_id: int, body: ClientModel, db: Session):
    client = await get_client_by_id(client_id, db)
    if client:
        client.first_name = body.first_name
        client.last_name = body.last_name
        client.email = body.email
        client.mobile = body.mobile
        client.birthday = body.birthday
        client.add_info = body.add_info
        db.commit()
    return client


async def remove(client_id: int, db: Session):
    client = await get_client_by_id(client_id, db)
    if client:
        db.delete(client)
        db.commit()
    return client

