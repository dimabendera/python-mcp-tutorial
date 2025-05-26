"""
AUTO.RIA MCP Server для пошуку автомобільних оголошень
Використання: fastmcp run servers/mcp-server-auto-ria-search.py
"""

from fastmcp import FastMCP
import httpx
import asyncio
from typing import Optional, List, Dict, Any
import json

mcp = FastMCP("AUTO.RIA Search Server 🚗")

# Глобальна змінна для зберігання API ключа
api_key: Optional[str] = None

# Базовий URL для AUTO.RIA API
BASE_URL = "https://developers.ria.com/auto"

@mcp.tool()
def set_api_key(key: str) -> str:
    """
    Встановлює API ключ для AUTO.RIA

    Args:
        key: API ключ отриманий з developers.ria.com
    """
    global api_key
    api_key = key
    return f"API ключ встановлено успішно"


def add_list_params(params: dict, param_name: str, values: Optional[List[int]]) -> None:
    """
    Додає параметри списку до словника параметрів у правильному форматі для AUTO.RIA API
    """
    if values:
        # Спробуємо різні формати - спочатку через кому
        params[param_name] = values
        # Альтернативно, можна спробувати формат з індексами
        # for i, value in enumerate(values):
        #     params[f"{param_name}[{i}]"] = value


def add_array_params(params: Dict[str, Any], name: str,
                     values: Optional[List[int]]) -> None:
    """
    Додає елементи списку до словника параметрів у форматі name[0], name[1]...
    """
    if values:
        for idx, val in enumerate(values):
            params[f"{name}[{idx}]"] = val


