import requests, os, logging, datetime, json
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

logging.basicConfig(filename='payrent.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

# load config
with open('config.json') as json_data_file:
    config = json.load(json_data_file)

@sched.scheduled_job('cron', day=int(config['charge_day']), hour=int(config['charge_hour']), start_date=str(config['start_date']), end_date=str(config['end_date']))
def get_access_token():
    url='https://api.venmo.com/v1/oauth/authorize?client_id='+str(config['client_id'])+'&scope=make_payments%20access_profile'
    r = requests.get(url)
    s = BeautifulSoup(r.text, 'html.parser')

    csrftoken2 = ''
    auth_request = ''
    for link in s.find_all('input'):
        if link.get('name')=='csrftoken2':
            csrftoken2 = str(link.get('value'))
        if link.get('name')=='auth_request':
            auth_request = str(link.get('value'))

    headers = {
        "Host":"api.venmo.com",
        "Connection":"keep-alive",
        "Content-Length":"195",
        "Cache-Control":"max-age=0",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Origin":"https://api.venmo.com",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
        "Content-Type":"application/x-www-form-urlencoded",
        "Referer":"https://api.venmo.com/v1/oauth/authorize?client_id="+str(config['client_id'])+"&scope=make_payments",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"en-US,en;q=0.8",
        "Cookie":str(config['cookie'])   
    }
    data = {
        "csrftoken2":csrftoken2,
        "auth_request":auth_request,
        "web_redirect_url":"http://localhost:5000", # an arbitrary url
        "username":os.environ.get('VENMO_USER'),
        "password":os.environ.get('VENMO_PASS'),
        "grant":"1"
    }

    r2 = requests.post(url, data=data, headers=headers, allow_redirects=False)
    access_token = r2.headers['location'].split('=')[1]
    
    collect_rent(access_token)


def collect_rent(access_token):
    month = datetime.datetime.now().month + 1 # charge for next month
    month_name = datetime.date(2000, month, 1).strftime("%b").lower() # arbitrary year and day (neither is shown) 
    roommates = config['roommates']
    for roommate in roommates:
        payment = {
            'access_token':access_token,
            'username':str(roommate['venmo_username']),
            'note':month_name + str(config['note']),
            'amount':str(roommate['amount']),
            'audience':str(config['audience'])}
        r = requests.post('https://api.venmo.com/v1/payments', data=payment)
        logging.info(r)
        logging.info(payment)


if __name__ == '__main__':
    # run the cron task
    sched.start()