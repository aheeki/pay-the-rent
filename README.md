# pay-the-rent
pay the rent in &lt; 80 lines of code. I use Advanced Python Scheduler and the Venmo API to collect monthly rent from my roomates.

## quickstart (ubuntu):

#### edit config.json:
- login to venmo and create a new app (https://venmo.com/account/settings/developer)
- add the app's ID to client_id in config.json
- in the same session, open the browser inspector's network tab, and navigate to `https://api.venmo.com/v1/oauth/authorize?client_id=[CLIENT ID HERE]&scope=make_payments%20access_profile` Copy the cookie field from the request headers and paste in the config
- choose start & end dates ("yyyy-mm-dd"), day of the month to charge, and hour (1-24) of day to charge
- add roommates' venmo id's, amount, note, and audience `public`, `friends`, or `private`


#### run it:
- make the script executable `chmod +x run.sh` and kick it off `source run.sh`
- enter venmo username and password

#### logging:
`cat payrent.log` to view logs

## pip packages
- Requests for http get and post
- Logging for logging
- BS4 for pulling token out of html form
- APScheduler for cron tasks and kicking off monthly venmo charges
