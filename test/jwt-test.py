from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 5
SECRET = "0373fe2d7be51cdc4fb34a928c94721118a5123c84d16bb4345f4d40efecbd2a"

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# cryptContext para encriptar y desencriptar nuestros datos
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "teqnobit": {
        "username": "teqnobit",
        "fullname": "Ariel Tequida",
        "email": "ariel.tequida@gmail.com",
        "disabled": False,
        "password": "$2a$12$pp7/LSr382U1LdACVa/BSeTd2U7XpXhk4QkzXr8qsrPQi7ptNBaaC"
    },
    "teqnobit2": {
        "username": "teqnobit2",
        "fullname": "Ariel Tequida2",
        "email": "ariel.tequida2@gmail.com",
        "disabled": True,
        "password": "$2a$12$THFUs8xfR5v6wp5ax.CQyujL/tGjGVDayotP4kvTrJrBpJcJTxXOi"
    }
}

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticacion invalidas",
        headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        # Pieza clave de la autenticacion por jwt
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")

        if username is None:
            raise exception

    except JWTError:
        raise exception
    
    return search_user(username)
    
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario Inactivo"
        )
    return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400,
            detail="El usuario no es correcto"
        )
    
    user = search_user_db(form.username)

            # Uso del encriptado
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, 
            detail="La contraseña no es correcta"
        )
    
    # access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)

    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION) ## Obsoleto
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {
        "sub": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }

    return {            # pieza clave de jwt
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM, ), 
        "token_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user