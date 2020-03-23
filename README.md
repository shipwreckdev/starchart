# shipwreck / starchart

![starchart](https://github.com/shipwreckdev/starchart/blob/master/assets/starchart.png)

Starchart is a tool that allows you to identify and scan resources in cloud infrastructures. 

Under the hood, `boto3` is used to identify qualifying instances in AWS. `python-nmap` is used to facilitate scans.

The tool can also be used to run `nmap` scans locally if not running against a cloud-native environment.

## Development Notes

In its current iteration, the tool depends on [AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) to provide connectivity and visibility into your account(s).

The following variables should be configured before running the tool for use with `aws`:

* `ACCESS_KEY`
* `AWS_REGION`
* `SECRET_KEY`

The long term concept behind the tool is to be able to place it into an AWS account and have it run via Fargate, ECS, EKS, or whatever other chosen method works best. This avoids the requirement for AWS credentials on a local machine.

## Requirements

* `python3`

## Usage

### Running Locally

Run `pip3 install -r requirements.txt` to install dependencies.

The tool can be invoked via the command line and has various arguments that can be passed in:

```bash
usage: main.py [-h] [-t SCAN_TYPE] [-i MANUAL_IPS] [-a] [-p PORT_RANGE]
               [-c PROVIDER] [-o]

Run nmap scans against dynamic lists of scannable objects in cloud native
environments.

optional arguments:
  -h, --help            show this help message and exit
  -t SCAN_TYPE, --type SCAN_TYPE
                        This is to establish what type of scanning to use.
                        Options are: public_ip, private_ip, kube, manual
  -i MANUAL_IPS, --ip MANUAL_IPS
                        If running a scan type of manual, provide the target
                        address(es) here.
  -a, --all             If using a scan type of ip, scan ports 1-65535.
  -p PORT_RANGE, --ports PORT_RANGE
                        If not scanning all ports, set the port range to scan
                        - ex: 22-26, 53 - This will default to 22 if no
                        optional input is provided.
  -c PROVIDER, --cloud-provider PROVIDER
                        The cloud provider where the tool is being used, if
                        using provider-specific options. This will default to
                        manual for a manual scan unless otherwise specified.
                        Options are: aws
  -o, --os-discovery    Enable OS detection for hosts IP based nmap scans.
```

### Sample CLI Usage

`python3 main.py -t -p 53 -c aws` - finds instance public IP addresses and scans those on port 53

`python3 main.py -t private_ip -p 22-100 -c aws` - finds instance private IP addresses and scans those on ports 22 through 100

`python3 main.py -t private_ip -a -c aws` - finds instance private IP addresses and scans all ports 1-65535.

`python3 main.py -t manual -i 1.2.3.4,5.6.7.8` - run a local, manual scan against the IP addresses provided as a comma separated list.

### Running In Docker

The same concept can be used when running the tool using Docker:

`docker container run -i 192.168.1.1`

If running against `aws`:

`docker container run -e AWS_REGION -e ACCESS_KEY -e SECRET_KEY shipwreckdev/starchart -c aws -t public_ip`

This will pass host variables (which were mentioned above) into the Docker container.

## Update Paths

More providers will be added in the future. There are also plans to identify other types of resources.

A Docker image will also be created for portability.

Better options for authenticating against AWS (STS) will be added.
