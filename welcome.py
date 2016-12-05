# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify
import json
import ibm_db
import logging

app = Flask(__name__)

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

# Parse VCAP_SERVICES Variable 
vcap_services = json.loads(os.environ['VCAP_SERVICES'])
service = vcap_services['dashDB'][0]
credentials = service["credentials"]
url = 'DATABASE=%s;uid=%s;pwd=%s;hostname=%s;port=%s;' % ( credentials["db"],credentials["username"],credentials["password"],credentials["host"],credentials["port"])
print "URl = %s" %url

connection = ibm_db.connect(url, '', '')
statement = ibm_db.prepare(connection, 'SELECT * from DASH111327.DOGS FETCH FIRST 10 ROWS ONLY')
print 'SUCCESS1!!'

ibm_db.execute(statement)
#print 'SUCCESS2!!'
out = "<html><table border=\"1\"><tr><td>Table Name</td><td>Table Schema</td>" 
#print 'SUCCESS3!!'

data = ibm_db.fetch_tuple(statement)
while (data):
    out = out + "<tr><td>"+data[1]+"</td><td>"+data[3]+"</td></tr>"
    data = ibm_db.fetch_tuple(statement)
#    print "data:[0]"'+ data[0]
#    print "data:%s" %data[0]
    

ibm_db.free_stmt(statement)
ibm_db.close(connection)
out = out + "</table></html>"
return out

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
