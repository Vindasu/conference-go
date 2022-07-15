from datetime import datetime
import json
from operator import is_
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendees_bc.settings")
django.setup()

from attendees.models import AccountVO


def update_AccountVO(ch, method, properties, body):
    print("updated account")
    content = json.loads(body)
    first_name = content["first_name"]
    last_name = content["last_name"]
    email = content["email"]
    is_active = content["is_active"]
    updated_string = content["updated"]
    updated = datetime.fromisoformat(updated_string)
    if is_active:
        account = AccountVO.objects.update_or_create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            updated=updated,
        )
        account.save()
    else:
        account = AccountVO.objects.get(email=email).delete()
        account.delete()


while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq")
        )
        channel = connection.channel
        queue_name = channel.queue_declare(queue="")
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=update_AccountVO,
            auto_ack=True,
        )
        channel.start_consuming()
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)


# Declare a function to update the AccountVO object (ch, method, properties, body)
#   content = load the json in body
#   first_name = content["first_name"]
#   last_name = content["last_name"]
#   email = content["email"]
#   is_active = content["is_active"]
#   updated_string = content["updated"]
#   updated = convert updated_string from ISO string to datetime
#   if is_active:
#       Use the update_or_create method of the AccountVO.objects QuerySet
#           to update or create the AccountVO object
#   otherwise:
#       Delete the AccountVO object with the specified email, if it exists


# Based on the reference code at
#   https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/python/receive_logs.py
# infinite loop
#   try
#       create the pika connection parameters
#       create a blocking connection with the parameters
#       open a channel
#       declare a fanout exchange named "account_info"
#       declare a randomly-named queue
#       get the queue name of the randomly-named queue
#       bind the queue to the "account_info" exchange
#       do a basic_consume for the queue name that calls
#           function above
#       tell the channel to start consuming
#   except AMQPConnectionError
#       print that it could not connect to RabbitMQ
#       have it sleep for a couple of seconds
