import os
from flask import Flask, render_template, session, request, redirect, flash, url_for



app = Flask('app')
app.secret_key = 'secret'

@app.route('/', methods=['GET', 'POST'])
def disprecords():
    ##records - record['name'] record['date']
    ##date 
    ##signins - signin['time']}} - {{signin['name']
    files = os.listdir()
    files = [{'name':f,'date':f[16:-4]} for f in files if(f.startswith('attendance_data_') and f.endswith('.csv'))]
    if request.method == 'POST':
        
        file = request.form['file']
        selected = {'name':file,'date':file[16:-4]}
        date = request.form['file'][16:-4]
        import csv
        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            ##for row in reader:
                ##print(row['first_name'], row['last_name'])
            signins = [{'time':row[list(row)[1]],'name':row[list(row)[0]]} for row in reader]
        return render_template('index.html',records=files,selected =selected, date = date,signins=signins)
    else:
        return render_template('index.html',records=files,selected = None, date = None, signins=None)



app.run(host='0.0.0.0', port=8080)