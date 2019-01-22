from . import db
from app.models.user import User


# 创建用户
def create_user(reg_info):
    new_user = User(reg_info)
    db.session.add(new_user)
    db.session.commit()
    db.session.close()


# 查询指定数据
def search(name):
    user = User.query.filter(User.username == name).first()
    return user


# 查询所有数据
def get_all():
    all_list = User.query.all()
    result = []

    for user in all_list:
        result.append(user.to_json())

    return result


# 切换用户状态
def toggle_user_status(id):
    user = User.query.filter(User.id == id).first()
    user.status = not user.status
    db.session.commit()
    db.session.close()
