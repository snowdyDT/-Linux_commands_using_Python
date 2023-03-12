import requests

json_data_client = {
    'iin': '',
    'summ': '',
    'dbz': ''
}


def post_request(url, json_data):
    res = requests.post(url, json=json_data)
    print(res.text)


if __name__ == "__main__":
    print(f"Data for POST request: {json_data_client}")
    post_request("http://127.0.0.1:8080/data_service", json_data_client)
