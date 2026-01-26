class Member:

    def __init__(self, uid, pw, name, role = "user", active = True):
        self.uid = uid
        self.pw = pw
        self.name = name
        self.role = role
        self.active = active

    def __str__(self):
        status = "활성" if self.active else "비활성"
        return f"{self.uid}|{self.name}|{self.role}|{status}"

    def to_line(self):
        return f"{self.uid}|{self.pw}|{self.name}|{self.role}|{self.active}"

    @staticmethod
    def from_line(line: str):
        uid, pw, name, role, active = line.strip().split("|")
        return Member(
            uid = uid,
            pw = pw,
            name = name,
            role = role,
            active = (active == "True")
        )

    def is_admin(self):
        return self.role == "admin"

    def is_manager(self):
        return self.role == "manager"