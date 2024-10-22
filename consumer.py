from kafka import KafkaConsumer, KafkaProducer
import json

def process_data(message):
    """Processes data and handles missing fields."""
    try:
        # Simulate processing of user login data
        data = json.loads(message)
        if 'device_type' not in data:
            data['device_type'] = 'unknown'
        return data
    except Exception as e:
        print(f"Error processing message: {e}")
        return None

consumer = KafkaConsumer(
    'user-login',
    bootstrap_servers='localhost:29092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='user-logins-group',
    value_deserializer=lambda x: x.decode('utf-8')
)

producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

for message in consumer:
    data = process_data(message.value)
    if data:
        producer.send('processed-user-login', value=data)
        print(f"Produced processed data: {data}")
