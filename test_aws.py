import boto3
client = boto3.client('sts')
client_identity = client.get_caller_identity()
print(client_identity)
