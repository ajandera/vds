import time
import redis
import mysql.connector
import os
import sys
import csv

from flask import Flask, request, url_for, redirect, render_template
from GPSPhoto import gpsphoto
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

app = Flask(__name__, template_folder='web')
cache = redis.Redis(host='redis', port=6379)
app.static_folder = 'web'

def insertVariablesIntoTable(path, latitude, longitude, prediction, pilon):
    try:
        connection = mysql.connector.connect(host='db',
                                             database='pilons',
                                             user='root',
                                             password='root')
        cursor = connection.cursor()
        mysql_insert_query = """INSERT INTO photos (path, latitude, longitude, result, code)
                                VALUES (%s, %s, %s, %s, %s) """

        recordTuple = (path, latitude, longitude, prediction, pilon)
        cursor.execute(mysql_insert_query, recordTuple)
        connection.commit()
        print("Record inserted successfully into photos table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# 'content' is base-64-encoded image data.
def get_prediction(content, project_id, model_id):
  prediction_client = automl_v1beta1.PredictionServiceClient()

  name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
  payload = {'image': {'image_bytes': content }}
  params = {}
  request = prediction_client.predict(name, payload, params)
  return request  # waits till request is returned

def get_pilon(latitude, longitude):
    great_circle_radius = 6372.795
    radius = 0.5
    with open('web/VN_PB_KE_okolie.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                 distance = acos(cos(deg2rad(latitude)) * cos(deg2rad(longitude)) * cos(deg2rad(row[0])) * cos(deg2rad(row[1]))
                                + cos(deg2rad(latitude)) * sin(deg2rad(longitude)) * cos(deg2rad(row[0])) * sin(deg2rad(row[1]))
                                + sin(deg2rad(latitude)) * sin(deg2rad(row[0]))
                                        ) * great_circle_radius

                if (distance < radius) {
                    return row[0]
                }

                line_count += 1


@app.route('/')
def index():
    return render_template("homepage.html")

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/reports')
def reports():
    return render_template("reports.html")

@app.route('/statistics')
def statistics():
    return render_template("statistics.html")

@app.route('/photos')
def photos():
    return render_template("AllPhotos.html")

@app.route('/unidentified-photos')
def not_defined_photos():
    return render_template("UnidentifiedPhotoLayout.html")

@app.route('/api/v1/pilon', methods=['GET'])
def pilons():
    count = get_hit_count()
    return  'Helo World! I have been seen {} times.\n'.format(count)

@app.route('/api/v1/add', methods=['POST'])
def add():
    path = '/web/photos'
    if request.files:
        image = request.file['image']
        name = os.path.join(path, image.filename)
        image.save(name)
        data = gpsphoto.getGPSData(name)
        prediction = get_prediction(content, '67264033942', 'IOD6491855299970859008')
        pilonCode = get_pilon()
        insertVariablesIntoTable(name, data['Latitude'], data['Longitude'], prediction, pilonCode)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)