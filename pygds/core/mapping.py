import datetime

MONTH_STR_FORMAT_TO_MONTH_NUMBER_FORMAT = {"JAN": "01", "FEB": "02", "MAR": "03", "APR": "04", "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08", "OCT": "09", "SEP": "10", "NOV": "11", "DEC": "12"}


def change_string_date(date: str):
    day = date[:2]
    month = date[2:5]
    year = date[5:]
<<<<<<< HEAD
    
    try:
        month = MONTH_STR_FORMAT_TO_MONTH_NUMBER_FORMAT[month]
    except KeyError:
=======
    try:
        month = MONTH_STR_FORMAT_TO_MONTH_NUMBER_FORMAT[month]
    except KeyError:
        return date
    if not month:
>>>>>>> 093c059ddd1ad35eef389a3579ad98108ef6d4fe
        return date

    for digit in year:
        if not digit.isdigit():
            return date
    new_date = month + "." + day + "." + year

    try:
        new_date = datetime.datetime.strptime(new_date, '%m.%d.%y').strftime('%m-%d-%Y')
    except Exception:
        return date
        
    return new_date
