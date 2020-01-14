import argparse
import lib.ec2 as EC2
import lib.scan as Scanner
from lib.utils import info, failure, success, bold, italics, reset
import time

# Provide some timing details.
start_time = time.time()

# Parse for arguments.
parser = argparse.ArgumentParser(description='Run nmap scans against dynamic lists of scannable objects in cloud native environments.')
parser.add_argument('-t', '--type', dest='scan_type', type=str, help='This is to establish what type of scanning to use. Options are: public_ip (default), private_ip, kube', default='public_ip')
parser.add_argument('-a', '--all', dest='all_ports', help='If using a scan type of ip, scan ports 1-65535.', action='store_true')
parser.add_argument('-p', '--ports', dest='port_range', type=str, help='If not scanning all ports, set the port range to scan - ex: 22-26, 53 - This will default to 22 if no optional input is provided.', default='22')
parser.add_argument('-c', '--cloud-provider', dest='provider', type=str, help='The cloud provider where the tool is being used, if using provider-specific options. Options are: aws (default)', default='aws')
parser.add_argument('-o', '--os-discovery', dest='os_discovery', help='Enable OS detection for hosts IP based nmap scans.', action='store_true')
args = parser.parse_args()

# Establish variables.
all_ports = args.all_ports
os_discovery = args.os_discovery
port_range = args.port_range
provider = args.provider
scan_type = args.scan_type

scan_args = '-sS -vv -Pn -T5 {os_detect}'.format(os_detect='-O' if os_discovery == True else '') # -sS TCP_SYN scan, -vv verbose, -Pn skip discovery, -T5 timing template (higher is faster)

# Present some basic information.
print(italics('starchart'))
print()
if provider:
  print(success + bold(' Provider: ') + provider)
print(success + bold(' Type: ') + scan_type)
if port_range:
  print(success + bold(' Port Range: ') + str(port_range))
print()

# Build list of targets and scan.
if provider == 'aws' and (scan_type == 'public_ip' or scan_type == 'private_ip'):
  print(info + ' Looking for instances...')
  print()

  # Build target list.
  if scan_type == 'public_ip':
    target_list = EC2.InstancePublicIPList()
  elif scan_type == 'private_ip':
    target_list = EC2.InstancePrivateIPList()
  else:
    target_list = []

  # Respond based on contents of target list.
  if len(target_list) == 0:
    print(failure + ' No instances found using the specified parameters.')
  else:
    print(info + ' Discovered instances:')

    for t in target_list:
      print(t)
  
    print()

    for ip in target_list:
      Scanner.Scan(ip, scan_args, port_range)

    # Time info.
    final_time = time.time() - start_time

    print(success + ' Scan complete in %s seconds.' % (str(final_time)[0:4]))
    print()
else:
  print(failure + bold(' Unrecognized scan type: ') + scan_type)
  print()
