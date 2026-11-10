
import json
import os
from datetime import date, datetime
from collections import defaultdict

FILE_NAME = "expense_data.json"
BUDGET_FILE = "budget_data.json"


# ------------------------------
# 데이터 불러오기 및 저장
# ------------------------------

def load_data():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        print("데이터 형식이 올바르지 않습니다.")
    except (json.JSONDecodeError, OSError):
        print("거래 내역 파일을 읽을 수 없습니다.")

    return []


def save_data(data):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError:
        print("거래 내역 저장에 실패했습니다.")


def load_budgets():
    if not os.path.exists(BUDGET_FILE):
        return {}

    try:
        with open(BUDGET_FILE, "r", encoding="utf-8") as file:
            budgets = json.load(file)

        if isinstance(budgets, dict):
            return budgets

        print("예산 데이터 형식이 올바르지 않습니다.")
    except (json.JSONDecodeError, OSError):
        print("예산 파일을 읽을 수 없습니다.")

    return {}


def save_budgets(budgets):
    try:
        with open(BUDGET_FILE, "w", encoding="utf-8") as file:
            json.dump(budgets, file, ensure_ascii=False, indent=4)
    except OSError:
        print("예산 저장에 실패했습니다.")


# ------------------------------
# 입력 검증
# ------------------------------

def input_amount():
    try:
        amount = int(input("금액(원): ").replace(",", "").strip())

        if amount <= 0:
            print("금액은 0보다 커야 합니다.")
            return None

        return amount

    except ValueError:
        print("올바른 금액을 입력해 주세요.")
        return None


def input_date():
    value = input(
        f"거래 날짜(YYYY-MM-DD, 엔터 입력 시 오늘 날짜 "
        f"{date.today()}): "
    ).strip()

    if not value:
        return date.today().isoformat()

    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError:
        print("날짜는 YYYY-MM-DD 형식으로 입력해 주세요.")
        return None


def input_type():
    print("\n1. 수입")
    print("2. 지출")

    choice = input("구분 선택: ").strip()

    if choice == "1":
        return "수입"
    elif choice == "2":
        return "지출"

    print("잘못된 선택입니다.")
    return None


# ------------------------------
# 예산 확인
# ------------------------------

def check_budget(data, budgets, month):
    budget = budgets.get(month)

    if budget is None:
        return

    monthly_expense = sum(
        record["amount"]
        for record in data
        if record.get("date", "").startswith(month)
        and record.get("type") == "지출"
    )

    print("\n===== 예산 현황 =====")
    print(f"월 예산: {budget:,}원")
    print(f"현재 지출: {monthly_expense:,}원")
    print(f"남은 예산: {budget - monthly_expense:,}원")

    if monthly_expense > budget:
        print("주의! 설정한 월 예산을 초과했습니다.")
    elif monthly_expense == budget:
        print("알림! 월 예산을 모두 사용했습니다.")
    else:
        print("예산 범위 내에서 사용 중입니다.")


# ------------------------------
# 거래 내역 등록
# ------------------------------

def add_record(data, budgets):
    print("\n===== 거래 내역 등록 =====")

    record_type = input_type()
    if record_type is None:
        return

    amount = input_amount()
    if amount is None:
        return

    record_date = input_date()
    if record_date is None:
        return

    category = input("분류: ").strip()
    memo = input("내용: ").strip()

    if not category:
        print("분류를 입력해 주세요.")
        return

    record = {
        "date": record_date,
        "type": record_type,
        "amount": amount,
        "category": category,
        "memo": memo
    }

    data.append(record)
    save_data(data)

    print("\n거래 내역이 저장되었습니다!")

    if record_type == "지출":
        check_budget(data, budgets, record_date[:7])


# ------------------------------
# 거래 내역 조회
# ------------------------------

def show_records(data):
    if not data:
        print("\n등록된 내역이 없습니다.")
        return

    print("\n===== 거래 내역 =====")

    for i, record in enumerate(data, 1):
        print(f"\n[{i}] 날짜: {record.get('date', '-')}")
        print(f"    구분: {record.get('type', '-')}")
        print(f"    금액: {record.get('amount', 0):,}원")
        print(f"    분류: {record.get('category', '-')}")
        print(f"    내용: {record.get('memo', '-')}")


# ------------------------------
# 거래 내역 수정
# ------------------------------

def edit_record(data, budgets):
    if not data:
        print("\n수정할 내역이 없습니다.")
        return

    show_records(data)

    try:
        number = int(input("\n수정할 내역 번호: "))

        if number < 1 or number > len(data):
            print("올바른 번호를 입력해 주세요.")
            return

    except ValueError:
        print("숫자로 입력해 주세요.")
        return

    record = data[number - 1]

    print("\n수정할 항목을 선택하세요.")
    print("1. 거래 구분")
    print("2. 금액")
    print("3. 날짜")
    print("4. 분류")
    print("5. 내용")
    print("0. 취소")

    choice = input("선택: ").strip()

    if choice == "1":
        value = input_type()
        if value is None:
            return
        record["type"] = value

    elif choice == "2":
        value = input_amount()
        if value is None:
            return
        record["amount"] = value

    elif choice == "3":
        value = input_date()
        if value is None:
            return
        record["date"] = value

    elif choice == "4":
        value = input("새 분류: ").strip()
        if not value:
            print("분류를 입력해 주세요.")
            return
        record["category"] = value

    elif choice == "5":
        record["memo"] = input("새 내용: ").strip()

    elif choice == "0":
        print("수정을 취소했습니다.")
        return

    else:
        print("잘못된 선택입니다.")
        return

    save_data(data)
    print("거래 내역이 수정되었습니다!")

    if record["type"] == "지출":
        check_budget(data, budgets, record["date"][:7])


