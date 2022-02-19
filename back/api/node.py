from django.contrib.auth.models import User
from django.db.models import Q
from fastapi import APIRouter, Depends
from pydantic import ValidationError

from back.api.weather import get_weather
from back.depends.user import get_current_active_user
from back.models.node import Node
from back.schemas.node import NodePointGet, SensorLocationPointGet, ListNodes, ListNodeMetrics
from back.time_series.air import InfluxAir
from back.utils.exceptions import NotFound, PermissionDenied
from config.owm import weather_manager

router = APIRouter(tags=["node"], prefix="/node")


def create_node_response(node: Node) -> NodePointGet:
    metrics = node.get_metrics()
    if not metrics: return
    if not metrics.pm25: return

    try:
        result = NodePointGet(**metrics.dict(), **node.__dict__)
    except ValidationError as e:
        print(e)
        return

    result.wind = get_weather(latitude=node.latitude, longitude=node.longitude)
    # result.location = node.location
    result.aqi_category = result.get_aqi_category()
    # TODO: где имя? пустое приходит
    result.name = node.name
    result.city = node.city.name

    return result


@router.get('/all', response_model=ListNodes)
def get_nodes():
    nodes_query = Node.objects.all()
    nodes = []

    for node in nodes_query:
        if not node.point: continue
        # todo: не делать много повторно запросов к инфлюкс а сразу брать все
        result = create_node_response(node)
        if result:
            nodes.append(result.dict())
    return nodes


@router.get('/{node_id}', response_model=NodePointGet)
def get_node(node_id: int):
    """
    Данные по датчику
    todo: рефакторить, положить метрики в отдельный массив
    """

    try:
        node = Node.objects.get(id=node_id)
    except Node.DoesNotExist:
        raise NotFound

    result = create_node_response(node)

    return result


@router.get('/{node_id}/history', response_model=ListNodeMetrics)
def get_node_history(node_id: int):
    try:
        node = Node.objects.get(id=node_id)
    except Node.DoesNotExist:
        raise NotFound
    return node.get_history()


@router.post('/')
def create_node(user: User = Depends(get_current_active_user)):
    if not user.is_staff:
        raise PermissionDenied
    pass
