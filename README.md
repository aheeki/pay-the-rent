# pay-the-rent
cron and venmo api to collect rent from roomates

## quickstart (ubuntu):

#### edit config.json:
- login to venmo and create a new app (https://venmo.com/account/settings/developer)
- add the app's ID to client_id in config.json
- in the same session, navigate to `https://api.venmo.com/v1/oauth/authorize?client_id=[CLIENT ID HERE]&scope=make_payments%20access_profile` and open the browser inspector's network tab, then copy the cookie field from the request headers and paste in the config.json
- choose start & end dates ("yyyy-mm-dd"), day of the month to charge, and hour (1-24) of day to charge
- add roommates' venmo id's, amount, note, and audience `public`, `friends`, or `private`


#### run it:
- make the script executable `chmod +x run.sh` and kick it off `source run.sh`
- enter venmo username and password

#### logging:
`cat payrent.log` to view logs

## pip packages
- [**Requests**](http://docs.python-requests.org/en/latest/) for http get and post
- [**Logging**](https://docs.python.org/2/library/logging.html) for logging
- [**BS4**](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) for pulling token out of html form
- [**APScheduler**](https://apscheduler.readthedocs.org/en/latest/) for cron tasks and kicking off monthly venmo charges

## License
MIT
