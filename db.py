from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.engine import URL


# Uso de libreria dotenv para mantener segura la informacion sensible de la base de datos
from dotenv import load_dotenv
import os
load_dotenv()

### Creacion del motor y enlace a la BD
url = URL.create(
    drivername = "mysql+mysqldb",
    username = os.environ.get('USER_MYSQL'),
    password = os.environ.get('PASS_MYSQL'),
    host = os.environ.get('HOST_MYSQL'),
    database = "pruebaonline",
    port = "3306"
)
engine = create_engine(url)
## Tenemos estas dos formas de crear el engine
# username = os.environ.get('USER_MYSQL')
# password = os.environ.get('PASS_MYSQL')
# host = os.environ.get('HOST_MYSQL')
# engine = create_engine(f"mysql+mysqldb://{username}:{password}@{host}/pruebaonline")


### Definimos el modelo
Base = declarative_base()
# Definir una tabla como una clase
class Palabras(Base):
    __tablename__ = 'palabras'
    palabra_id = Column(Integer, primary_key=True)
    palabra_ingles = Column(String)
    traduccion = Column(String)
    fecha_insercion = Column(TIMESTAMP, default=func.now())
# Creamos la tabla (si ya existe solo la enlaza)
Base.metadata.create_all(engine)


### Creamos la sesion (esta es la que interactua con la BD)
Session = sessionmaker(bind=engine)
session = Session()