@mcp.tool()
async def search_cars(
    category_id: int = 1,
    s_yers: Optional[List[int]] = None,
    po_yers: Optional[List[int]] = None,
    price_ot: Optional[int] = None,
    price_do: Optional[int] = None,
    currency: int = 1,
    auctionPossible: Optional[int] = None,
    exchangePossible: Optional[int] = None,
    with_exchange_type: Optional[int] = None,
    credit_possible: Optional[int] = None,
    under_credit: Optional[int] = None,
    confiscated_car: Optional[int] = None,
    custom_cleared: Optional[int] = None,
    page: int = 0,
    countpage: int = 20,
    auto_id: Optional[int] = None,
    marka_id: Optional[List[int]] = None,
    model_id: Optional[List[int]] = None,
    city_id: Optional[List[int]] = None,
    state_id: Optional[List[int]] = None,
    gear_id: Optional[List[int]] = None,
    drive_id: Optional[List[int]] = None,
    fuel_id: Optional[List[int]] = None,
    engineVolume_ot: Optional[float] = None,
    engineVolume_do: Optional[float] = None,
    power_ot: Optional[int] = None,
    power_do: Optional[int] = None,
    raceInt_ot: Optional[int] = None,
    raceInt_do: Optional[int] = None,
    bodystyle_id: Optional[List[int]] = None,
    color_id: Optional[List[int]] = None,
    verified: Optional[int] = None
) -> Dict[str, Any]:
    """
    Пошук автомобільних оголошень через AUTO.RIA API

    Args:
        category_id: ID категорії (1 - легкові авто, 2 - мото, 3 - вантажівки, 4 - автобуси, 5 - причепи, 6 - с/г техніка, 7 - спецтехніка, 8 - водний транспорт, 9 - повітряний транспорт)
        s_yers: Рік випуску від (список років)
        po_yers: Рік випуску до (список років)
        price_ot: Ціна від
        price_do: Ціна до
        currency: Валюта (1 - USD, 2 - EUR, 3 - UAH)
        auctionPossible: Можливість аукціону (0 - ні, 1 - так)
        exchangePossible: Можливість обміну (0 - ні, 1 - так)
        with_exchange_type: Тип обміну (1 - авто, 2 - нерухомість, 3 - комерція)
        credit_possible: Можливість кредиту (0 - ні, 1 - так)
        under_credit: Під кредитом (0 - ні, 1 - так)
        confiscated_car: Конфісковане авто (0 - ні, 1 - так)
        custom_cleared: Розмитнене (0 - ні, 1 - так)
        page: Номер сторінки (початок з 0)
        countpage: Кількість записів на сторінку (макс 100)
        auto_id: ID конкретного авто
        marka_id: ID марки авто (список)
        model_id: ID моделі авто (список)
        city_id: ID міста (список)
        state_id: ID області (список)
        gear_id: ID коробки передач (список: 1 - ручна, 2 - автомат, 3 - типтронік, 4 - адаптивна, 5 - варіатор)
        drive_id: ID приводу (список: 1 - передній, 2 - задній, 3 - повний)
        fuel_id: ID типу палива (список)
        engineVolume_ot: Об'єм двигуна від (л)
        engineVolume_do: Об'єм двигуна до (л)
        power_ot: Потужність від (к.с.)
        power_do: Потужність до (к.с.)
        raceInt_ot: Пробіг від (тис. км)
        raceInt_do: Пробіг до (тис. км)
        bodystyle_id: ID типу кузова (список)
        color_id: ID кольору (список)
        verified: Перевірені оголошення (0 - ні, 1 - так)

    Returns:
        Словник з результатами пошуку
    """
    if not api_key:
        return {"error": "API ключ не встановлено. Використайте set_api_key() спочатку"}

    # Формуємо базові параметри запиту
    params = {
        "api_key": api_key,
        "category_id": category_id,
        "page": page,
        "countpage": countpage
    }

    # Додаємо прості параметри
    if price_ot is not None:
        params["price_ot"] = price_ot
    if price_do is not None:
        params["price_do"] = price_do
    if currency != 1:
        params["currency"] = currency
    if auctionPossible is not None:
        params["auctionPossible"] = auctionPossible
    if exchangePossible is not None:
        params["exchangePossible"] = exchangePossible
    if with_exchange_type is not None:
        params["with_exchange_type"] = with_exchange_type
    if credit_possible is not None:
        params["credit_possible"] = credit_possible
    if under_credit is not None:
        params["under_credit"] = under_credit
    if confiscated_car is not None:
        params["confiscated_car"] = confiscated_car
    if custom_cleared is not None:
        params["custom_cleared"] = custom_cleared
    if auto_id is not None:
        params["auto_id"] = auto_id
    if engineVolume_ot is not None:
        params["engineVolume_ot"] = engineVolume_ot
    if engineVolume_do is not None:
        params["engineVolume_do"] = engineVolume_do
    if power_ot is not None:
        params["power_ot"] = power_ot
    if power_do is not None:
        params["power_do"] = power_do
    if raceInt_ot is not None:
        params["raceInt_ot"] = raceInt_ot
    if raceInt_do is not None:
        params["raceInt_do"] = raceInt_do
    if verified is not None:
        params["verified"] = verified

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Формуємо параметри для GET запиту
            # Спочатку спробуємо стандартний підхід з множинними параметрами
            query_params = []

            for key, value in params.items():
                query_params.append((key, str(value)))

            add_array_params("s_yers", s_yers)
            add_array_params("po_yers", po_yers)
            add_array_params("marka_id", marka_id)
            add_array_params("model_id", model_id)
            add_array_params("city_id", city_id)
            add_array_params("state_id", state_id)
            add_array_params("gear_id", gear_id)
            add_array_params("drive_id", drive_id)
            add_array_params("fuel_id", fuel_id)
            add_array_params("bodystyle_id", bodystyle_id)
            add_array_params("color_id", color_id)

            # Виконуємо запит з параметрами у форматі list of tuples
            response = await client.get(f"{BASE_URL}/search", params=query_params)

            # Для дебагу - виводимо фінальний URL
            print(f"Request URL: {response.url}")

            response.raise_for_status()
            data = response.json()

            return {
                "success": True,
                "total_count": data.get("count", 0),
                "page": page,
                "countpage": countpage,
                "cars": data.get("result", []),
                "request_url": str(response.url)  # Для дебагу
            }

    except httpx.HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP помилка: {str(e)}",
            "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Загальна помилка: {str(e)}"
        }


