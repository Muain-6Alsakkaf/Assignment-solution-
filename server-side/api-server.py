from flask import Flask,request,jsonify



app = Flask(__name__)

data_global = dict()

@app.route('/data',methods=['GET','POST'])
def data():
    global data_global
    if request.method=='POST':
        data = request.get_json()
        for key in  data.keys():
            print(key,":",data[key])
        data_global =data    
        return jsonify({"status":201,"message":"Successfully recieved Data"}),201

    elif request.method=='GET':
        return jsonify({"status":200,"data":str(data_global)}),200

    

if __name__=="__main__":
    app.run("0.0.0.0",5000,debug=True)


