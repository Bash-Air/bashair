import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from http.client import HTTPException

import logging
from asgiref.sync import sync_to_async
from fastapi import APIRouter
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from fastapi import Request

from back.schemas.sensors import SensorData, SensorMeasurement
from config.envs import envs
from config.influx import client
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

router = APIRouter()

NAME_MAP = {
    "Max_cycle": "max_micro",
    "Samples": "samples",
    "Min_cycle": "min_micro",
    "Signal": "signal",
    "SDS_P1": "pm10",
    "SDS_P2": "pm25",
    "BME280_temperature": "temperature",
    "BME280_humidity": "humidity",
    "BME280_pressure": "pressure",
}


@router.post('/upload_measurement')
async def upload_measurement(data: SensorData, request: Request):
    from back.models.sensors import Node, SensorLocation

    node: Node = await sync_to_async(Node.objects.select_related('location').get, thread_sensitive=True)(uid=data.node_tag)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found.")
    print(request.client.host, node)

    data_points = {}
    for dp in data.sensordatavalues:
        data_points[dp.value_type] = dp.value
        data_points[NAME_MAP.get(dp.value_type, dp.value_type)] = dp.value

    try:
        sensor_measurement = SensorMeasurement(**data_points)
    except Exception as e:
        print(data.node_tag, e)
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e))

    sensor_measurement.aqi = sensor_measurement.get_aqi_value
    sensor_measurement.aqi_category = sensor_measurement.get_aqi_category

    # print(sensor_measurement.dict())

    write_api = client.write_api(write_options=SYNCHRONOUS)

    _dict = {
        "measurement": envs.MEASUREMENT_NAME,
        "fields": sensor_measurement.dict(),
        "tags": {
            "node": data.node_tag,
            "location": node.location.location,
            "lat": node.location.latitude,
            "lon": node.location.longitude,
            "city": node.location.city,
            "street": node.location.street_name,
        },
    }

    p = Point.from_dict(_dict)

    write_api.write(bucket=envs.MEASUREMENT_NAME, record=p)

    return True