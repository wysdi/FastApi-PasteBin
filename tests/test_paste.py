from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from datetime import datetime, date, timedelta
import uuid
import secrets
from app.database import Base
from app.main import app
from app.router import get_db
from app.models import Paste

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"
fake = Faker()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_creating_paste():
    content = fake.paragraph(nb_sentences=5)
    response = client.post(
        "/paste",
        json={"content": content},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "paste_id" in data
    paste_id = data["paste_id"]

    response = client.get(f"/paste/{paste_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["content"] == content


def test_creating_paste_with_expired_set():
    current = datetime.today()
    expired_at = current + timedelta(hours=2)
    content = fake.paragraph(nb_sentences=5)
    response = client.post(
        "/paste",
        json={"content": content, "expired_at": expired_at.isoformat()}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['expired_at'] == expired_at.isoformat()


def test_updating_paste():
    db = TestingSessionLocal()
    paste_id = db.query(Paste).first().paste_id
    content = fake.paragraph(nb_sentences=5)
    response = client.patch(
        "/paste/"+paste_id,
        json={"content": content}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['content'] == content


def test_updating_paste_expired_at():
    db = TestingSessionLocal()
    paste_id = db.query(Paste).first().paste_id
    content = fake.paragraph(nb_sentences=5)
    current = datetime.today()
    expired_at = current + timedelta(hours=2)
    response = client.patch(
        "/paste/"+paste_id,
        json={"content": content, "expired_at": expired_at.isoformat()}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['expired_at'] == expired_at.isoformat()


def test_deleting_paste():
    db = TestingSessionLocal()
    paste_id = db.query(Paste).first().paste_id
    response = client.delete(
        "/paste/"+paste_id
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['status'] == 'OK'


def test_deleting_paste_not_exist():
    response = client.delete(
        "/paste/" + str(uuid.uuid4())
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data['detail'] == 'Unable To Delete'

def test_access_public_paste():
    db = TestingSessionLocal()
    paste = db.query(Paste).first()
    current = datetime.today()
    setattr(paste, 'expired_at',  current + timedelta(hours=6))
    db.add(paste)
    db.commit()
    db.refresh(paste)

    response = client.get(
        "/" + paste.url
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data == paste.content


def test_access_expired_paste():
    db = TestingSessionLocal()
    paste = db.query(Paste).first()
    current = datetime.today()
    setattr(paste, 'expired_at',  current - timedelta(hours=6))
    db.add(paste)
    db.commit()
    db.refresh(paste)

    response = client.get(
        "/" + paste.url
    )

    assert response.status_code == 400, response.text
    data = response.json()
    assert data['detail'] == 'Paste is already expired'


def test_access_notfound_paste():
    response = client.get(
        "/" + secrets.token_urlsafe(10)
    )

    assert response.status_code == 400, response.text
    data = response.json()
    assert data['detail'] == 'Paste not exist'