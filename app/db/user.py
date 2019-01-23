from . import db
from app.models.user import Users


# 创建用户
def create_user(reg_info):
    new_user = Users(reg_info)
    db.session.add(new_user)
    db.session.commit()


# 查询指定数据
def search(name):
    user = Users.query.filter(Users.username == name).first()
    return user


# 查询所有数据
def get_all():
    all_list = Users.query.all()
    result = []

    for user in all_list:
        result.append(user.to_json())

    return result


# 切换用户状态
def toggle_user_status(id):
    user = Users.query.filter(Users.id == id).first()
    user.status = not user.status
    db.session.commit()
