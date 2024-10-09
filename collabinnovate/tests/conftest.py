import pytest
from collabinnovate import create_app, db
import os
import tempfile

from collabinnovate.config import TestingConfig
from collabinnovate.manage_user_accounts.user.model import User

@pytest.fixture(scope='module')
def test_client():
    # Configure une application Flask pour les tests
    app = create_app(TestingConfig)

    # Configure la base de données SQLite temporaire
    db_fd, db_path = tempfile.mkstemp(suffix='.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True

    # Active le mode de test
    with app.test_client() as testing_client:
        with app.app_context():
            # Crée toutes les tables nécessaires dans la base de données de test
            db.create_all()
            yield testing_client  # Ceci retourne l'application de test pour les tests à utiliser

    # Nettoyage après les tests : supprime la base de données
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    # Créer un utilisateur de test
    user = User(email="test_user@example.com",username='test_username', full_name="Test Fullname",role_id=1,group_id=1,password='2852003Max#',)
    db.session.add(user)
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()
