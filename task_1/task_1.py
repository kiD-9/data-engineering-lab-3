from bs4 import BeautifulSoup
import math
import json


def extract_item_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    no_class_spans = soup.find_all('span', attrs={'class': ''})
    item = {}

    item['type'] = no_class_spans[0].get_text().split(':')[1].strip()
    item['id'] = int(soup.h1['id'])
    item['tournament'] = soup.h1.get_text().split(':')[1].strip()
    p = soup.p.get_text().split('Город:')[1].split('Начало:')
    item['city'] = p[0].strip()
    item['start_date'] = p[1].strip()
    item['tours'] = int(soup.find('span', attrs={'class': 'count'}).get_text().split(':')[1].strip())
    item['game_time_minutes'] = int(soup.find('span', attrs={'class': 'year'}).get_text().split(':')[1].split()[0].strip())
    item['min_rating'] = int(no_class_spans[1].get_text().split(':')[1].strip())
    item['img'] = soup.img['src']
    item['tournament_rating'] = float(no_class_spans[2].get_text().split(':')[1].strip())
    item['views'] = int(no_class_spans[3].get_text().split(':')[1].strip())
    return item


def calculate_statistics(data):
    init_views = data[0]['views']
    views_max, views_min, views_sum  = init_views, init_views, 0
    type_frequencies = {}

    for item in data:
        type = item['type']
        if type in type_frequencies:
            type_frequencies[type] += 1
        else:
            type_frequencies[type] = 1
        views = item['views']
        views_sum += views
        if views < views_min:
            views_min = views
        if views > views_max:
            views_max = views

    views_avg = round(views_sum / len(data), 4)
    sum_pow = 0
    for item in data:
        sum_pow += ((item['views'] - views_avg) ** 2)
    views_standard_deviation = round(math.sqrt(sum_pow / len(data)), 4)

    for k, v in type_frequencies.items():
        type_frequencies[k] = round(v / len(data), 3)

    return {'views_max': views_max, 'views_min': views_min, 'views_sum': views_sum, 'views_avg': views_avg,
            'views_standard_deviation': views_standard_deviation, 'type_frequencies': type_frequencies}


def sort_and_filter(data):
    sorted_data = sorted(data, key=lambda d: d['views'], reverse=True)
    return list(filter(lambda d: d['game_time_minutes'] > 100, sorted_data))


def read_file(path):
    with open(path, newline='', encoding="utf-8") as file:
        return file.read()


def read_data():
    items = []
    for i in range(2, 80):
        html = read_file(f"../data/1/{i}.html")
        items.append(extract_item_data(html))
    return items

def write_to_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


data = read_data()
result_data = sort_and_filter(data)
statistics = calculate_statistics(data)
write_to_json("task_1_original_result.json", data)
write_to_json("task_1_sorted_and_filtered_result.json", result_data)
write_to_json("task_1_statistics_result.json", statistics)
