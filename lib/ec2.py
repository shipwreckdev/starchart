import boto3
import os

# AWS Credentials
ACCESS_KEY = os.getenv("ACCESS_KEY")
REGION = os.getenv("AWS_REGION")
SECRET_KEY = os.getenv("SECRET_KEY")

ec2 = boto3.resource(
    'ec2',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION,
)

def InstanceIDList():
  # Builds a list of EC2 instances.

  instance_id_list = []

  for i in ec2.instances.all():
    if i.state['Name'] == 'running':
      instance_id_list.append(i.id)
    else:
      continue

  return instance_id_list

def InstancePublicIPList():
  # Builds a list of EC2 public IP addresses.

  instance_ip_list = []

  for i in ec2.instances.all():
    if i.state['Name'] == 'running':
      instance_ip_list.append(i.public_ip_address)
    else:
      continue

  return instance_ip_list

def InstancePrivateIPList():
  # Builds a list of EC2 private IP addresses.

  instance_ip_list = []

  for i in ec2.instances.all():
    if i.state['Name'] == 'running':
      instance_ip_list.append(i.private_ip_address)
    else:
      continue

  return instance_ip_list

def GetNameTag(instance):
  # Gets defined instance tags.
  i = ec2.Instance(instance)

  taglist = []

  for tags in i.tags:
    if tags["Key"] == 'Name':
      taglist.append(tags["Value"])

  return taglist
