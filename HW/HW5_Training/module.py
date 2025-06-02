import requests


def add_numbers(a, b):
    return a + b


def is_even(number):
    return number % 2 == 0


def fetch_data(url):
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None


def process_mock_object(obj):
    return obj.value * 2 if obj.value > 0 else None


def run_data_pipeline(data_processor):
    prepared_data = data_processor.process_data().analyze_data()
    prepared_data.save_result()


def divide_numbers(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
    except TypeError:
        print("Error: Unsupported operand type(s) for division!")
    else:
        return result


def check_even_odd(numbers, url):
    result = []
    for number in numbers:
        response = requests.get(f'{url}/{number}').json()['results'][0]['value']
        if response % 2 == 0:
            result.append("Even")
        else:
            result.append("Odd")
    return result


class DataProcessor:
    def process_data(self, data):
        return [x * 2 for x in data]

    def analyze_data(self, data):
        processed_data = self.process_data(data)
        return sum(processed_data)
