def setup_models(db):
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True)
        date_of_birth = db.Column(db.String(10), unique=True)

        def __init__(self, username, date_of_birth):
            self.username = username
            self.date_of_birth = date_of_birth

        def __repr__(self):
            return f"{self.username}: {self.date_of_birth}"

    class UserDBO(object):
        def get_by_username(self, username):
            return User.query.filter_by(username=username).first()
        def add_birthday(self, username, date_of_birth):
            # if the user exists delete it
            user = self.get_by_username(username)
            if user is not None:
                db.session.delete(user)
                db.session.commit()
            new_user = User(username=username, date_of_birth=date_of_birth)
            db.session.add(new_user)
            db.session.commit()            
            return new_user          

    return UserDBO()
