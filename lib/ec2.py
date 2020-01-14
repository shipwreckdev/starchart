import boto3

def InstanceIDList():
  """Builds a list of EC2 instances."""

  ec2 = boto3.resource('ec2')

  instance_id_list = []

  for i in ec2.instances.all():
    instance_id_list.append(i.id)

  return instance_id_list

def InstancePublicIPList():
  """Builds a list of EC2 public IP addresses."""

  ec2 = boto3.resource('ec2')

  instance_ip_list = []

  for i in ec2.instances.all():
    instance_ip_list.append(i.public_ip_address)

  return instance_ip_list

def InstancePrivateIPList():
  """Builds a list of EC2 private IP addresses."""

  ec2 = boto3.resource('ec2')

  instance_ip_list = []

  for i in ec2.instances.all():
    instance_ip_list.append(i.private_ip_address)

  return instance_ip_list

def tags(instance):
  for tags in ec2.instance.tags():
    if tags["Key"] == 'Name':
      instancename = tags["Value"]

  return instancename
