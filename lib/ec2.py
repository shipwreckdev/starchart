import boto3

ec2 = boto3.resource('ec2')

def InstanceIDList():
  """Builds a list of EC2 instances."""

  instance_id_list = []

  for i in ec2.instances.all():
    instance_id_list.append(i.id)

  return instance_id_list

def InstancePublicIPList():
  """Builds a list of EC2 public IP addresses."""

  instance_ip_list = []

  for i in ec2.instances.all():
    instance_ip_list.append(i.public_ip_address)

  return instance_ip_list

def InstancePrivateIPList():
  """Builds a list of EC2 private IP addresses."""

  instance_ip_list = []

  for i in ec2.instances.all():
    instance_ip_list.append(i.private_ip_address)

  return instance_ip_list

def GetNameTag(instance):
  i = ec2.Instance(instance)

  taglist = []

  for tags in i.tags:
    if tags["Key"] == 'Name':
      taglist.append(tags["Value"])

  return taglist
