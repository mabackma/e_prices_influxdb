import calendar
from datetime import datetime

import influxdb_client

def make_queries():

    token = "Q1CuZ3BC0tumrOyiffrftR16OqZJiY72hwfu4v7em0BUVeJoQEHBho4TItLXX7nj9WjK5NCsdCkLL5ZCLBpfoQ=="
    org = "my_org"
    url = "http://localhost:8086"
    client = None

    user_date = input("\nAnna päivämäärä YYYY-MM-DD: ")

    try:

        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

        query_api = client.query_api()

        # Päivän kaikki hinnat tunneittain.
        start_time = user_date + "T00:00:00Z"
        stop_time = user_date + "T23:59:59Z"

        query = f"""from(bucket: "e_prices") 
        |> range(start: {start_time}, stop: {stop_time}) """
        tables = query_api.query(query, org=org)

        sum = 0
        print(f"\nPäivän {user_date} hinnat tunneittain:")
        for table in tables:
            for record in table.records:
                print(f"{record['_time'].hour}:00    {round(record['_value'], 3)} ¢")
                sum += record['_value']
        print("AVG: " + str(round(sum/24, 3)))

        start_time = user_date[:7] + "-01T00:00:00Z"

        # Lasketaan montako päivää kuukaudessa on
        date_object = datetime.strptime(user_date, '%Y-%m-%d')
        days_in_month = calendar.monthrange(date_object.year, date_object.month)[1]
        stop_time = user_date[:7] + f"-{days_in_month}T23:59:59Z"

        # keskimääräiset päivähinnat kuukausittain
        query = f"""from(bucket: "e_prices")
         |> range(start: {start_time}, stop: {stop_time})
         |> filter(fn: (r) => r["_measurement"] == "electricity_price" and r["_field"] == "price")
         |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
         |> yield(name: "mean")"""
        tables = query_api.query(query, org=org)

        amount = 0
        sum = 0
        print(f"\nKeskimääräiset päivähinnat {user_date[:7]}:")
        for table in tables:
            for record in table.records:
                amount += 1
                if amount == len(table.records):
                    print(f"{record['_time'].day}.{record['_time'].month}    {round(record['_value'], 3)} ¢")
                else:
                    print(f"{record['_time'].day - 1}.{record['_time'].month}    {round(record['_value'], 3)} ¢")
                sum += record['_value']
        print("AVG: " + str(round(sum / days_in_month, 3)))

        start_time = user_date[:4] + "-01-01T00:00:00Z"
        stop_time = user_date[:4] + "-12-31T00:00:00Z"

        # keskimääräiset kuukausihinnat vuosittain
        query = f"""from(bucket: "e_prices")
         |> range(start: {start_time}, stop: {stop_time})
         |> filter(fn: (r) => r["_measurement"] == "electricity_price" and r["_field"] == "price")
         |> aggregateWindow(every: 1mo, fn: mean, createEmpty: false)
         |> yield(name: "mean")"""
        tables = query_api.query(query, org=org)

        amount = 0
        sum = 0
        print(f"\nKeskimääräiset kuukausihinnat {user_date[:4]}:")
        for table in tables:
            for record in table.records:
                amount += 1
                if amount == len(table.records):
                    print(f"{record['_time'].month}    {round(record['_value'], 3)} ¢")
                else:
                    print(f"{record['_time'].month - 1}    {round(record['_value'], 3)} ¢")
                sum += record['_value']
        print("AVG: " + str(round(sum / 12, 3)))

    except Exception as e:
        print(e)

    finally:
        if client is not None:
            client.close()
