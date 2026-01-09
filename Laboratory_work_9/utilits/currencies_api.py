import requests
import sys
import io
import logging.handlers

def get_currencies(currency_codes: list, url:str = "https://www.cbr-xml-daily.ru/daily_json.js", handle=sys.stdout)->dict:
    """
    Получает курсы валют с API Центробанка России.


    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']).

    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
              Возвращает None в случае ошибки запроса.
    """
    try:

        response = requests.get(url)

        # print(response.status_code)
        response.raise_for_status()  # Проверка на ошибки HTTP
        try:
            data = response.json()
        except ValueError as e:
            raise ValueError("Некорректный JSON")


        currencies = {}
        try:
            a = data["Valute"]
        except KeyError:
            raise KeyError("Нет ключа 'Valute'")


        if "Valute" in data:
            for code in currency_codes:
                if code in data["Valute"]:
                    try:
                        currencies[code] = float(data["Valute"][code]["Value"])
                    except:
                        raise TypeError("Курс валюты имеет неверный тип")
                else:
                    currencies[code] = f"Код валюты '{code}' не найден."
                    raise KeyError("Валюта отсутствует в данных")
        return currencies

    except requests.exceptions.RequestException as e:
        # print(f"Ошибка при запросе к API: {e}", file=handle)
        handle.write(f"Ошибка при запросе к API: {e}")
        #raise ValueError('Упали с исключением')
        raise requests.exceptions.ConnectionError('Упали с исключением')

# Пример использования функции:
currencies = [
    "USD",  # Доллар США (United States Dollar)
    "EUR",  # Евро (Euro)
    "JPY",  # Японская иена (Japanese Yen)
    "GBP",  # Фунт стерлингов (British Pound)
    "CHF",  # Швейцарский франк (Swiss Franc)
    "CAD",  # Канадский доллар (Canadian Dollar)
    "AUD",  # Австралийский доллар (Australian Dollar)
    "CNY",  # Китайский юань (Chinese Yuan)
    "NZD",  # Новозеландский доллар (New Zealand Dollar)
    "INR"   # Индийская рупия (Indian Rupee)
]

if __name__ == "__main__":
    currency_list = get_currencies(currencies, url="https://www.cbr-xml-daily.ru/daily_json.js")
    print(currency_list["USD"])
    print(currency_list)