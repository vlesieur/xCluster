from index import db, bcrypt, app


class Users(db.Document):
    login = db.StringField(max_length=255, required=True, unique=True, index=True)
    mail = db.StringField(max_length=255, required=True, unique=True, index=True)
    password = db.StringField(max_length=255, required=True)

    @staticmethod
    def get_user_with_login_and_password(login, password):
        user = Users.objects.get(login=login)
        app.logger.info('%s user', user.login)
        app.logger.info('%s user', user.password)
        app.logger.info('%s user', user.mail)
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None
        
    def save(self, *args, **kwargs):
       
        if not self.id and self.password:
            self.password = bcrypt.generate_password_hash(self.password).decode('utf-8')
            print (self.password)
        super(Users, self).save(*args, **kwargs)