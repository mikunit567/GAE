#!/usr/bin/env python
import Queue
import threading
import time
import httplib
 
# Modified from: http://www.ibm.com/developerworks/aix/library/au-threadingpython/
# Fixed with try-except around urllib call

# https://8j3xxxjqml.execute-api.eu-central-1.amazonaws.com/prod

runs = 5
count = 1000
 
queue = Queue.Queue()
 
class ThreadUrl(threading.Thread):
  def __init__(self, queue):
    threading.Thread.__init__(self)
    self.queue = queue
 
  def run(self):
    while True:
      count = self.queue.get()
   
      try: 
        c = httplib.HTTPSConnection("8j3xxxjqml.execute-api.eu-central-1.amazonaws.com")
        json= '{ "key1": ' + str(count) +  '}'
        c.request("POST", "/prod", json)
        response = c.getresponse()
        data = response.read()

        print(data)
      except IOError as e: 
        print('Failed to open "%s".' % host)

      #signals to queue job is done
      self.queue.task_done()
 
# The class definition ends - the function below is outside
# the class body, so not initially indented

def parallel_run():
  #spawn a pool of threads, and pass them queue instance 
  for i in range(0, runs):
    t = ThreadUrl(queue)
    t.setDaemon(True)
    t.start()
     
  #populate queue with data   
  for x in range(0, runs):
    queue.put(count)
  
 #wait on the queue until everything has been processed     
  queue.join()

# Also not indented  
start = time.time()
parallel_run()
print("Elapsed Time: %s" % (time.time() - start))
