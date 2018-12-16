from app import create_app
from app.db import db
from app.routes.user import users

app = create_app()
# 初始化上下文
with app.app_context():
    db.init_app(app)
    db.create_all()

# 路由注册
app.register_blueprint(users, url_prefix="/api/user")

if __name__ == '__main__':
    app.run(host='localhost', port=4000)
