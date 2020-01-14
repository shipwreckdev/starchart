# shipwreck / starchart
This tool allows you to identify and scan resources in cloud infrastructures.

In its current iteration, the tool depends on [AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) to provide connectivity and visibility into your account(s).

Once `awscli` is installed and `aws configure` has been run, the tool can be used.

The long term concept behind the tool is to be able to place it into an AWS account and have it run via Fargate, ECS, EKS, or whatever other chosen method works best. This avoids the requirement for AWS credentials on a local machine.

## Requirements
The tool requires Python 3.

Run `pip3 install -r requirements.txt` to install dependencies.

## Usage
The tool can be invoked via the command line and has various options that can be passed in:

```bash
usage: main.py [-h] [-t SCAN_TYPE] [-a] [-p PORT_RANGE] [-c PROVIDER] [-o]

Run nmap scans against dynamic lists of scannable objects in cloud native
environments.

optional arguments:
  -h, --help            show this help message and exit
  -t SCAN_TYPE, --type SCAN_TYPE
                        This is to establish what type of scanning to use.
                        Options are: public_ip (default), private_ip
  -a, --all             If using a scan type of ip, scan ports 1-65535.
  -p PORT_RANGE, --ports PORT_RANGE
                        If not scanning all ports, set the port range to scan
                        - ex: 22-26, 53 - This will default to 22 if no
                        optional input is provided.
  -c PROVIDER, --cloud-provider PROVIDER
                        The cloud provider where the tool is being used.
                        Options are: aws (default)
  -o, --os-discovery    Enable OS detection for hosts IP based nmap scans.
```

### Sample CLI Usage
`python3 main.py -t -p 53 -c aws` - finds instance public IP addresses and scans those on port 53

`python3 main.py -t private_ip -p 22-100 -c aws` - finds instance private IP addresses and scans those on ports 22 through 100

`python3 main.py -t private_ip -a -c aws` - finds instance private IP addresses and scans all ports 1-65535.

## Update Paths
More providers will be added in the future. There are also plans to identify other types of resources.
