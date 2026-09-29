from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from core.database import get_session
from core.security import get_password_hash
from elbicho.models import User
from elbicho.schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    # Verificar email
    statement = select(User).where(User.email == user.email)
    if db.exec(statement).first():
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Verificar username
    statement = select(User).where(User.username == user.username)
    if db.exec(statement).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

    # Hashear contraseña
    hashed_password = get_password_hash(user.password)

    # Crear usuario
    db_user = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        hashed_password=hashed_password,
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_session)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = user_update.model_dump(exclude_unset=True)

    # Si se actualiza la contraseña, la hasheamos
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user