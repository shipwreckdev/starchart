import nmap
from .utils import info, failure, success, bold, italics, reset


def Scan(ip, scan_args, port_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip, arguments=scan_args, ports=port_range)

    open_port_list = []

    for host in nm.all_hosts():
        print(info + ' Scanning host: %s' % (host))
        if nm[host].hostname() != '':
            print('     Hostname: %s' % nm[host].hostname())
        print('     State: %s' % nm[host].state())

        for proto in nm[host].all_protocols():
            print('     Port states:')
            print(italics('       %s') % proto)

            lport = sorted(nm[host][proto].keys())

            # Build a list of open ports based on discovery.
            for port in lport:
                port_state = nm[host][proto][port]['state']

                if port_state == 'open':
                    open_port_list.append(port)

            # Only scan the open ports.
            if len(open_port_list) != 0:
                for open_port in open_port_list:
                    print(italics('         service: ') +
                          nm[host][proto][open_port]['name'])
                    print(italics('         port: ') + str(open_port))
                    print(italics('         state: ') + port_state)
                    print()
            else:
                print(info + ' No open ports found on host.')
                print()
