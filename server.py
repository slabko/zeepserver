import faker
import soap_utils
from zeep import Client
from zeep.wsdl.utils import etree_to_string
from flask import Flask, request
from flask import make_response, Response

fake = faker.Faker()

APPLICATION = '{spyne.examples.hello.http}Application'
client = Client(wsdl='person.wsdl')
binding = client.wsdl.bindings[APPLICATION]

app = Flask('person_api')

# Types from WSDL
Person = client.get_type('ns0:Person')
SSN = client.get_type('ns0:SSN')


# Actual implementation of endpoints (return random values)
def get_person(key):
    return Person(
        username=key.username,
        email=key.email,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        address=fake.address()
    )


def get_ssn(key):
    return SSN(
        username=key.username,
        ssn=fake.ssn()
    )


# Actual SOAP endpoint
@app.route('/', methods=['POST', 'GET'])
def soap_endpoint():

    if request.method == 'GET':
        with open('person.wsdl', 'r') as fp:
            return Response(fp.read(), mimetype='text/xml')

    document = soap_utils.parse_xml(request.data)
    operation_name = soap_utils.operation_name(document)
    operation = binding.get(operation_name)

    request_object = operation.input.deserialize(document)

    if operation_name == 'get_person':
        response_object = get_person(request_object)

    elif operation_name == 'get_ssn':
        response_object = get_ssn(request_object)

    else:
        raise NotImplementedError()

    to_return = operation.output.serialize(response_object)
    return Response(etree_to_string(to_return.content), mimetype='text/xml')


@app.errorhandler(Exception)
def handle_server_error(error):
    # Needs to return proper errors
    response = make_response('<error>SOAP Error</error>')
    response.mimetype = 'text/xml'
    response.status_code = 500
    return response


if __name__ == '__main__':
    app.run()

