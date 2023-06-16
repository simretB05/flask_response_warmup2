
from flask import Flask, request, make_response,jsonify
import dbhelper
import apiHelper
import dbcreds
from flask_cors import CORS
app=Flask(__name__)
CORS(app)

@app.get('/api/pokemon')
def get_all_pokemon():
        results = dbhelper.run_procedure('CAll get_all_pokemon()',[])
        if(type(results)==list):
            return make_response(jsonify(results), 200)
        else:
            return make_response(jsonify(results), 500) 

@app.post('/api/pokemon')
def post_new_pokemon():
     
        error=apiHelper.check_endpoint_info(request.json,["name","description","image_url"]) 
        if (error !=None):
         return make_response(jsonify(error), 400)
        results = dbhelper.run_procedure('CAll add_pokemon(?,?,?)',[request.json.get("name"),request.json.get("description"),request.json.get("image_url")])
        if(type(results)==list):
             return make_response(jsonify(results), 200)
        else:
            return make_response(jsonify(results), 500) 

if (dbcreds.production_mode == True):
    print("Running in Production Mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5001)
else: 
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing/Development Mode!")

app.run(debug=True)