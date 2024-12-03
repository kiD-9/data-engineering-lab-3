from bs4 import BeautifulSoup
import math
import json


def extract_items_data(xml):
    soup = BeautifulSoup(xml, 'xml')
    items = []
    for e in soup.find('clothing-items'):
        if e.name is None:
            continue
        item = {}
        item['id'] = int(e.id.get_text().strip())
        item['name'] = e.find('name').get_text().strip()
        item['category'] = e.category.get_text().strip()
        item['size'] = e.size.get_text().strip()
        item['color'] = e.color.get_text().strip()
        item['material'] = e.material.get_text().strip()
        item['price'] = int(e.price.get_text().strip())
        item['rating'] = float(e.rating.get_text().strip())
        item['reviews'] = int(e.reviews.get_text().strip())
        if e.new is not None:
            item['new'] = e.new.get_text().strip() == '+'
        if e.exclusive is not None:
            item['exclusive'] = e.exclusive.get_text().strip() == 'yes'
        if e.sporty is not None:
            item['sporty'] = e.sporty.get_text().strip() == 'yes'
        items.append(item)

    return items


def calculate_statistics(data):
    init_price = data[0]['price']
    price_max, price_min, price_sum  = init_price, init_price, 0
    size_frequencies = {}

    for item in data:
        size = item['size']
        if size in size_frequencies:
            size_frequencies[size] += 1
        else:
            size_frequencies[size] = 1
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

    for k, v in size_frequencies.items():
        size_frequencies[k] = round(v / len(data), 3)

    size_frequencies = dict(sorted(size_frequencies.items(), key=lambda d: d[0], reverse=True))

    return {'price_max': price_max, 'price_min': price_min, 'price_sum': price_sum, 'price_avg': price_avg,
            'price_standard_deviation': price_standard_deviation, 'size_frequencies': size_frequencies}


def sort_and_filter(data):
    sorted_data = sorted(data, key=lambda d: d['reviews'], reverse=True)
    return list(filter(lambda d: d['rating'] > 4.5, sorted_data))


def read_file(path):
    with open(path, newline='', encoding="utf-8") as file:
        return file.read()


def read_data():
    items = []
    for i in range(1, 155):
        xml = read_file(f"../data/4/{i}.xml")
        items.extend(extract_items_data(xml))
    return items

def write_to_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


data = read_data()
result_data = sort_and_filter(data)
statistics = calculate_statistics(data)
write_to_json("task_4_original_result.json", data)
write_to_json("task_4_sorted_and_filtered_result.json", result_data)
write_to_json("task_4_statistics_result.json", statistics)