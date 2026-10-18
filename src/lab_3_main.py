from collections import defaultdict
from functools import reduce
import datetime

available_sessions: list = [
    {
        "date": "2026-07-29",
        "film": "Spider-Man: Brand New Day",
        "session": "11:30",
        "quantity": 60,
        "price": 190,
    },
    {
        "date": "2026-07-29",
        "film": "The Odyssey",
        "session": "12:00",
        "quantity": 40,
        "price": 180,
    },
    {
        "date": "2026-07-29",
        "film": "Spider-Man: Brand New Day",
        "session": "15:30",
        "quantity": 40,
        "price": 240,
    },
    {
        "date": "2026-07-30",
        "film": "The Odyssey",
        "session": "17:00",
        "quantity": 50,
        "price": 200,
    },
    {
        "date": "2026-07-30",
        "film": "Spider-Man: Brand New Day",
        "session": "19:30",
        "quantity": 55,
        "price": 260,
    },
    {
        "date": "2026-07-31",
        "film": "Minions & Monsters",
        "session": "10:00",
        "quantity": 75,
        "price": 190,
    },
    {
        "date": "2026-07-31",
        "film": "Moana",
        "session": "14:30",
        "quantity": 100,
        "price": 200,
    },
    {
        "date": "2026-07-31",
        "film": "Moana",
        "session": "19:00",
        "quantity": 80,
        "price": 210,
    },
]

sales_data = []

editable = ("date", "film", "session", "price", "quantity")

sort_keys = {
    "date": lambda s: (s["date"], s["session"]),
    "film": lambda s: (s["film"].lower(), s["date"], s["session"]),
    "session": lambda s: (s["session"], s["date"]),
    "price": lambda s: (s["price"], s["date"], s["session"]),
    "quantity": lambda s: (s["quantity"], s["date"], s["session"]),
}

def add_sale(data: list, sale: dict):
    # Додає продаж квитка
    data.append(sale)
    print("Додано новий продаж!")

def remove_sale(data: list, index: int):
    # Видаляє продаж квитка
    if not data[index]:
        print(f"Немає продажу за індексом: {index}")
        return

    session_index: int = data[index]["session_index"]
    available_sessions[session_index]['quantity'] += data[index]['quantity']

    del data[index]
    print(f"Видалено квиток за індексом: {index + 1}")

def calculate_ticket_price_by(param: str):
    sessions = list(filter(
        lambda x: x["quantity"] > 0,
        available_sessions
    ))

    if param == "avg":
        summ = reduce(
            lambda a, b: a + b["price"], sessions, 0
        ) / max(len(sessions), 1)

        print(summ)
        if summ == 0:
            print("Немає квитків в наявності")
            return

        print(f"Середня ціна за квиток: {summ:.2f} грн")
    elif param == "min":
        val = pow(10, 10)

        for session in sessions:
            val = min(val, session["price"])

        if val == 1000:
            print("Немає квитків в наявності")
            return

        print(f"Мінімальна ціна за квиток: {val:.2f} грн")
    elif param == "max":
        val = 0

        for session in sessions:
            val = max(val, session["price"])

        if val == 0:
            print("Немає квитків в наявності")
            return

        print(f"Максимальна ціна за квиток: {val:.2f} грн")


def find_available_sessions_by_parameter(array, param_name: str, parameter):
    return list(
        filter(
            lambda x: x[param_name] == parameter,
            array
        )
    )

def print_sales():
    ind = 1
    for sale in sales_data:
        print(f"{ind} - {sale['date']} | {sale['film']} | {sale['session']} | {sale['price']:.2f} грн. | {sale['quantity']} квитків")
        ind += 1

    if ind == 1:
        print("Немає придбаних квитків")

def print_available_sessions(sessions=None):
    # Якщо список не передано - виводить сеанси в початковому порядку
    if sessions is None:
        sessions = available_sessions

    ind = 1
    for session in sessions:
        if session["quantity"] > 0:
            print(
                f"{ind} - {session['date']} | {session['film']} | {session['session']} | {session['price']:.2f} грн. | {session['quantity']} квитків")
            ind += 1

    if ind == 1:
        print("Немає активних сеансів")


def get_available_tickets_by_film_name(film_name: str):
    sorted_list = find_available_sessions_by_parameter(available_sessions, "film", film_name)
    if not sorted_list:
        return f"Немає вільних квитків до фільму: {film_name}"


    return f"{reduce(
        lambda a, b: a + b['quantity'], sorted_list, 0
    )} вільних квитків"

