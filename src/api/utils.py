from typing import Annotated

from fastapi import Request, Depends

from src.core import RabbitMQProducer


def get_producer(request: Request):
    return request.app.state.rabbitmq_producer


RabbitMQProducerDep = Annotated[RabbitMQProducer, Depends(get_producer)]
