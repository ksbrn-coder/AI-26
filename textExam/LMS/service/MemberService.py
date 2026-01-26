import os
from textExam.LMS.common import Session
from textExam.LMS.domain import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "..", "data", "member.txt")

class MemberService:
    members = []

    @classmethod
    def load(cls):
        cls.members = []
        if not os.path.exists(FILE_PATH):
            cls.save()
            return

        with open(FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                cls.members.append(Member.from_line(line))

    @classmethod
    def save(cls):
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            for m in cls.members:
                f.write(m.to_line() + "\n")

    @classmethod
    def login(cls):
        print("\n [로그인]")

        uid = input("아이디 : ")
        pw = input("비밀번호 : ")

        for m in cls.members:
            if m.uid == uid:
                if not m.active :
                    print("비활성화 처리된 계정입니다. 관리자에게 문의하세요.")
                    return

                if m.pw == pw:
                    Session.login(m)
                    print(f"{m.name} 님, 환영합니다. (권한 : {m.role})")
                    return


                else :
                    print("비밀번호가 일치하지 않습니다.")
                    return

        else :
            print("존재하지 않는 아이디입니다.")

    @classmethod
    def logout(cls):
        if not Session.is_login():
            print("로그인 후 이용 가능합니다.")
            return

        logout = input("정말 로그아웃하시겠습니까? (y/n) : ")
        if logout == "y":
            Session.logout()
            print("로그아웃 되었습니다.")
        else :
            return

    @classmethod
    def signup(cls):
        if Session.is_login():  # 회원가입 전 로그인 상태일 경우 로그아웃을 유도하도록 설정
            print("이미 로그인된 상태입니다. 로그아웃 후 이용해 주세요.")
            return
        print("\n[회원가입]")
        uid = input("아이디 : ")
        if any(m.uid == uid for m in cls.members):
            print("이미 존재하는 아이디입니다.")
            return
        pw = input("비밀번호 : ")
        name = input("이름 : ")
        member = Member(uid, pw, name)
        cls.members.append(member)
        cls.save()

        print(f"회원가입이 완료되었습니다. {name} 님, 환영합니다.")

    @classmethod
    def modify(cls):
        if not Session.is_login():
            print("로그인 후 이용해 주세요.")
            return

        member = Session.login_member
        old_name = member.name # 기존 이름, 비밀번호가 같이 뜨도록 변수 설정
        old_pw = member.pw

        print("""
\n[내 정보 수정]
1. 이름 변경
2. 비밀번호 변경
3. 취소        
""")
        sel = input(" >>> ")

        if sel == "1":
            member.name = input("새 이름 : ")
            selname = input(f"""입력하신 이름이 맞습니까?
(기존 이름 : {old_name} / 새 이름 : {member.name})
(y/n) : """)
            if selname == "y" :
                cls.save()
            else :
                return

        elif sel == "2":
            member.pw = input("새 비밀번호 : ")
            selpw = input(f"""입력하신 비밀번호가 맞습니까?
(기존 비밀번호 : {old_pw} / 새 비밀번호 : {member.pw})
(y/n) : """)
            if selpw == "y" :
                cls.save()
            else :
                return

        else :
            print("잘못 입력하셨습니다. 다시 입력해 주세요.")
            return

        print("정보 수정이 완료되었습니다.")


    @classmethod
    def delete(cls):
        if not Session.is_login():
            print("로그인 후 이용 가능합니다.")
            return

        member = Session.login_member
        print("""
\n[회원 탈퇴]
1. 완전 탈퇴
2. 비활성화 (30일 후 완전 탈퇴 처리)
""")
        sel = input(" >>> ")

        if sel == "1":
            del_sel = input("정말 탈퇴하시겠습니까? (y/n) : ")
            if del_sel == "y" :
                cls.members.remove(member)
                Session.logout()
                cls.save()
                print("회원 탈퇴 처리가 완료되었습니다.")
            else :
                return

        elif sel == "2":
            false_sel = input("정말 비활성화 하시겠습니까? 30일 후에는 복구할 수 없습니다. (y/n) : ")
            if false_sel == "y" :
                member.active = False
                Session.logout()
                cls.save()
                print("비활성화 처리가 완료되었습니다.")
            else :
                return

    @classmethod
    def admin_menu(cls):
        if not Session.is_login() or not Session.is_admin():
            print("권한이 없습니다.")
            return

        while True:
            print("""\n[관리자 메뉴]
1. 회원 목록 조회
2. 권한 변경
3. 블랙리스트 처리 (비활성화)""")

            sel = input(" >>> ")

            if sel == "1":
                cls.list_members()
            elif sel == "2":
                result = cls.change_role()
                if result == "logout":
                    return
            elif sel == "3":
                cls.block_member()
            else :
                return

    @classmethod
    def list_members(cls):
        print("\n[회원 목록]")
        for m in cls.members :
            print(m)

    @classmethod
    def change_role(cls):
        uid = input("대상자 아이디 : ")
        for m in cls.members :
            if m.uid == uid :
                m.role = input("admin / manager / user : ")
                if m.role == "admin" : # 관리자 권한 위임 설정 (본인은 user로)
                    admin_role = input("정말 권한을 위임하시겠습니까? (y/n) : ")
                    if admin_role == "y" :
                        Session.login_member.role = "user"
                        cls.save()
                        Session.logout()
                        print("권한 위임 완료. 로그아웃 처리됩니다.")
                        return "logout"
                else :
                    cls.save()
                    print("권한 위임 완료되었습니다.")
                cls.save()

    print("찾는 회원이 없습니다.")


    @classmethod
    def block_member(cls):
        uid = input("대상 아이디 : ")
        for m in cls.members :
            if m.uid == uid :
                m.active = False
                cls.save()
                print(f"비활성화 처리가 완료되었습니다. ({m.uid} : {m.active})")