@mcp.tool()
async def search_cars(
    *,
    category_id: int = 1,
    s_yers: Optional[List[int]] = None,
    po_yers: Optional[List[int]] = None,
    price_ot: Optional[int] = None,
    price_do: Optional[int] = None,
    currency: int = 1,
    auctionPossible: Optional[int] = None,
    exchangePossible: Optional[int] = None,
    with_exchange_type: Optional[int] = None,
    credit_possible: Optional[int] = None,
    under_credit: Optional[int] = None,
    confiscated_car: Optional[int] = None,
    custom_cleared: Optional[int] = None,
    page: int = 0,
    countpage: int = 20,
    auto_id: Optional[int] = None,
    marka_id: Optional[List[int]] = None,
    model_id: Optional[List[int]] = None,
    city_id: Optional[List[int]] = None,
    state_id: Optional[List[int]] = None,
    gear_id: Optional[List[int]] = None,
    drive_id: Optional[List[int]] = None,
    fuel_id: Optional[List[int]] = None,
    engineVolume_ot: Optional[float] = None,
    engineVolume_do: Optional[float] = None,
    power_ot: Optional[int] = None,
    power_do: Optional[int] = None,
    raceInt_ot: Optional[int] = None,
    raceInt_do: Optional[int] = None,
    bodystyle_id: Optional[List[int]] = None,
    color_id: Optional[List[int]] = None,
    verified: Optional[int] = None
) -> Dict[str, Any]:
    """
    Пошук оголошень AUTO.RIA. Параметри див. докстрінг вище.
    """

    # ---------- валідація ----------
    if not api_key:
        return {"success": False,
                "error": "API ключ не встановлено; спершу викличте set_api_key()"}
    if s_yers and po_yers and len(s_yers) != len(po_yers):
        return {"success": False,
                "error": "s_yers і po_yers повинні бути однакової довжини"}

    # ---------- базові параметри ----------
    params: Dict[str, Any] = {
        "api_key": api_key,
        "category_id": category_id,
        "page": page,
        "countpage": min(countpage, 100)  # API ліміт
    }

    # ---------- скалярні опції ----------
    scalar_map = {
        "price_ot": price_ot,
        "price_do": price_do,
        "currency": currency if currency != 1 else None,
        "auctionPossible": auctionPossible,
        "exchangePossible": exchangePossible,
        "with_exchange_type": with_exchange_type,
        "credit_possible": credit_possible,
        "under_credit": under_credit,
        "confiscated_car": confiscated_car,
        "custom_cleared": custom_cleared,
        "auto_id": auto_id,
        "engineVolume_ot": engineVolume_ot,
        "engineVolume_do": engineVolume_do,
        "power_ot": power_ot,
        "power_do": power_do,
        "raceInt_ot": raceInt_ot,
        "raceInt_do": raceInt_do,
        "verified": verified
    }
    params.update({k: v for k, v in scalar_map.items() if v is not None})

    # ---------- спискові опції ----------
    add_array_params(params, "s_yers", s_yers)
    add_array_params(params, "po_yers", po_yers)
    add_array_params(params, "marka_id", marka_id)
    add_array_params(params, "model_id", model_id)
    add_array_params(params, "city_id", city_id)
    add_array_params(params, "state_id", state_id)
    add_array_params(params, "gear_id", gear_id)
    add_array_params(params, "drive_id", drive_id)
    add_array_params(params, "fuel_id", fuel_id)
    add_array_params(params, "bodystyle_id", bodystyle_id)
    add_array_params(params, "color_id", color_id)

    # ---------- HTTP запит ----------
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(f"{BASE_URL}/search", params=params)
            resp.raise_for_status()
            data = resp.json()

        return {
            "success": True,
            "total_count": data.get("count", 0),
            "cars": data.get("result", []),
            "page": page,
            "countpage": countpage,
            "request_url": str(resp.url)  # корисно для дебагу
        }

    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "error": f"HTTP {e.response.status_code}: {e.response.text}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Неочікувана помилка: {e}"
        }


