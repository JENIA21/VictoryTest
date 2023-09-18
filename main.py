import schedule


def job():
    print('Boo')


# run job until a 2030-01-01 18:33 today
schedule.every(1).hours.until("2023-09-18 08:47").do(job)
