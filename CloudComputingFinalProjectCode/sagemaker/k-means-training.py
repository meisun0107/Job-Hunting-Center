import sagemaker
from sagemaker import get_execution_role
from sagemaker import KMeans
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy import genfromtxt
from sagemaker.predictor import json_serializer, json_deserializer
role = get_execution_role()
# sagemaker_session=sagemaker_session()
# Set the name of your S3 bucket and the name of your CSV file
bucket_name = 'ui-of-jrc-cloud-computing'
csv_filename = 'text.csv'

# Set the path to the CSV file in your S3 bucket
csv_path = f's3://{bucket_name}/{csv_filename}'
my_data = genfromtxt("http://ui-of-jrc-cloud-computing.s3-website-us-east-1.amazonaws.com/training_data.csv", delimiter=',')
train_data = my_data.astype('float32')
print(len(train_data[0]))
num_clusters = 5
kmeans = KMeans(role=role,
               instance_count=1,
               instance_type='ml.m4.xlarge',
               output_path='s3://'+bucket_name+'/counties/',
#                sagemaker_session=sagemaker_session,
               use_spot_instances=True,
               max_run=300,
               max_wait=600,
               k=num_clusters)
kmeans.fit(kmeans.record_set(train_data))
# pf.iloc[:, 1:]
kmeans_predictor = kmeans.deploy(initial_instance_count=1,
                                  instance_type='ml.m4.xlarge')
print(kmeans_predictor.content_type)
print(kmeans_predictor.accept)
# kmeans_predictor = response['predictions']
# print(kmeans_predictor)
result_km = kmeans_predictor.predict(train_data)
cluster_labels = [r.label['closest_cluster'].float32_tensor.values[0] for r in result_km]
# pd.DataFrame(cluster_labels)[0].value_counts()
fs = [int(x) for x in cluster_labels]
print(fs)