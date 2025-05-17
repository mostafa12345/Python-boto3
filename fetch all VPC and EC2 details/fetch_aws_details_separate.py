import boto3
import json
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = "C:/Users/mostafa/Documents/"

ec_client = boto3.client('ec2', region_name="us-east-1")


all_available_vpcs = ec_client.describe_vpcs()
vpcs = all_available_vpcs["Vpcs"]

 
vpc_data = []
for vpc in vpcs:
    vpc_id = vpc["VpcId"]
    cidr_block = vpc["CidrBlock"]
    state = vpc["State"]
    
    vpc_data.append({
        "VpcId": vpc_id,
        "CidrBlock": cidr_block,
        "State": state
    })

with open(f"{output_path}vpc_details_{timestamp}.json", "w") as vpc_file:
    json.dump(vpc_data, vpc_file, indent=2)


all_instances = ec_client.describe_instances()


ec2_data = []
for reservation in all_instances["Reservations"]:
    for instance in reservation["Instances"]:
        instance_id = instance["InstanceId"]
        instance_type = instance["InstanceType"]
        state = instance["State"]["Name"]
        private_ip = instance.get("PrivateIpAddress", "N/A")
        public_ip = instance.get("PublicIpAddress", "N/A")
        launch_time = str(instance["LaunchTime"])  # Convert datetime to string
        ami_id = instance["ImageId"]
        vpc_id = instance["VpcId"]

        ec2_data.append({
            "InstanceId": instance_id,
            "InstanceType": instance_type,
            "State": state,
            "PrivateIpAddress": private_ip,
            "PublicIpAddress": public_ip,
            "LaunchTime": launch_time,
            "AMI": ami_id,
            "VpcId": vpc_id
        })


with open(f"{output_path}ec2_details_{timestamp}.json", "w") as ec2_file:
    json.dump(ec2_data, ec2_file, indent=2)
