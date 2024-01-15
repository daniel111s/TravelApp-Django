import requests
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from .models import Travel, Task
from .forms import TravelForm, TaskForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta


def remove_spaces(city_name):
    # Usuń spacje z nazwy miasta i zwróć pojedynczy ciąg znaków
    return city_name.replace(" ", "")


def travelList(request):
    # Pobierz wszystkie podróże (travels) z bazy danych
    travels = Travel.objects.all()

    # Przekazuj listę podróży jako kontekst do szablonu HTML
    context = {'travels': travels}


    # Renderuj szablon HTML z kontekstem i zwróć jako odpowiedź
    return render(request, 'travelList.html', context)


def home_page(request):
    return render(request, 'homePage.html')


@login_required
def new_travel(request):
    form = TravelForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(travelList)

    return render(request, 'new_travel.html', {'form': form})


@login_required
def edit_travel(request, id):
    travel = get_object_or_404(Travel, pk=id)

    form = TravelForm(request.POST or None, instance=travel)

    if form.is_valid():
        form.save()
        return redirect(travelList)

    return render(request, 'edit_travel.html', {'form': form})


@login_required
def delete_travel(request, id):
    travel = get_object_or_404(Travel, pk=id)

    if request.method == 'POST':
        travel.delete()
        return redirect(travelList)

    return render(request, 'confirm_delete.html', {'travel': travel})



def show_details(request, id):
    travel = get_object_or_404(Travel, pk=id)

    # Pobieranie zdjęć z Unsplash API
    access_key = 'Pt95CjM-fdMfvzhDLPV2zh8JTGLhbr59661GgCvwVhs'
    api_url = f'https://api.unsplash.com/photos/random?query={travel.city}&client_id={access_key}&count=25&orientation=landscape'# Pobierz 25 zdjęć poziomych

    city_images = []

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        for item in data:
            image_url = item.get('urls', {}).get('regular', None)
            if image_url:
                city_images.append(image_url)
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas próby pobrania obrazów z Unsplash: {e}")

    # Użyj obrazów zapasowych, jeśli nie znaleziono URL z Unsplash
    if not city_images:
        city_images.append(f"/static/city_images/{travel.city}.jpg")

    # Pobieranie prognozy pogodowej
# Fragment odpowiedzialny za pracę z API Visual Crossing oraz wyświetlanie inforamcji pogodowych w karuzeli
    def kelvin_to_celsius(kelvin):
        return kelvin - 273.15

    travel = get_object_or_404(Travel, pk=id)
    weather_data_list = []

    if travel.city:
        api_key = "BAXWSR86V9LCTJC333BMU6LHN"
        base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

        # Specify the location and date range for the weather data
        location = f"{travel.city},{travel.country}"
        start_date = travel.start_date.strftime('%Y-%m-%d')
        end_date = travel.end_date.strftime('%Y-%m-%d')

        # Construct the API URL
        url = f"{base_url}{location}/{start_date}/{end_date}?unitGroup=metric&key={api_key}"
        response = requests.get(url)
        weather_data = response.json()

        # Process the weather data
        for entry in weather_data['days']:
            date = datetime.strptime(entry['datetime'], '%Y-%m-%d')
            temperature = round(entry['tempmax'])
            weather_description = entry['conditions'].replace(" ", "_").lower()
            weather_icon_url = f'/static/city_images/Other/Weather_images/{weather_description}.jpg'

            weather_data = {
                'dt': date.strftime('%Y-%m-%d'),
                'main': {'temp': temperature},
                'weather': [{'description': entry['conditions']}],
                'weather_icon_url': weather_icon_url
            }

            weather_data_list.append(weather_data)

    return render(request, 'details.html', {'travel': travel, 'city_images': city_images, 'weather_data_list': weather_data_list})


def show_gallery(request, id):
    travel = get_object_or_404(Travel, pk=id)

    # Pobieranie zdjęć z Unsplash API
    access_key = 'Pt95CjM-fdMfvzhDLPV2zh8JTGLhbr59661GgCvwVhs'
    api_url = f'https://api.unsplash.com/photos/random?query={travel.city}&client_id={access_key}&count=100&orientation=landscape'  # Pobierz 100 zdjęć poziomych

    city_images = []

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        for item in data:
            image_url = item.get('urls', {}).get('regular', None)
            if image_url:
                city_images.append(image_url)
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas próby pobrania obrazów z Unsplash: {e}")

    # Użyj obrazów zapasowych, jeśli nie znaleziono URL z Unsplash
    if not city_images:
        city_images.append(f"/static/city_images/{travel.city}.jpg")

    return render(request, 'gallery.html', {'travel': travel, 'city_images': city_images})


