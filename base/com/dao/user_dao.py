from base import db
from base.com.vo.user_vo import UserVO


class UserDAO:

    def insert_user(self, user_vo):
        db.session.add(user_vo)
        db.session.commit()

    def view_all_users(self):
        return UserVO.query.all()

    def get_by_id(self, user_id):
        return UserVO.query.get(user_id)

    def get_by_email(self, email):
        return UserVO.query.filter_by(email=email).first()

    def update_user(self, user_vo):
        existing = UserVO.query.filter_by(id=user_vo.id).first()
        if existing:
            existing.name = user_vo.name
            existing.email = user_vo.email
            db.session.commit()

    def delete_user(self, user_vo):
        user = UserVO.query.get(user_vo.id)
        db.session.delete(user)
        db.session.commit()