@mcp.tool()
async def get_car_info(auto_id: int) -> Dict[str, Any]:
    """
    Отримує детальну інформацію про конкретне авто за його ID

    Args:
        auto_id: ID автомобіля з AUTO.RIA

    Returns:
        Словник з детальною інформацією про авто
    """
    if not api_key:
        return {"error": "API ключ не встановлено. Використайте set_api_key() спочатку"}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{BASE_URL}/info",
                params={"api_key": api_key, "auto_id": auto_id}
            )
            response.raise_for_status()

            return {
                "success": True,
                "car_info": response.json()
            }

    except httpx.HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP помилка: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Загальна помилка: {str(e)}"
        }

@mcp.tool()
async def get_average_price(
    marka_id: int,
    model_id: int,
    yers: int,
    gear_id: Optional[int] = None,
    race_id: Optional[int] = None,
    fuel_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Отримує середню ціну для автомобіля за параметрами

    Args:
        marka_id: ID марки авто
        model_id: ID моделі авто
        yers: Рік випуску
        gear_id: ID коробки передач (опціонально)
        race_id: ID пробігу (опціонально)
        fuel_id: ID типу палива (опціонально)

    Returns:
        Словник з інформацією про середню ціну
    """
    if not api_key:
        return {"error": "API ключ не встановлено. Використайте set_api_key() спочатку"}

    params = {
        "api_key": api_key,
        "marka_id": marka_id,
        "model_id": model_id,
        "yers": yers
    }

    if gear_id is not None:
        params["gear_id"] = gear_id
    if race_id is not None:
        params["race_id"] = race_id
    if fuel_id is not None:
        params["fuel_id"] = fuel_id

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{BASE_URL}/average_price", params=params)
            response.raise_for_status()

            return {
                "success": True,
                "average_price_info": response.json()
            }

    except httpx.HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP помилка: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Загальна помилка: {str(e)}"
        }

@mcp.tool()
def get_search_help() -> str:
    """
    Повертає довідкову інформацію про параметри пошуку AUTO.RIA
    """
    help_text = """
    🚗 AUTO.RIA MCP Server - Довідка по пошуку
    
    Основні функції:
    1. set_api_key(key) - встановити API ключ
    2. search_cars(...) - пошук авто за параметрами (з списками)
    3. search_cars_alternative(...) - спрощений пошук (одиничні значення)
    4. get_car_info(auto_id) - детальна інформація про авто
    5. get_average_price(...) - середня ціна авто
    
    Основні параметри пошуку:
    
    📅 Рік випуску:
    - s_yers: рік від або список років [2010, 2015]  
    - po_yers: рік до або список років [2020, 2023]
    
    💰 Ціна:
    - price_ot/price_do: ціна від/до
    - currency: 1-USD, 2-EUR, 3-UAH
    
    🏭 Марка і модель:
    - marka_id: [79] для BMW, [84] для Mercedes тощо
    - model_id: ID моделі авто
    
    📍 Місцезнаходження:
    - city_id: [5] для Києва, [4] для Харкова тощо
    - state_id: ID області
    
    ⚙️ Технічні характеристики:
    - gear_id: [1-ручна, 2-автомат, 3-типтронік, 4-адаптивна, 5-варіатор]
    - drive_id: [1-передній, 2-задній, 3-повний]
    - fuel_id: ID типу палива
    - engineVolume_ot/do: об'єм двигуна від/до (л)
    - power_ot/do: потужність від/до (к.с.)
    - raceInt_ot/do: пробіг від/до (тис. км)
    
    🎨 Зовнішній вигляд:
    - bodystyle_id: ID типу кузова
    - color_id: ID кольору
    
    ✅ Додаткові опції:
    - verified: 1 для перевірених оголошень
    - custom_cleared: 1 для розмитнених авто
    - exchangePossible: 1 для авто з можливістю обміну
    - credit_possible: 1 для авто з можливістю кредиту
    
    📄 Пагінація:
    - page: номер сторінки (з 0)
    - countpage: кількість записів (макс 100)
    
    Приклад використання:
    await search_cars_alternative(marka_id=79, price_ot=10000, price_do=50000, currency=1)
    """
    return help_text


if __name__ == "__main__":
    mcp.run()