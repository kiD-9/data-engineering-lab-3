from bs4 import BeautifulSoup
import math
import json


def extract_item_data(xml):
    soup = BeautifulSoup(xml, 'xml')
    item = {}
    for e in soup.star:
        if e.name is not None:
            item[e.name.replace("-", "_")] = e.get_text().strip()

    item['radius'] = int(item['radius'])
    return item


def calculate_statistics(data):
    init_radius = data[0]['radius']
    radius_max, radius_min, radius_sum  = init_radius, init_radius, 0
    constellation_frequencies = {}

    for item in data:
        constellation = item['constellation']
        if constellation in constellation_frequencies:
            constellation_frequencies[constellation] += 1
        else:
            constellation_frequencies[constellation] = 1
        radius = item['radius']
        radius_sum += radius
        if radius < radius_min:
            radius_min = radius
        if radius > radius_max:
            radius_max = radius

    radius_avg = round(radius_sum / len(data), 4)
    sum_pow = 0
    for item in data:
        sum_pow += ((item['radius'] - radius_avg) ** 2)
    radius_standard_deviation = round(math.sqrt(sum_pow / len(data)), 4)

    for k, v in constellation_frequencies.items():
        constellation_frequencies[k] = round(v / len(data), 3)

    return {'radius_max': radius_max, 'radius_min': radius_min, 'radius_sum': radius_sum, 'radius_avg': radius_avg,
            'radius_standard_deviation': radius_standard_deviation, 'type_frequencies': constellation_frequencies}


def sort_and_filter(data):
    sorted_data = sorted(data, key=lambda d: d['radius'], reverse=True)
    return list(filter(lambda d: float(d['age'].replace(' billion years', '')) > 4, sorted_data))


def read_file(path):
    with open(path, newline='', encoding="utf-8") as file:
        return file.read()


def read_data():
    items = []
    for i in range(1, 189):
        xml = read_file(f"../data/3/{i}.xml")
        items.append(extract_item_data(xml))
    return items

def write_to_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


data = read_data()
result_data = sort_and_filter(data)
statistics = calculate_statistics(data)
write_to_json("task_3_original_result.json", data)
write_to_json("task_3_sorted_and_filtered_result.json", result_data)
write_to_json("task_3_statistics_result.json", statistics)
