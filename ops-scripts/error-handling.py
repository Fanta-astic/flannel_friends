import subprocess
from jinja2 import Environment, FileSystemLoader

#get version
getVersion = "curl -s --data-urlencode 'query=rate(istio_requests_total{response_code=\"500\"}[5m])' 10.43.10.11:30708/api/v1/query | jq -r '.data.result[] | .metric | .source_version'" 
version = subprocess.getoutput(getVersion)

#get service name
getServiceName = "curl -s --data-urlencode 'query=rate(istio_requests_total{response_code=\"500\"}[5m])' 10.43.10.11:30708/api/v1/query | jq -r '.data.result[] | .metric | .source_app'"
servniceName = subprocess.getoutput(getServiceName)

#get json object and load data in var
getData = "curl -s --data-urlencode 'query=rate(istio_requests_total{response_code=\"500\"}[5m])' 10.43.10.11:30708/api/v1/query | jq -r '.data'"
data = subprocess.getoutput(getData)
test = 1
workingVersions = set([])
#if 'unknown' not in version.splitlines():
if test == 1:
	for i in version.splitlines():
		if i == 'unknown':
			print('something')	
		elif i != 'v1':
			workingVersions.add("v1")
		elif i != 'v2':
			workingVersions.add("v2")
		elif i != 'v3':
			workingVersions.add("v3")
	print(workingVersions)
	#jinja templating file
	file_loader = FileSystemLoader('templates')
	env = Environment(loader=file_loader)
	template = env.get_template('virtual-service-reviews-fix.yaml')

	if len(workingVersions) == 1:
		weight = 100
	elif len(workingVersions) == 2:
		weight = 50
	else:
		weight = 33
			
	output = template.render(workingVersions=workingVersions,weight=weight)
	print(output, file=open("fix.yaml", "w"))
        
	print('applying fix')
	fix = "kubectl apply -f /root/fix.yaml"
	subprocess.getoutput(fix)
else:
	remove = "kubectl delete -f /root/fix.yaml"
	subprocess.getoutput(remove)

