import argparse
import lib.scan as Scanner
from lib.utils import info, failure, success, bold, italics, reset
import os
from termcolor import colored
import time

version = "v1.0"

# Provide some timing details.
start_time = time.time()

# Parse for arguments.
parser = argparse.ArgumentParser(
    description='Run nmap scans against dynamic lists of scannable objects in cloud native environments.')
parser.add_argument('-t', '--type', dest='scan_type', type=str,
                    help='This is to establish what type of scanning to use. Options are: public_ip, private_ip, kube, manual', default='manual')
parser.add_argument('-i', '--ip', dest='manual_ips', type=str,
                    help='If running a scan type of manual, provide the target address(es) here.')
parser.add_argument('-a', '--all', dest='all_ports',
                    help='If using a scan type of ip, scan ports 1-65535.', action='store_true')
parser.add_argument('-p', '--ports', dest='port_range', type=str,
                    help='If not scanning all ports, set the port range to scan - ex: 22-26, 53 - This will default to 22 if no optional input is provided.', default='22')
parser.add_argument('-c', '--cloud-provider', dest='provider', type=str,
                    help='The cloud provider where the tool is being used, if using provider-specific options. This will default to manual for a manual scan unless otherwise specified. Options are: aws', default='manual')
parser.add_argument('-o', '--os-discovery', dest='os_discovery',
                    help='Enable OS detection for hosts IP based nmap scans.', action='store_true')
args = parser.parse_args()

# Establish variables.
all_ports = args.all_ports
os_discovery = args.os_discovery
manual_ips = args.manual_ips
port_range = args.port_range
provider = args.provider
scan_type = args.scan_type
# -sS TCP_SYN scan, -vv verbose, -Pn skip discovery, -T5 timing template (higher is faster)
scan_args = '-sS -vv -Pn -T5 {os_detect}'.format(
    os_detect='-O' if os_discovery == True else '')

# Present some basic information.
print(colored('starchart', 'cyan'))
print(version)
print()

if provider:
    print(success + bold(' Provider: ') + provider)
print(success + bold(' Type: ') + scan_type)
if port_range:
    print(success + bold(' Port Range: ') + str(port_range))
if scan_type == 'manual' and manual_ips != None:
    print(success + bold(' Target IP Addresses: ') + str(manual_ips))
print()

# Build list of targets and scan.
if provider == 'aws':
    import lib.ec2 as EC2

    if (scan_type == 'public_ip' or scan_type == 'private_ip'):
        print(info + ' Looking for instances...')
        print()

        # Build target list.
        if scan_type == 'public_ip':
            instance_list = EC2.InstanceIDList()
            target_list = EC2.InstancePublicIPList()

            subjects = dict(zip(instance_list, target_list))
        elif scan_type == 'private_ip':
            instance_list = EC2.InstanceIDList()
            target_list = EC2.InstancePrivateIPList()

            subjects = dict(zip(instance_list, target_list))
        else:
            instance_list = []
            target_list = []

            subjects = {}

        # Respond based on contents of target list.
        if len(target_list) == 0:
            print(failure + ' No instances found using the specified parameters.')
        else:
            print(info + ' Discovered instances:')

            for inst in subjects:
                print(inst, '->', subjects[inst])

            print()

            for inst in subjects:
                Scanner.Scan(subjects[inst], scan_args, port_range)
                print()

            # Time info.
            final_time = time.time() - start_time

            print(success + ' Scan complete in %s seconds.' %
                  (str(final_time)[0:4]))
            print()
    else:
        print(failure + bold(' Must use scan type of public_ip or private_ip with provider aws.'))
elif scan_type == 'manual':
    if manual_ips != None:
        target_list = []

        for ip in manual_ips.split(','):
            Scanner.Scan(ip, scan_args, port_range)

        # Time info.
        final_time = time.time() - start_time

        print()
        print(success + ' Scan complete in %s seconds.' %
              (str(final_time)[0:4]))
        print()
    else:
        print(failure + bold(' No IP addresses provided for manual scan type.'))
else:
    print(failure + bold(' Unrecognized scan type: ') + scan_type)
    print()
