from urllib.request import Request, urlopen

req = Request('https://cmxlocationsandbox.cisco.com/api/config/v1/maps/info/DevNetCampus/DevNetBuilding/DevNetZone')
req.add_header('Authorization', 'Basic bGVhcm5pbmc6bGVhcm5pbmc=')
response = urlopen(req)
response_string = response.read().decode('utf-8')
print(response_string)
response.close()