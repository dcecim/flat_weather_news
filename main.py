import flet as ft
import requests

API_KEY = 'd51c4b2113303483460c4c6f1fcdefc3'

# Build out the API and get a response
BASE_URL = 'http://api.openweathermap.org/geo/1.0/direct?'
# BASE_URL = 'https://api.stormglass.io/v2/weather/point'

def get_weather(latitude, longitude):
    params = {'lat':latitude, 'lon':longitude, 'appid': API_KEY}
    resposta = requests.get(BASE_URL, params=params)

    if resposta.status_code == 200:
        dados = resposta.json()
        return {
            'cidade': dados['name'],
            'tempo': dados['main']['temp'],
            'humidade': dados['main']['humidity'],
            'clima': dados['weather'][0]['description'],
            'latitude': dados['coord']['lat'],
            'longitude': dados['coord']['lon'],
        }
    return None

# print(get_weather(latitude= -15.7801, longitude= -47.9292))

def main(page: ft.Page):
    page.title = 'Noticias do Clima'
    page.bgcolor= ft.colors.BLUE_GREY_900
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 500
    page.window.height = 700



if __name__ == '__main__':
    ft.app(target=main)