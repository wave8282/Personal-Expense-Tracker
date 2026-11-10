
import json
import os
from datetime import date, datetime

FILE_NAME = "expense_data.json"


def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("데이터 파일을 읽을 수 없습니다.")
    return []


def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def input_amount():
    try:
        amount = int(input("금액(원): ").replace(",", ""))
        if amount <= 0:
            print("금액은 0보다 커야 합니다.")
            return None
        return amount
    except ValueError:
        print("올바른 금액을 입력해 주세요.")
        return None


def add_record(data):
    print("\n1. 수입")
    print("2. 지출")
    choice = input("구분 선택: ")

    if choice == "1":
        record_type = "수입"
    elif choice == "2":
        record_type = "지출"
    else:
        print("잘못된 선택입니다.")
        return

    amount = input_amount()
    if amount is None:
        return

    category = input("분류: ").strip()
    memo = input("내용: ").strip()

    if not category:
        print("분류를 입력해 주세요.")
        return

    record = {
        "date": date.today().isoformat(),
        "type": record_type,
        "amount": amount,
        "category": category,
        "memo": memo
    }

    data.append(record)
    save_data(data)
    print("거래 내역이 저장되었습니다!")


def show_records(data):
    if not data:
        print("등록된 내역이 없습니다.")
        return

    print("\n===== 거래 내역 =====")

    for i, record in enumerate(data, 1):
        print(f"\n{i}. 날짜: {record['date']}")
        print(f"   구분: {record['type']}")
        print(f"   금액: {record['amount']:,}원")
        print(f"   분류: {record['category']}")
        print(f"   내용: {record['memo']}")


def show_summary(data):
    income = sum(r["amount"] for r in data if r["type"] == "수입")
    expense = sum(r["amount"] for r in data if r["type"] == "지출")

    print("\n===== 전체 통계 =====")
    print(f"총수입: {income:,}원")
    print(f"총지출: {expense:,}원")
    print(f"현재 잔액: {income - expense:,}원")


def show_monthly_summary(data):
    month = input("조회할 월(YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("YYYY-MM 형식으로 입력해 주세요.")
        return

    records = [r for r in data if r["date"].startswith(month)]

    income = sum(r["amount"] for r in records if r["type"] == "수입")
    expense = sum(r["amount"] for r in records if r["type"] == "지출")

    print(f"\n===== {month} 통계 =====")
    print(f"수입: {income:,}원")
    print(f"지출: {expense:,}원")
    print(f"잔액: {income - expense:,}원")


def delete_record(data):
    if not data:
        print("삭제할 내역이 없습니다.")
        return

    show_records(data)

    try:
        number = int(input("삭제할 내역 번호: "))

        if number < 1 or number > len(data):
            print("올바른 번호를 입력해 주세요.")
            return

        deleted = data.pop(number - 1)
        save_data(data)
        print(f"{deleted['category']} 내역이 삭제되었습니다!")

    except ValueError:
        print("숫자로 입력해 주세요.")


def main():
    data = load_data()

    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. 수입 및 지출 등록")
        print("2. 전체 내역 조회")
        print("3. 전체 잔액 및 통계")
        print("4. 월별 통계")
        print("5. 거래 내역 삭제")
        print("0. 종료")

        choice = input("\n메뉴 선택: ")

        if choice == "1":
            add_record(data)
        elif choice == "2":
            show_records(data)
        elif choice == "3":
            show_summary(data)
        elif choice == "4":
            show_monthly_summary(data)
        elif choice == "5":
            delete_record(data)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()
