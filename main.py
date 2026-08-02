from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy import create_engine,Column,Integer,String,Boolean
from sqlalchemy.orm import sessionmaker,declarative_base,Session
from pydantic import BaseModel,EmailStr
from datetime import datetime, timedelta, timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

app=FastAPI()
Base=declarative_base()

class User(Base):
    __tablename__ = "users"  # Added required table name for SQLAlchemy
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)


class Task(Base):
    __tablename__ = "tasks"  # Added required table name for SQLAlchemy
    id=Column(Integer,primary_key=True)
    title=Column(String)
    completed=Column(Boolean)
    owner_id=Column(Integer)

DATABASE_URL = "sqlite:///./task.db"

engine=create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # Added SQLite thread configuration

sessionLocal=sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")


def get_db():                            
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class TaskCreate(BaseModel):
    title: str
class TaskUpdate(BaseModel):
    title: str
    completed: bool
class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

Pwd_contex=CryptContext(schemes=["bcrypt"],deprecated="auto")


def hashed_password(password):
    return Pwd_contex.hash(password)


def verify_password(password:str,hashed_password:str):
    return Pwd_contex.verify(password,hashed_password)


def access_token(data:dict):
    to_encode=data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exceptions=HTTPException(status_code=404,
                                    detail="invalid credentials")
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email=payload.get("sub")
        if email is None:
            raise credentials_exceptions
    except JWTError:
        raise credentials_exceptions

    user=db.query(User).filter(User.email==email).first()

    if user is None:
        raise credentials_exceptions

    return user


@app.post("/user")
def register(user:UserCreate,db:Session=Depends(get_db)):

    existing_user=db.query(User).filter(User.email==user.email).first()

    if existing_user:
        raise HTTPException(status_code=400,detail="user is already registered")

    hash_password=hashed_password(user.password)

    new_user=User(username=user.username,email=user.email,hashed_password=hash_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):

    user=db.query(User).filter(User.email==form_data.username).first()

    if user is None:
        raise HTTPException(status_code=400,detail="user is not registered")

    v=verify_password(form_data.password,user.hashed_password)

    if v is False:
        raise HTTPException(status_code=401,detail="incorrect password")

    a=access_token({"sub":user.email})

    return {
        "access_token": a,
        "token_type": "bearer"
    }

@app.post("/taskcreate")
def create_task(task:TaskCreate,current_user:User=Depends(current_user),db:Session=Depends(get_db)):
    new_task=Task(title=task.title,completed=False,owner_id=current_user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.get("/tasks")
def get_alltasks(current_user:User=Depends(current_user),db:Session=Depends(get_db)):

    task=db.query(Task).filter(Task.owner_id==current_user.id).all()

    return task

@app.put("/updatetask/{task_id}")
def Update_task(task_id:int,updated_task:TaskUpdate,current_user:User=Depends(current_user),db:Session=Depends(get_db)):

    task=db.query(Task).filter(Task.id==task_id,Task.owner_id==current_user.id).first()

    if task is None:
        raise HTTPException(status_code=404,detail="Task not found")

    task.title = updated_task.title
    task.completed = updated_task.completed

    
    db.commit()
    db.refresh(task)

    return task

@app.delete("/task/{task_id}")
def delete_task(task_id:int,current_user:User=Depends(current_user),db:Session=Depends(get_db)):
    task=db.query(Task).filter(Task.id==task_id,Task.owner_id==current_user.id).first()

    if task is None:
        raise HTTPException(status_code=404,detail="task not found")

    db.delete(task)
    db.commit()

    return {"message":"task deleted successfully"}
    






