import boto
import boto.ec2
import time
import itertools
import sys
import os

def start_vm_openstack(num_vms):
	""" Create a VM instance on OpenStack using the ec2 boto interface commands
	Args: 
		Set the EC2_ACCESS_KEY and EC2_SECRET_KEY environment variables
		num_vms:  Number of vms to spawn
	Returns:
				
	"""
	access_key = os.getenv("EC2_ACCESS_KEY")
	secret_key = os.getenv("EC2_SECRET_KEY")
	ec2=None

	## get the aws regions.  Return type <class 'boto.regioninfo.RegionInfo'>
	regions = boto.ec2.regions(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
	#RegionInfo:eu-west-1
        #RegionInfo:sa-east-1
        #RegionInfo:us-east-1
        #RegionInfo:ap-northeast-1
        #RegionInfo:us-west-2
        #RegionInfo:us-west-1
        #RegionInfo:ap-southeast-1
	ec2_region = "us-east-1"
	ec2_region_endpoint = "ec2.us-east-1.amazonaws.com"
	try:
		region = boto.regioninfo.RegionInfo(name="east", endpoint=ec2_region_endpoint)	
		ec2 = boto.connect_ec2(aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                is_secure=False,
                region=region,
                port=8773,
                path="/services/Cloud")

	except:
		print 'Error connection to openstack' 
		return 

	## the machine image 
        ami = "ami-baba68d3"
	
	## start a bunch of vms
	for count in range(0,6):
		reservations=ec2.run_instances(ami,instance_type='m1.tiny',max_count=1) 
		print "Launching vm ",count," of 256" 
	## create a chain (ie. Make in iterator that returns elements fromt the first
	## iterable untils it is exhaused, then proceeds to the next iterable
	chain = itertools.chain.from_iterable
	existing_instances = list(chain([res.instances for res in ec2.get_all_instances()]))
	status = [e.update() for e in existing_instances]
	
	## wait until all the instances have transitioned from 'pending' to 'running' status 
	while 'pending' in status:
		existing_instances = list(chain([res.instances for res in ec2.get_all_instances()]))
		status = [e.update() for e in existing_instances]
		status_dict = dict(zip(existing_instances,status))	
		print [(i,status_dict[i]) for i in status_dict.keys() if status_dict[i] != 'terminated']	
		print 'Still pending'
		time.sleep(3)
	
	return status_dict; 	


def stop_vm_openstack(status_dict):
	""" 
	Stop vm-s given a dict containing the instance ids
	Args: 
		status_dict:  Dictionary containing  information about the instances	
	Returns:
		None:
	"""
	## terminate the instances 
	instances_to_terminate=[]
	for i in status_dict.keys():
		if status_dict[i] == 'running':
			instances_to_terminate.append(i.id)
	print instances_to_terminate
	try:
		ec2.terminate_instances(instances_to_terminate)
	except:
		print 'Error terminating VMs'
		return -1
	return 0
