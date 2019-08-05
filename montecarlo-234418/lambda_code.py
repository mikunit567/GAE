import json
import math
import Queue
import random
import re
import sys
import threading
import time


def lambda_handler(event, context):
    
    zero = 0
    listy = []
    lambdaa = str(event['lambda'])
    shots = int(event["dartshots"])
    decimal = int(event['decimal_accuracy'])
    reportingrate = int(event ['reporting_rate'])
    resources = int(event ['resources'])
    
    shotsapprox = int(math.ceil(shots/resources))
    shotsrate = int(math.ceil(shots/reportingrate))
    
    incircle_total = zero
    incircle_list = [zero] * reportingrate
    pi_results = [zero] * reportingrate
    
    if (lambdaa) == "lambda":
    
        
        
        for j in range (reportingrate):
            
            incircle_counter = zero
            
            for i in range (zero, shotsrate):
                
                random1 = random.uniform(-1.0,1.0)
                random2 = random.uniform (-1.0, 1.0)
                
                if ((random1*random1+random2*random2)<1):
                    
                    incircle_counter += 1
                incircle_list[j] = incircle_counter
                
        for j in range (zero,len(incircle_list)):
            pi_results[j] = str(round(float((4.0*incircle_list[j])/shotsrate), decimal))
             
        for i in pi_results:
            listy.append(i)
        listy[zero]   
        
    
        s3_bucket_name = 'montecarlomike'
        textfile = "PiValues.txt"
        persistent_storage = "/tmp/" + textfile
        s3 = boto3.resource('s3')
        try:
            obj=s3.Bucket(s3_bucket_name).download_file(persistent_storage, textfile)
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
            with open("/tmp/"+ textfile, 'a') as file:
                file.write(str(pi_results))
                file.close()
                s3.meta.client.upload_file(persistent_storage, s3_bucket_name, textfile) 
    else:
        print("Error ocurred ") 
        
    return pi_results    
        
    ''''elif (lambdaa) == "emr":  
        
        conn = boto3.client("emr")
        # chooses the first cluster which is Running or Waiting
        # possibly can also choose by name or already have the cluster id
        clusters = conn.list_clusters()
        # choose the correct cluster
        clusters = [c["Id"] for c in clusters["Clusters"] 
                    if c["Status"]["State"] in ["RUNNING", "WAITING"]]
        if not clusters:
            sys.stderr.write("No valid clusters\n")
            sys.stderr.exit()
        # take the first relevant cluster
        cluster_id = clusters[0]
        # code location on your emr master node
        CODE_DIR = "/home/hadoop/code/"
    
        # spark configuration example
        step_args = ["/usr/bin/spark-submit", "--spark-conf", "your-configuration",
                     CODE_DIR + "your_file.py", '--your-parameters', 'parameters']
    
        step = {"Name": "what_you_do-" + time.strftime("%Y%m%d-%H:%M"),
                'ActionOnFailure': 'CONTINUE',
                'HadoopJarStep': {
                    'Jar': 's3n://elasticmapreduce/libs/script-runner/script-runner.jar',
                    'Args': step_args
                }
            }
        action = conn.add_job_flow_steps(JobFlowId=cluster_id, Steps=[step])
    
    else:
        print("Error ocurred")'''
        
    
# code reference : https://gist.github.com/tomron/6ebc60cd3450478c7fc4 | Date : 19/05/2019 | Author: tomron
