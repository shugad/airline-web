from django.shortcuts import render
from datetime import datetime
from .handler.preprocessing import get_group_airline, encode_airline, \
    encode_season, encode_time_of_day, encode_radio, get_duration, get_final_prediction


def home(request):
    if request.POST:
        airline = request.POST['user_airline']
        total_stops = request.POST['user_total_stops']
        date = request.POST['user_date']
        month = datetime.strptime(request.POST['user_date'], "%Y-%m-%d").month
        day = datetime.strptime(request.POST['user_date'], "%Y-%m-%d").day
        season = encode_season(month)
        airline_group = get_group_airline(airline)
        airline_encoded = encode_airline(airline)
        hours = request.POST['user_hours']
        minutes = request.POST['user_minutes']
        duration = get_duration(hours, minutes)
        period_of_day = request.POST['user_duration_time']
        period_of_day_enc = encode_time_of_day(period_of_day)
        user_baggage = encode_radio(request.POST['user_baggage'])
        user_layover = encode_radio(request.POST['user_long_layover'])
        user_business = encode_radio(request.POST['user_business_class'])
        user_change = encode_radio(request.POST['user_change_airports'])
        user_meal = encode_radio(request.POST['user_meal'])
        X = []
        X.append(airline_encoded)
        X.append(total_stops)
        X.append(month)
        X.append(day)
        X.append(season)
        X.append(period_of_day_enc)
        X.append(user_layover)
        X.append(user_business)
        X.append(user_change)
        X.append(user_meal)
        X.append(user_baggage)
        X.append(airline_group)
        X.append(duration)

        predicted = get_final_prediction(X)

        context = {'airline': airline, 'date': date,
                   'hours': hours, 'minutes': minutes,
                   'X': X, 'predicted': predicted}

        return render(request, 'main/output.html', context)
    return render(request, 'main/input.html')

