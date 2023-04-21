import requests
import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

def bring_values():

    token = "Q1CuZ3BC0tumrOyiffrftR16OqZJiY72hwfu4v7em0BUVeJoQEHBho4TItLXX7nj9WjK5NCsdCkLL5ZCLBpfoQ=="
    org = "my_org"
    url = "http://localhost:8086"
    client = None

    try:

        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        bucket = "e_prices"

        res = requests.get('http://spotprices.energyecs.frostbit.fi/api/v1/prices')
        prices_list = res.json()

        write_api = client.write_api(write_options=SYNCHRONOUS)

        for p in prices_list:
            point = (
                # change these to match yours
                Point("electricity_price")
                    .field("price", float(p['value']))
                    .time(p['_time'])
            )
            write_api.write(bucket=bucket, org=org, record=point)

    except Exception as e:
        print(e)

    finally:
        if client is not None:
            client.close()

