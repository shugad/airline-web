import numpy as np
import pickle
import sklearn
import catboost
from scipy.special import inv_boxcox
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ALPHA = 0.30550104689624275

dict_groups_airlines = {
    'multiple carriers premium economy': 'premium', 'jet airways business': 'premium',
    'jet airways': 'premium', 'vistara': 'medium', 'vistara premium economy': 'medium',
    'goair': 'medium', 'multiple carriers': 'medium', 'air india': 'medium',
    'trujet': 'low-cost', 'spicejet': 'low-cost', 'indigo': 'low-cost', 'air asia': 'low-cost'
}

dict_airlines_enc = {'air asia': 0, 'air india': 1, 'goair': 2, 'indigo': 3,
                     'jet airways': 4, 'jet airways business': 5, 'multiple carriers': 6,
                     'multiple carriers premium economy': 7, 'spicejet': 8,
                     'trujet': 9, 'vistara': 10, 'vistara premium economy': 11}

dict_groups_airlines_enc = {'low-cost': 0, 'medium': 1, 'premium': 2}

dict_time_of_day_enc = {'Early Morning': 0, 'Morning': 1,
                        'Noon': 2, 'Eve': 3, 'Night': 4, 'Late Night': 5}

dict_season_enc = {'spring': '0', 'summer': '1', 'fall': '2', 'winter': '3'}


def get_group_airline(value):
    value = value.lower()
    dictionary = dict_groups_airlines
    category = dictionary[value]
    return encode_group_airline(category)


def encode_group_airline(value):
    value = value.lower()
    dictionary = dict_groups_airlines_enc
    return dictionary[value]


def encode_radio_1(value):
    if value == 'No':
        return 0
    else:
        return 1


def encode_radio(value):
    if value == 'No':
        return 0
    else:
        return 1


def encode_airline(value):
    value = value.lower()
    dictionary = dict_airlines_enc
    return dictionary[value]


def encode_time_of_day(value):
    dictionary = dict_time_of_day_enc
    return dictionary[value]


def encode_season(value):
    value = get_season(value)
    dictionary = dict_season_enc
    return dictionary[value]


# function for month extraction
def get_season(month):
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "fall"


def get_duration(hours, minutes):
    return int(hours) * 60 + int(minutes)


def get_prediction(model, x):
    if model == 'gbr':
        model_loaded = pickle.load(open(f'{BASE_DIR}/gbr.sav', 'rb'))
    elif model == 'catboost':
        model_loaded = pickle.load(open(f'{BASE_DIR}/catboost.sav', 'rb'))
    pred = model_loaded.predict([x])
    return np.round(inv_boxcox(pred, ALPHA)[0], 2)


def get_final_prediction(X):
    return np.round((get_prediction('gbr', X) + get_prediction('catboost', X))/2, 2)

