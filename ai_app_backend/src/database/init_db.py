from .connection import Base, engine
from . import models  # noqa: F401 - needed to register models with Base

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    print('Database tables created')
