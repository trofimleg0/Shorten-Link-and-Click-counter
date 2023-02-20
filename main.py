import os
import requests
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_urls', nargs='+')

    return parser.parse_args().user_urls


def is_bitlink(bitly_token, user_url):
    parsed_url = urlparse(user_url)
    netloc, path = parsed_url.netloc, parsed_url.path

    headers = {'Authorization': f'Bearer {bitly_token}'}

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{netloc}{path}',
        headers=headers)

    return response.ok


def missing_schema(user_url):
    parsed_url = urlparse(user_url)

    if not parsed_url.scheme:
        user_url = f'http://{user_url}'

    return user_url


def is_correct_link(user_url):
    response = requests.get(user_url)
    response.raise_for_status()

    return response.ok


def shorten_link(bitly_token, user_url):
    headers = {'Authorization': f'Bearer {bitly_token}'}
    payload = {'long_url': user_url}

    response = requests.post('https://api-ssl.bitly.com/v4/shorten',
                             headers=headers,
                             json=payload)

    response.raise_for_status()

    return response.json()['link']


def count_clicks(bitly_token, user_url):
    parsed_url = urlparse(user_url)
    netloc, path = parsed_url.netloc, parsed_url.path

    headers = {'Authorization': f'Bearer {bitly_token}'}

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{netloc}{path}/clicks/summary',
        headers=headers)

    response.raise_for_status()

    return response.json()['total_clicks']


if __name__ == '__main__':
    load_dotenv()

    bitly_token = os.environ['BITLY_TOKEN']
    user_urls = get_args()

    for i, user_url in enumerate(user_urls):
        try:
            if is_bitlink(bitly_token, user_url):
                print(
                    f'{i+1}.Count of clicks for the bitlink:',
                    count_clicks(bitly_token, user_url),
                )
            else:
                user_url = missing_schema(user_url)
                if is_correct_link(user_url):
                    bitlink = shorten_link(bitly_token, user_url)
                    print(f'{i+1}.Your bitlink:',
                          bitlink[bitlink.find('://') + 3:])
        except requests.exceptions.HTTPError:
            print('Error 404. Page Not Found')
        except requests.exceptions.ConnectionError:
            print('Please write the correct page. '
                  'For example: https://www.github.com/')
