from bs4 import BeautifulSoup
import math
import json


def extract_items_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    products_layout = soup.find_all('div', attrs={'class': 'product-item'})
    items = []
    for product in products_layout:
        item = {}
        item['id'] = int(product.find('a', attrs={'class': 'add-to-favorite'})['data-id'])
        item['href'] = product.find('a', attrs={'class': ''})['href']
        item['img'] = product.find('img')['src']
        item['name'] = product.find('span').get_text().strip().replace('"', '\"')
        item['price'] = int(product.find('price').get_text().replace('₽', '').replace(' ', '').strip())
        item['bonus'] = int(product.find('strong').get_text().split()[2])
        item['specs'] = {}
        for spec in product.ul.find_all('li'):
            item['specs'][spec['type']] = spec.get_text().strip()
        items.append(item)
    return items


def calculate_statistics(data):
    init_price = data[0]['price']
    price_max, price_min, price_sum  = init_price, init_price, 0
    ram_frequencies = {}

    for item in data:
        ram = item['specs'].get('ram', '-1')
        if ram in ram_frequencies:
            ram_frequencies[ram] += 1
        else:
            ram_frequencies[ram] = 1
        price = item['price']
        price_sum += price
        if price < price_min:
            price_min = price
        if price > price_max:
            price_max = price

    price_avg = round(price_sum / len(data), 4)
    sum_pow = 0
    for item in data:
        sum_pow += ((item['price'] - price_avg) ** 2)
    price_standard_deviation = round(math.sqrt(sum_pow / len(data)), 4)

    for k, v in ram_frequencies.items():
        ram_frequencies[k] = round(v / len(data), 3)

    ram_frequencies = dict(sorted(ram_frequencies.items(), key=lambda d: int(d[0].split()[0]), reverse=True))
    ram_frequencies['No data'] = ram_frequencies['-1']
    ram_frequencies.pop('-1')

    return {'price_max': price_max, 'price_min': price_min, 'price_sum': price_sum, 'price_avg': price_avg,
            'price_standard_deviation': price_standard_deviation, 'ram_frequencies': ram_frequencies}


def sort_and_filter(data):
    sorted_data = sorted(data, key=lambda d: d['bonus'], reverse=True)
    return list(filter(lambda d: float(d['name'].split('\"')[0]) < 7, sorted_data))


def read_file(path):
    with open(path, newline='', encoding="utf-8") as file:
        return file.read()


def read_data():
    items = []
    for i in range(1, 37):
        html = read_file(f"../data/2/{i}.html")
        items.extend(extract_items_data(html))
    return items

def write_to_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


data = read_data()
result_data = sort_and_filter(data)
statistics = calculate_statistics(data)
write_to_json("task_2_original_result.json", data)
write_to_json("task_2_sorted_and_filtered_result.json", result_data)
write_to_json("task_2_statistics_result.json", statistics)