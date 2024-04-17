import boto3
import csv
import requests
import shutil

def list_bucket():
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()

    for bucket in response['Buckets']:
        print(f"{bucket['Name']}")

def upload_file(file_name, bucket, store_as=None):
    if store_as is None:
        store_as = file_name

    s3_client = boto3.client('s3')
    s3_client.upload_file(file_name, bucket, store_as)

image_data = []

with open('watermark.csv', mode='r') as csvfile:
  csv_reader = csv.reader(csvfile)
  next(csv_reader)
  for row in csv_reader:
      id = row[0]
      text = row[1]

      start_index = text.find("https://")
      link = text[start_index:]
      
      datum = {}
      datum['filename'] = id
      datum['link'] = link

      image_data.append(datum)

for image in image_data:
    link = image['link']
    filename = "images/" + image['filename'] + ".jpg"

    response = requests.get(link, stream=True)

    if response.status_code == 200:
        with open(filename, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        print(f'Image successfully downloaded: {filename}')

        upload_file(filename, "watermark-ml-us-east-1", f"output/{filename}")
    else:
        print(f'Image could not be retrieved')