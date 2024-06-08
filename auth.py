from db import db_session
from db.users import User
from werkzeug.security import generate_password_hash, check_password_hash

db_session.global_init('db/database.db')


def register(name: str, psw: str, psw_again: str) -> str | dict:
    if psw != psw_again:
        return 'Пароли не совпадают'
    if len(psw) < 8:
        return 'Пароль слишком короткий'
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.name == name).first():
        return "Имя занято"
    user = User()
    user.name = name
    user.password_hash = generate_password_hash(psw)
    db_sess.add(user)
    db_sess.commit()
    return {'name': name, 'score': 0}


def login(name: str, psw: str) -> str | dict:
    if len(psw) < 8:
        return 'Неправильное имя пользователя или пароль'
    db_sess = db_session.create_session()
    user: None | User = db_sess.query(User).filter(User.name == name).first()
    if not user or not check_password_hash(user.password_hash, psw):
        return 'Неправильное имя пользователя или пароль'
    return {'name': user.name, 'score': user.score}


def add_score(name: str, score: int):
    db_sess = db_session.create_session()
    user: User | None = db_sess.query(User).filter(User.name == name).first()
    if user:
        try:
            user.score += score
            db_sess.commit()
            print(f'Успешно добавлено {score} очков пользавтелю {name}')
        except Exception as e:
            print(f'Возникла ошибка {e} при добавлении {score} очков пользователю {name}')
    else:
        print(f'Пользователь {name} не найден')
