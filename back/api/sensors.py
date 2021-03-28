import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from http.client import HTTPException

from fastapi import APIRouter
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from back.schemas.sensors import SensorData, SensorMeasurement
from config.envs import envs
from config.influx import client

router = APIRouter()

#
# @router.get("/")
# def get_choices(
#     choices: List[Choice] = Depends(adapters.retrieve_choices),
# ) -> FastChoices:
#     return FastChoices.from_qs(choices)


@router.post('/push')
async def upload_measurement(data: SensorData):
    # print(data)

    from back.models.sensors import Node

    instance = Node.objects.filter(uid=data.node_tag).first()
    if not instance:
        raise HTTPException(status_code=404, detail="Node not found.")
    return instance


    print(node)

    data_points = {}
    for dp in data.sensordatavalues:
        data_points[dp.value_type] = dp.value

    sensor_measurement = SensorMeasurement(
        pm10=data_points['SDS_P1'],
        pm25=data_points['SDS_P2'],
        temperature=data_points['BME280_temperature'],
        pressure=data_points['BME280_pressure'],
        humidity=data_points['BME280_humidity'],
        samples=data_points['samples'],
        min_micro=data_points['min_micro'],
        max_micro=data_points['max_micro'],
        signal=data_points['signal'],
    )

    sensor_measurement.aqi = sensor_measurement.get_aqi_value
    sensor_measurement.aqi_category = sensor_measurement.get_aqi_category

    # print(sensor_measurement.dict())

    write_api = client.write_api(write_options=SYNCHRONOUS)

    p = Point.from_dict({
        "measurement": envs.MEASUREMENT_NAME,
        "fields": sensor_measurement.dict(),
        "tags": {
            "node": data.node_tag
        },
    }
    )

    write_api.write(bucket=envs.MEASUREMENT_NAME, record=p)

    return sensor_measurement.dict()