def find_restaurants(request, id):
    travel = get_object_or_404(Travel, pk=id)
    restaurants = []
    api_key = 'AIzaSyDid74zryD1kYtklWI01JOTfqaClAOGXQE'

    if travel.city:
        # Tworzenie zapytania do Google Places API, aby znaleźć restauracje w okolicy
        query = f'restaurants in {travel.city}, {travel.country}'
        url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}'

        response = requests.get(url)
        data = response.json()

        if 'results' in data:
            restaurants = data['results']

            # Przechodzimy przez znalezione restauracje i uzyskujemy photo_reference
            for restaurant in restaurants:
                if 'photos' in restaurant:
                    photo_reference = restaurant['photos'][0]['photo_reference']  # Uzyskanie pierwszej photo_reference
                else:
                    photo_reference = ''  # Jeśli brak zdjęć, przypisz pusty string

                # Dodajemy place_id i photo_reference do wyników miejsc
                restaurant['restaurant_id'] = restaurant.get('restaurant_id', '')
                restaurant['photo_reference'] = photo_reference

    return render(request, 'restaurants.html', {'travel': travel, 'restaurants': restaurants, 'api_key': api_key})


def find_places(request, id):
    travel = get_object_or_404(Travel, pk=id)
    api_key = 'AIzaSyDid74zryD1kYtklWI01JOTfqaClAOGXQE'

    if travel.city:
        # Tworzenie zapytania do Google Places API, aby znaleźć miejsca w okolicy
        query = f'places in {travel.city}, {travel.country}'
        url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}'

        response = requests.get(url)
        data = response.json()

        if 'results' in data:
            places = data['results']

            # Przechodzimy przez znalezione miejsca i uzyskujemy photo_reference
            for place in places:
                if 'photos' in place:
                    photo_reference = place['photos'][0]['photo_reference']  # Uzyskanie pierwszej photo_reference
                else:
                    photo_reference = ''  # Jeśli brak zdjęć, przypisz pusty string

                # Dodajemy place_id i photo_reference do wyników miejsc
                place['place_id'] = place.get('place_id', '')
                place['photo_reference'] = photo_reference

    return render(request, 'places.html', {'travel': travel, 'places': places, 'api_key': api_key})


def find_hotels(request, id):
    travel = get_object_or_404(Travel, pk=id)
    api_key = 'AIzaSyDid74zryD1kYtklWI01JOTfqaClAOGXQE'

    if travel.city:
        # Tworzenie zapytania do Google Places API, aby znaleźć hotele w okolicy
        query = f'hotels in {travel.city}, {travel.country}'
        url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}'

        response = requests.get(url)
        data = response.json()

        if 'results' in data:
            hotels = data['results']

            # Przechodzimy przez znalezione hotele i uzyskujemy photo_reference
            for hotel in hotels:
                if 'photos' in hotel:
                    photo_reference = hotel['photos'][0]['photo_reference']  # Uzyskanie pierwszej photo_reference
                else:
                    photo_reference = ''  # Jeśli brak zdjęć, przypisz pusty string

                # Dodajemy place_id i photo_reference do wyników miejsc
                hotel['hotel_id'] = hotel.get('hotel_id', '')
                hotel['photo_reference'] = photo_reference

    return render(request, 'hotels.html', {'travel': travel, 'hotels': hotels, 'api_key': api_key})


@login_required
def add_task(request, id):
    travel = get_object_or_404(Travel, pk=id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.travel = travel
            task.save()
            return redirect('task_list', id=id)
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form, 'travel': travel})


def task_list(request, id):
    travel = get_object_or_404(Travel, pk=id)
    tasks = Task.objects.filter(travel=travel)
    return render(request, 'task_list.html', {'tasks': tasks, 'travel': travel})



@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, pk=id)

    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()
        return redirect('task_list', id=task.travel.id)

    return render(request, 'edit_task.html', {'form': form})


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, pk=id)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list', id=task.travel.id)

    return render(request, 'confirm_delete_task.html', {'task': task})











