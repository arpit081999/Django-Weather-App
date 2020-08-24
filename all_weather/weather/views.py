import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=YOUR_API_KEY'
    
    err_msg = ''
    meassage = ''
    meassage_class = ''
    
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg='City does not exist in this world!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            meassage=err_msg
            meassage_class='is-danger'
        else:
            meassage= 'City added successfully!'
            meassage_class='is-success'
        

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data,
         'form' : form,
         'meassage' : meassage,
         'meassage_class' : meassage_class
         }
    return render(request, 'weather/weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
