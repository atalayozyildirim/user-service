import boto3
import os

# AWS bağlantı ayarları
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='eu-north-1'
)

dynamodb = session.resource('dynamodb')

# Tablo oluşturma
table_name = 'users'

try:
    table = dynamodb.Table(table_name)
    table.load()  # Bu tablo yoksa bir istisna fırlatır
    print(f"Tablo {table_name} mevcut ve erişilebilir.")
except dynamodb.meta.client.exceptions.ResourceNotFoundException:
    print(f"Tablo {table_name} mevcut değil. Tablo oluşturuluyor...")
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'username',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(f"Tablo {table_name} başarıyla oluşturuldu.")