# ------------------------------
# 전체 통계
# ------------------------------

def show_summary(data):
    income = sum(
        r["amount"] for r in data if r["type"] == "수입"
    )

    expense = sum(
        r["amount"] for r in data if r["type"] == "지출"
    )

    print("\n===== 전체 통계 =====")
    print(f"총수입: {income:,}원")
    print(f"총지출: {expense:,}원")
    print(f"현재 잔액: {income - expense:,}원")


# ------------------------------
# 월별 통계
# ------------------------------

def show_monthly_summary(data, budgets):
    month = input("조회할 월(YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("YYYY-MM 형식으로 입력해 주세요.")
        return

    records = [
        r for r in data
        if r.get("date", "").startswith(month)
    ]

    income = sum(
        r["amount"] for r in records if r["type"] == "수입"
    )

    expense = sum(
        r["amount"] for r in records if r["type"] == "지출"
    )

    print(f"\n===== {month} 통계 =====")
    print(f"수입: {income:,}원")
    print(f"지출: {expense:,}원")
    print(f"잔액: {income - expense:,}원")

    check_budget(data, budgets, month)


# ------------------------------
# 카테고리별 지출 통계
# ------------------------------

def show_category_summary(data):
    categories = defaultdict(int)

    for record in data:
        if record.get("type") == "지출":
            category = record.get("category", "기타")
            categories[category] += record.get("amount", 0)

    if not categories:
        print("\n등록된 지출 내역이 없습니다.")
        return

    print("\n===== 카테고리별 지출 통계 =====")

    for category, amount in sorted(
        categories.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        print(f"{category}: {amount:,}원")


# ------------------------------
# 거래 내역 검색
# ------------------------------

def search_records(data):
    keyword = input("\n검색어 입력: ").strip().lower()

    if not keyword:
        print("검색어를 입력해 주세요.")
        return

    results = []

    for record in data:
        searchable = [
            str(record.get("date", "")),
            str(record.get("type", "")),
            str(record.get("category", "")),
            str(record.get("memo", ""))
        ]

        if any(keyword in value.lower() for value in searchable):
            results.append(record)

    if not results:
        print("검색 결과가 없습니다.")
        return

    print(f"\n===== 검색 결과: {len(results)}건 =====")

    for i, record in enumerate(results, 1):
        print(f"\n[{i}] {record['date']}")
        print(f"    구분: {record['type']}")
        print(f"    금액: {record['amount']:,}원")
        print(f"    분류: {record['category']}")
        print(f"    내용: {record['memo']}")


# ------------------------------
# 월별 예산 설정
# ------------------------------

def set_budget(budgets):
    month = input("예산을 설정할 월(YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("YYYY-MM 형식으로 입력해 주세요.")
        return

    amount = input_amount()

    if amount is None:
        return

    budgets[month] = amount
    save_budgets(budgets)

    print(f"\n{month} 예산이 {amount:,}원으로 설정되었습니다!")


# ------------------------------
# 거래 내역 삭제
# ------------------------------

def delete_record(data):
    if not data:
        print("\n삭제할 내역이 없습니다.")
        return

    show_records(data)

    try:
        number = int(input("\n삭제할 내역 번호: "))

        if number < 1 or number > len(data):
            print("올바른 번호를 입력해 주세요.")
            return

    except ValueError:
        print("숫자로 입력해 주세요.")
        return

    deleted = data.pop(number - 1)
    save_data(data)

    print(f"{deleted['category']} 내역이 삭제되었습니다!")


# ------------------------------
# 메인 프로그램
# ------------------------------

def main():
    data = load_data()
    budgets = load_budgets()

    while True:
        print("\n================================")
        print("     PERSONAL EXPENSE TRACKER")
        print("================================")
        print("1. 수입 및 지출 등록")
        print("2. 전체 거래 내역 조회")
        print("3. 전체 잔액 및 통계")
        print("4. 월별 통계")
        print("5. 거래 내역 수정")
        print("6. 거래 내역 삭제")
        print("7. 카테고리별 지출 통계")
        print("8. 거래 내역 검색")
        print("9. 월별 예산 설정")
        print("0. 프로그램 종료")
        print("================================")

        choice = input("메뉴 선택: ").strip()

        if choice == "1":
            add_record(data, budgets)

        elif choice == "2":
            show_records(data)

        elif choice == "3":
            show_summary(data)

        elif choice == "4":
            show_monthly_summary(data, budgets)

        elif choice == "5":
            edit_record(data, budgets)

        elif choice == "6":
            delete_record(data)

        elif choice == "7":
            show_category_summary(data)

        elif choice == "8":
            search_records(data)

        elif choice == "9":
            set_budget(budgets)

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("잘못된 입력입니다. 다시 선택해 주세요.")


if __name__ == "__main__":
    main()
