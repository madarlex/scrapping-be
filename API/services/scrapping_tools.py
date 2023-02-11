import requests
import json

def get_url(country, shop_id, offset):
    """
    This function get first complete url from FE.

    :country: a string value representing the name of searching country.
    :shop_id: a integer value representing the id of searching shop.
    :offset: a integer value representing the offset of searching items.
    :return: url
    """

    if country == "malaysia":
        url = f"https://shopee.com.my/api/v4/shop/search_items?limit=100&offset={offset}&order=desc&sort_by=pop&shopid={shop_id}"
    elif country == "singapore":
        url = f"https://shopee.sg/api/v4/shop/search_items?limit=100&offset={offset}&order=desc&sort_by=pop&shopid={shop_id}"
    elif country == "vietnam":
        url = f"https://shopee.vn/api/v4/shop/search_items?limit=100&offset={offset}&order=desc&sort_by=pop&shopid={shop_id}"
    elif country == "thailand":
        url = f"https://shopee.co.th/api/v4/shop/search_items?limit=100&offset={offset}&order=desc&sort_by=pop&shopid={shop_id}"
    elif country == "indonesia":
        url = f"https://shopee.co.id/api/v4/shop/search_items?limit=100&offset={offset}&order=desc&sort_by=pop&shopid={shop_id}"
    else:
        url = None
    return url

def get_total_offset_time(data, nomore):   
    """
    This function calculates how many pages are there to get an offset time for looping.

    :data: a json value from api.
    :nomore: a boolean get from data.
    :return: total_offset_time
    """ 

    if not nomore:
        total_offset_time = int(data["total_count"]) // 100
    else:
        total_offset_time = 0
    return total_offset_time

def concat_data(data, next_data):
    """
    This function concatinates items fields in multi json data from api.

    :data: a json value from api.
    :next_data: a json value by calling the next api with new offset.
    :return: data
    """ 

    current_items = data.get("items")
    next_items = next_data.get("items")
    current_items.extend(next_items)
    data["items"] = current_items
    return data

def get_data_from_api(country, shop_id):
    """
    This function gets all possible data from one or multi api

    :country: a string value representing the name of searching country.
    :shop_id: a integer value representing the id of searching shop.
    :return: data or "No data, and boolean
    """ 

    offset = 0
    url = get_url(country, shop_id, offset)
    if url:
        response = requests.get(url)
        data = json.loads(response.text)
        nomore = data.get("nomore", True)
        total_offset_time = get_total_offset_time(data, nomore)
        if total_offset_time != 0:
            for offset_time in range(total_offset_time):
                offset += 100
                next_url = get_url(country, shop_id, offset)
                next_response = requests.get(next_url)
                next_data = json.loads(next_response.text)
                data = concat_data(data, next_data)
        if data.get("items"):
            return data, True
        else:
            return "No data", False
    else:
        return "Wrong url", False

def convert_scrapping_data(data):
    """
    This function converts data from api into needed data (name, price)

    :data: a json value from api.
    :return: a json result value
    """ 

    product_infos = []
    total_items = 0
    for item in data['items']:
        product_name = item["item_basic"].get("name", "No Product Name")
        product_price = item["item_basic"].get("price", 0)
        product_info = {"name": product_name, "price": product_price}
        product_infos.append(product_info)
        total_items += 1
    results = {"total_items": total_items, "product_infos": product_infos}
    return results

def export_json_file(data):
    """
    This function export raw data from api

    :data: a json value from api.
    :return:
    """ 

    with open("raw_data.json", "w") as file:
        json.dump(data, file)


def scrapping_tools(country, shop_id):
    """
    This function is the main function of this service, combine and call other functions to get data

    :country: a string value representing the name of searching country.
    :shop_id: a integer value representing the id of searching shop.
    :return: a json value
    """ 

    data, data_check = get_data_from_api(country, shop_id)
    if data_check:
        export_json_file(data)
        data = convert_scrapping_data(data)
    return data

if __name__ == "__main__":
    scrapping_tools("vietnam", 27495213)

