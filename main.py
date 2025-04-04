import flet as ft
import requests
from googletrans import Translator
from flet_webview import WebView  # Altere a importação

translator = Translator()

API_KEY = 'f7de51de0e0e45058360b21570d1de91'
BASE_URL = 'https://api.weatherbit.io/v2.0/current?'
MAP_URL = 'https://www.openstreetmap.org/export/embed.html?bbox={lon}%2C{lat}%2C{lon}%2C{lat}&layer=mapnik'

def get_weather(cidade):
    params = {'city': cidade, 'key': API_KEY}
    resposta = requests.get(BASE_URL, params=params)

    if resposta.status_code == 200:
        dados = resposta.json()
        dados = dados['data'][0]
        return {
            'cidade': dados['city_name'],
            'temperatura': dados['app_temp'],
            'humidade': dados['rh'],
            'clima': dados['weather']['description'],
            'latitude': dados['lat'],
            'longitude': dados['lon'],
        }
    return None

def main(page: ft.Page):
    page.title = 'Noticias do Clima'
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 500
    page.window.height = 700

    cidade_input = ft.TextField(
        label='Informe a cidade',
        width=300,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        border_radius=10
    )

    resultado = ft.Column()
    
    # Criar o mapa usando o novo WebView
    mapa = WebView(url='', width=600, height=400, visible=False)

    def pesquisar_clima(e):
        cidade = cidade_input.value.strip()
        if not cidade:
            cidade_input.value = 'Por favor, informe a cidade...'
            page.update()
            return

        dados_clima = get_weather(cidade)

        if dados_clima:
            clima = str(dados_clima['clima']) 
            clima = translator.translate(clima, dest='pt')
            resultado.controls.clear()  # Limpa o conteúdo anterior
            resultado.controls.append(ft.Text(f"Cidade: {dados_clima['cidade']}", size=18, color=ft.Colors.WHITE))
            resultado.controls.append(ft.Text(f"Temperatura: {dados_clima['temperatura']}ºC", size=18, color=ft.Colors.WHITE))
            resultado.controls.append(ft.Text(f"Humidade: {dados_clima['humidade']}%", size=18, color=ft.Colors.WHITE))
            resultado.controls.append(ft.Text(f"Clima: {clima.text}", size=18, color=ft.Colors.WHITE))

            mapa.url = MAP_URL.format(lat=dados_clima['latitude'], lon=dados_clima['longitude'])
            mapa.visible = True
        else:
            resultado.controls.clear()
            resultado.controls.append(ft.Text('Cidade não encontrada...', size=18, color=ft.Colors.WHITE))
            mapa.visible = False

        page.update()

    bt_pesquisa = ft.ElevatedButton(
        'Pesquisar',
        on_click=pesquisar_clima,
        width=150,
        bgcolor=ft.Colors.BLUE_500,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=10)
    )
    
    container = ft.Container(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text('Noticias do clima', size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                cidade_input,
                bt_pesquisa,
                resultado,
                mapa
            ],
        ),
        alignment=ft.alignment.center,
        padding=20,
        bgcolor=ft.Colors.BLUE_GREY_800,
        shadow=ft.BoxShadow(blur_radius=15, spread_radius=2, color=ft.Colors.BLACK12)
    )
    
    page.add(container)

if __name__ == '__main__':
    ft.app(target=main)
