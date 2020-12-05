import requests
import time 
def req():
    url = 'https://smart-card-1.herokuapp.com/'
    requests.get(url)
    print('done')

while True:
    req()
    time.sleep(1200)