def clean_str(s: str):
    return "".join(char.lower() for char in s if char.isalnum())

def find_available_sessions_from_name(array, film_name: str):
    return list(filter(
        lambda session: clean_str(session["film"]) == clean_str(film_name),
        array
    ))

def group_sales_by_film_name(data):
    """Групує продажі за категоріями."""
    categories = defaultdict(list)
    for sale in data:
        categories[sale["film"]].append(sale)
    return dict(categories)

def update_sale(sales, index: int, key, value):
    """Оновлює інформацію про продаж"""
    if not (0 <= index < len(sales)):
        print("Невірний індекс.")
        return

    if key not in editable:
        print("Невірний ключ.")
        return

    sale = sales[index]
    sale_index: int = sale["session_index"]
    old_session = available_sessions[sale_index]

    if key == "price":
        try:
            price = float(value)
        except ValueError:
            print(f"Невірний тип значення для ключа '{key}'")
            return

        if price < 0:
            print("Ціна не може бути від'ємною.")
            return

        sale["price"] = price

    elif key == "quantity":
        try:
            new_quantity = int(value)
        except ValueError:
            print(f"Невірний тип значення для ключа '{key}'")
            return

        if new_quantity <= 0:
            print("Кількість квитків має бути більшою за 0.")
            return

        diff = new_quantity - sale["quantity"]
        if diff > old_session["quantity"]:
            print(f"Недостатньо вільних квитків. Можна додати ще: {old_session['quantity']}")
            return

        old_session["quantity"] -= diff
        sale["quantity"] = new_quantity

    else:
        # date / film / session - це переніс продажу на інший сеанс
        new_values = {
            "date": sale["date"],
            "film": sale["film"],
            "session": sale["session"],
        }

        if key == "date":
            try:
                datetime.datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                print("Невірний формат дати. Використовуйте YYYY-MM-DD.")
                return

        new_values[key] = value

        new_session = next(
            (
                s for s in available_sessions
                if s["date"] == new_values["date"]
                and clean_str(s["film"]) == clean_str(new_values["film"])
                and s["session"] == new_values["session"]
            ),
            None
        )

        if new_session is None:
            print("Сеанс з такими параметрами не існує.")
            return

        if new_session is old_session:
            print("Значення не змінилось - це той самий сеанс.")
            return

        if new_session["quantity"] < sale["quantity"]:
            print(f"На цьому сеансі недостатньо квитків (вільно: {new_session['quantity']}).")
            return

        old_session["quantity"] += sale["quantity"]
        new_session["quantity"] -= sale["quantity"]

        sale["date"] = new_session["date"]
        sale["film"] = new_session["film"]
        sale["session"] = new_session["session"]
        sale["price"] = new_session["price"]
        sale["session_index"] = available_sessions.index(new_session)

    print("Інформацію оновлено успішно.")

def sort_by_parameter(param: str, reverse: bool = False):
    key_func = sort_keys.get(param)
    if key_func is None:
        print(f"Невірний параметр. Доступні: {'/'.join(sort_keys)}")
        return

    sorted_sessions = sorted(available_sessions, key=key_func, reverse=reverse)
    print_available_sessions(sorted_sessions)

def print_menu():
        """
        Виводить меню опцій.
        """
        print("\n==== Меню керування кінотеатром ====")

        print("1. Показати всі сеанси") # +
        print("2. Показати всі придбані квитки") # +
        print("3. Додати новий квиток") # +
        print("4. Видалити квиток") # +
        print("5. Оновити інформацію про продаж") # +
        print("6. Знайти сеанси за назвою фільму") # +
        print("7. Обчислити загальну кількість вільних квитків за назвою фільму") # +
        print("8. Сортувати сеанси за параметром") # +
        print("9. Групувати продажі за назвами фільмів") # +
        print("10. Обчислити ціну квитка за параметром") # +

        print("0. Вийти\n")

