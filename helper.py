from datetime import datetime
import math

def date_format(date: str, month: str, year: str) -> str:
    return f"{date}-{month}-{year}"

def date_validation(date: str) -> bool:
    try:
        datetime.strptime(date, '%d-%m-%Y')
        return True
    except ValueError:
        return False

def date_css_selector(date: datetime) -> str:
    first_date_obj = date.replace(day=1)
    date_ind = first_date_obj.weekday() + date.day
    row_index = math.floor(date_ind/7) + 1
    col_index = date_ind % 7
    css_selector = f"tbody > tr:nth-child({row_index}) > td:nth-child({col_index})"
    return css_selector

def price_format(price: str) -> int:
    return int(price.replace(",", ""))

#
# def main():
#     date_str = "27-02-2025"
#     print(date_validation(date_str))
#     print(date_css_selector(date_str))
#
#
# if __name__ == "__main__":
#     main()
