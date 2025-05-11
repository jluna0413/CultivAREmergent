from flask_login import AnonymousUserMixin

class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.id = 1
        self.username = \ Guest User\
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return str(self.id)
