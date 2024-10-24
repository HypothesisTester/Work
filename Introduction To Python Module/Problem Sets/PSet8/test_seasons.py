from datetime import date, timedelta
from seasons import calculate_age_in_minutes, convert_to_words

def test_calculate_age_in_minutes():
    today = date.today()
    one_year_ago = today - timedelta(days=365)
    assert calculate_age_in_minutes(one_year_ago) == 525600

def test_convert_to_words():
    assert convert_to_words(525600) == "five hundred and twenty-five thousand six hundred"
    assert convert_to_words(1051200) == "one million fifty-one thousand two hundred"