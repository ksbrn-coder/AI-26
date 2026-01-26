class Session:
    login_member = None

    @classmethod
    def login(cls, member):
        cls.login_member = member

    @classmethod
    def logout(cls):
        cls.login_member = None

    @classmethod
    def is_login(cls):
        return cls.login_member is not None

    @classmethod
    def is_admin(cls):
        return cls.is_login() and cls.login_member.is_admin()

    @classmethod
    def is_manager(cls):
        return cls.is_login() and cls.login_member.is_manager()