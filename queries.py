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

        print(f"\nPäivän {user_date} hinnat tunneittain:")
        for table in tables:
            for record in table.records:
                print(f"{record['_time'].hour}:00    {round(record['_value'], 3)} ¢")


    except Exception as e:
        print(e)

    finally:
        if client is not None:
            client.close()

