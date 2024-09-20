import pika
import time
import random
import os
import logging
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up connection parameters
rabbitmq_host = os.getenv('RABBITMQ_HOST')  # RabbitMQ container name

# Check if the RabbitMQ host is set
if not rabbitmq_host:
    logging.error("RABBITMQ_HOST environment variable is not set")
    exit(1)

logging.info(f"RabbitMQ host: {rabbitmq_host}")
connection_params = pika.ConnectionParameters(host=rabbitmq_host)

# Function to send messages
def send_message(channel, message):
    # Send a message back to the queue
    channel.basic_publish(exchange='',
                          routing_key='test_queue',
                          body=message)
    
    print(f" [x] Sent '{message}'")

# Function to handle received messages and send a response
def on_message_received(ch, method, properties, body):
    received_message = body.decode()
    print(f" [x] Received '{received_message}'")
    
    # Create a response message
    response_message = f"Response to '{received_message}' from {random.randint(1, 1000)}"
    
    # Simulate some processing time
    time.sleep(2)
    
    # Send the response message
    send_message(ch, response_message)

# Function to start the auto-messaging system
def start_auto_messaging(start_with_message):
    # Set up a connection and channel
    logging.info(f"Establishing connection: {connection_params}")
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    
    logging.info("Connection established")

    # Declare a queue
    channel.queue_declare(queue='test_queue')

    # Check if the system should start by sending a message
    if start_with_message:
        logging.info("Starting with an initial message")
        initial_message = f"Initial message from {random.randint(1, 1000)}"
        send_message(channel, initial_message)

    # Start consuming and handle each message with the on_message_received function
    channel.basic_consume(queue='test_queue',
                          on_message_callback=on_message_received,
                          auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    # Read environment variable to check if the system should start by sending a message
    start_with_message = os.getenv('START_WITH_MESSAGE', 'false').lower() == 'true'
    logging.info(f"Does it start messaging: {start_with_message}")
    
    # Start the auto-messaging system
    start_auto_messaging(start_with_message)
