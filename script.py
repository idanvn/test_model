import datetime

def get_current_date_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    current_date_time = get_current_date_time()
    print(f"Current Date and Time: {current_date_time}")
