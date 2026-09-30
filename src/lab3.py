# ============================= УВАГА! =============================
# Цей файл містить ПРИКЛАД виконання лабораторної роботи.
# Ваше завдання - розробити ВЛАСНУ програму згідно з вашим варіантом.
#
# Ви можете використовувати цей код як зразок, але не копіювати його.
# Повністю замініть цей код своєю реалізацією.
#
# Ваш код повинен відповідати таким вимогам:
# 1. Обрана предметна область згідно з вашим варіантом.
# 2. Реалізовано всі необхідні функції:
#    - додавання, видалення, оновлення даних
#    - пошук та фільтрація
#    - обчислення статистик (середнє, min/max)
#    - групування та агрегація
# 3. Використано map(), filter(), reduce(), сортування, зрізи.
# 4. Реалізовано операції з множинами та словниками.
# 5. Створено інтерактивне меню для користувача.
# =================================================================

from collections import defaultdict
from functools import reduce
import datetime

# Приклад: Аналіз даних про продажі
# ЗАМІНІТЬ ЦІ ДАНІ ТА ЛОГІКУ НА ВАШІ ВЛАСНІ

# 1. Підготовка даних
sales_data = [
    {"date": "2023-01-01", "product": "Laptop", "category": "Electronics", "price": 1200, "quantity": 5},
    {"date": "2023-01-02", "product": "Smartphone", "category": "Electronics", "price": 800, "quantity": 10},
    {"date": "2023-01-03", "product": "T-shirt", "category": "Clothing", "price": 20, "quantity": 50},
    {"date": "2023-01-04", "product": "Jeans", "category": "Clothing", "price": 60, "quantity": 30},
    {"date": "2023-01-05", "product": "Keyboard", "category": "Electronics", "price": 75, "quantity": 20},
]

# 2. Функції для роботи з даними
def add_sale(data, sale):
    """Додає новий запис про продаж."""
    data.append(sale)
    print("Продаж додано успішно.")

def remove_sale(data, index):
    """Видаляє запис про продаж за індексом."""
    if 0 <= index < len(data):
        del data[index]
        print("Продаж видалено успішно.")
    else:
        print("Невірний індекс.")

def update_sale(data, index, key, value):
    """Оновлює інформацію про продаж."""
    if 0 <= index < len(data):
        # Перетворення значення до відповідного типу
        if key in ['price', 'quantity']:
            try:
                value = float(value) if key == 'price' else int(value)
            except ValueError:
                print(f"Невірний тип значення для ключа '{key}'")
                return
        data[index][key] = value
        print("Інформацію оновлено успішно.")
    else:
        print("Невірний індекс.")

def find_sales_by_product(data, product):
    """Знаходить всі продажі конкретного продукту."""
    return list(filter(lambda x: x["product"].lower() == product.lower(), data))

# 3. Специфічні функції аналізу
def calculate_total_sales(data):
    """Обчислює загальну суму продажів."""
    return reduce(lambda acc, sale: acc + sale["price"] * sale["quantity"], data, 0)

def calculate_average_price(data):
    """Обчислює середню ціну товару."""
    prices = [sale["price"] for sale in data]
    return sum(prices) / len(prices) if prices else 0

# 4. Вбудовані функції та методи
def sort_sales_by_date(data):
    """Сортує продажі за датою."""
    return sorted(data, key=lambda x: datetime.datetime.strptime(x["date"], "%Y-%m-%d"))

# 5. Робота з множинами та словниками
def group_sales_by_category(data):
    """Групує продажі за категоріями."""
    categories = defaultdict(list)
    for sale in data:
        categories[sale["category"]].append(sale)
    return dict(categories)

def find_best_selling_product(data):
    """Знаходить товар, який найкраще продається."""
    if not data:
        return None
    products = defaultdict(int)
    for sale in data:
        products[sale["product"]] += sale["quantity"]
    return max(products, key=products.get)

# 6. Інтерактивне меню
def print_menu():
    """Виводить меню опцій."""
    print("\n==== Меню аналізу продажів (ПРИКЛАД) ====")
    print("1. Показати всі продажі")
    print("2. Додати новий продаж")
    print("3. Видалити продаж")
    print("4. Оновити інформацію про продаж")
    print("5. Знайти продажі за назвою товару")
    print("6. Обчислити загальну суму продажів")
    print("7. Групувати продажі за категоріями")
    print("8. Сортувати продажі за датою")
    print("9. Знайти товар, який найкраще продається")
    print("10. Обчислити середню ціну товару")
    print("0. Вийти")

def main():
    """Головна функція програми."""
    global sales_data
    while True:
        print_menu()
        choice = input("Оберіть опцію: ")

        if choice == "1":
            if not sales_data:
                print("Немає даних про продажі.")
            for i, sale in enumerate(sales_data):
                print(f"{i}: {sale}")
        elif choice == "2":
            try:
                date = input("Введіть дату (YYYY-MM-DD): ")
                datetime.datetime.strptime(date, "%Y-%m-%d") # перевірка формату
                product = input("Введіть назву товару: ")
                category = input("Введіть категорію: ")
                price = float(input("Введіть ціну: "))
                quantity = int(input("Введіть кількість: "))
                new_sale = {"date": date, "product": product, "category": category, "price": price, "quantity": quantity}
                add_sale(sales_data, new_sale)
            except ValueError:
                print("Помилка введення. Перевірте формат дати, ціни та кількості.")
        elif choice == "3":
            try:
                index = int(input("Введіть індекс продажу для видалення: "))
                remove_sale(sales_data, index)
            except ValueError:
                print("Невірний індекс. Введіть число.")
        elif choice == "4":
            try:
                index = int(input("Введіть індекс продажу для оновлення: "))
                if not (0 <= index < len(sales_data)):
                    print("Невірний індекс.")
                    continue
                key = input("Введіть ключ для оновлення (date/product/category/price/quantity): ")
                if key not in sales_data[0]:
                    print("Невірний ключ.")
                    continue
                value = input("Введіть нове значення: ")
                update_sale(sales_data, index, key, value)
            except ValueError:
                print("Невірний індекс. Введіть існуючий числовий індекс.")
        elif choice == "5":
            product = input("Введіть назву товару для пошуку: ")
            results = find_sales_by_product(sales_data, product)
            if results:
                for sale in results:
                    print(sale)
            else:
                print(f"Продажі для товару '{product}' не знайдено.")
        elif choice == "6":
            total = calculate_total_sales(sales_data)
            print(f"Загальна сума продажів: {total}")
        elif choice == "7":
            grouped = group_sales_by_category(sales_data)
            for category, sales in grouped.items():
                print(f"\nКатегорія: {category}:")
                for sale in sales:
                    print(f"  {sale}")
        elif choice == "8":
            sorted_sales = sort_sales_by_date(sales_data)
            for sale in sorted_sales:
                print(sale)
        elif choice == "9":
            best_product = find_best_selling_product(sales_data)
            if best_product:
                print(f"Товар, який найкраще продається: {best_product}")
            else:
                print("Немає даних для аналізу.")
        elif choice == "10":
            avg_price = calculate_average_price(sales_data)
            print(f"Середня ціна товару: {avg_price:.2f}")
        elif choice == "0":
            print("Дякуємо за використання програми!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
