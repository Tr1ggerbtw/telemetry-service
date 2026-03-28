import pytest
from app import create_app
from app.db import db

@pytest.fixture()
def client():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": 'sqlite:///:memory:'
    })
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()