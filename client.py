from zeep import Client

# client = Client(wsdl='http://localhost:7789/?wsdl')
client = Client(wsdl='person.wsdl')

PersonKey = client.get_type('ns0:PersonKey')
pieter_key = PersonKey(username='pieter', email='piet@potac.com')

print(client.service.get_person(pieter_key))
print(client.service.get_ssn(pieter_key))

