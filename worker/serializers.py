import json
from dataclasses import dataclass

from worker.abstract import MessageSerializer, Message


@dataclass
class CreateOrderMessage(Message):
    order_number: str


class CreateOrderMessageSerializer(MessageSerializer):

    def deserialize(self, raw_message: str) -> CreateOrderMessage:
        message = json.loads(raw_message)
        return CreateOrderMessage(raw_content=raw_message,
                                  order_number=message['order_number'])
