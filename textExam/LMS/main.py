from textExam.LMS.service import *
from textExam.LMS.common import Session

def main():
    MemberService.load()

    run = True
    while run:
        print("""
===== MBC 아카데미 관리 프로그램 =====
1. 회원가입 2. 로그인  3. 로그아웃
4. 회원관리 (관리자 전용)
5. 내 정보 수정 6. 회원 탈퇴 9. 프로그램 종료
""")
        member = Session.login_member
        if member is None:
            print("현재 로그인 상태가 아닙니다.")
        else:
            print(f"{member.name} 님, 환영합니다.")

        sel = input(" >>> ")
        if sel == "1": MemberService.signup()
        elif sel == "2": MemberService.login()
        elif sel == "3": MemberService.logout()
        elif sel == "4": MemberService.admin_menu()
        elif sel == "5": MemberService.modify()
        elif sel == "6": MemberService.delete()
        elif sel == "9":
            print("프로그램을 종료합니다.")
            run = False

if __name__ == "__main__":
    main()