def main():
    global sales_data

    while True:
        try:
            print_menu()
            user_input = input()

            if user_input == "1":
                print_available_sessions()
            elif user_input == "2":
                print_sales()
            elif user_input == "3":
                try:
                    print_available_sessions()
                    date = input("\nВведіть дату (YYYY-MM-DD): ")
                    datetime.datetime.strptime(date, "%Y-%m-%d")  # перевірка формату

                    date_sessions = find_available_sessions_by_parameter(available_sessions, "date", date)
                    if not date_sessions:
                        print("Немає сесій за цією датою.")
                        continue

                    print("--------------------------------------------")
                    print(date)
                    for session in date_sessions:
                        print(f"{date_sessions.index(session) + 1} - {session["film"]} | {session['session']} | {session['quantity']} квитків")
                    print("--------------------------------------------")

                    film = input("Введіть назву фільму: ")

                    name_sessions = find_available_sessions_from_name(date_sessions, film)
                    if not name_sessions:
                        print("Немає сесій за цією назвою фільму.")
                        continue

                    print("--------------------------------------------")
                    print(name_sessions[0]['film'], "\n")
                    for session in name_sessions:
                        print(f"{name_sessions.index(session) + 1} - {session['session']} | {session['quantity']} квитків")
                    print("--------------------------------------------")

                    time_sessions = name_sessions
                    if len(name_sessions) > 1:
                        session_time = input("Введіть час сесії: ")

                        time_sessions = find_available_sessions_by_parameter(name_sessions, "session", session_time)
                        if not time_sessions:
                            print("Немає сесій на цей час.")
                            continue

                    session = time_sessions[0]
                    session_time = session['session']
                    print("--------------------------------------------")
                    print(f"{session_time}\n")
                    print(f"{time_sessions.index(session) + 1} - {session['quantity']} квитків")
                    print("--------------------------------------------")

                    quantity = int(input("Введіть кількість: "))

                    if quantity <= 0 or quantity > session["quantity"]:
                        print("Невірна кількість квитків.")
                        continue

                    new_sale = {
                        "date": session['date'],
                        "film": session['film'],
                        "session": session_time,
                        "price": session['price'],
                        "quantity": quantity,
                        "session_index": available_sessions.index(session),
                    }

                    session['quantity'] -= quantity
                    add_sale(sales_data, new_sale)
                except ValueError:
                    print("Помилка введення. Перевірте формат дати, ціни та кількості.")
            elif user_input == "4":
                print_sales()
                try:
                    index = int(input("Введіть індекс продажу: "))
                    if not (0 < index <= len(sales_data)):
                        print("Невірний індекс.")
                        continue

                    if not sales_data[index - 1]:
                        print("Немає продажів за цим індексом.")

                    remove_sale(sales_data, index - 1)
                except ValueError:
                    print("Невірний індекс. Введіть існуючий числовий індекс.")
            elif user_input == "5":
                if not sales_data:
                    print("Немає придбаних квитків")
                    continue

                print_sales()
                try:
                    index = int(input("Введіть індекс продажу для оновлення: "))
                    if not (0 < index <= len(sales_data)):
                        print("Невірний індекс.")
                        continue

                    key = input("Введіть ключ для оновлення (date/session/film/price/quantity): ").strip().lower()
                    if key not in editable:
                        print("Невірний ключ.")
                        continue

                    value = input("Введіть нове значення: ").strip()
                    update_sale(sales_data, index - 1, key, value)
                except ValueError:
                    print("Невірний індекс. Введіть існуючий числовий індекс.")
            elif user_input == "6":
                film_name = input("Введіть назву фільму: ")

                sessions = find_available_sessions_from_name(available_sessions, film_name)
                if not sessions:
                    print("Немає квитків за цієї назвою фільму.")
                    continue

                print(film_name, "\n")
                ind = 1
                for session in sessions:
                    print(
                        f"{ind} - {session['date']} | {session['session']} | {session["price"]:.2f} грн | {session["quantity"]} квитків")
                    ind += 1
            elif user_input == "7":
                print_available_sessions()
                film_name = input("Введіть назву фільму")

                print(get_available_tickets_by_film_name(film_name))
            elif user_input == "8":
                param = input(f"Введіть параметр сортування [{'/'.join(sort_keys)}]: ").strip().lower()
                order = input("Порядок [asc/desc] (за замовчуванням asc): ").strip().lower()

                sort_by_parameter(param, reverse=(order == "desc"))
            elif user_input == "9":
                grouped = group_sales_by_film_name(sales_data)

                for film, sales in grouped.items():
                    print(f"\nФільм: {film}:")
                    for sale in sales:
                        print(f"  {sale}")
            elif user_input == "10":
                param = input("Введіть параметр: [avg/min/max]")

                calculate_ticket_price_by(param)
            elif user_input == "0":
                break
        except ValueError as error:
            print(f"Помилка вводу: {error}\n")
        except (EOFError, KeyboardInterrupt):
            break

    return 0

if __name__ == "__main__":
    main()