# stock-app
- Sample here: https://dpaulstockapp.herokuapp.com/
- Linked to heroku account under dentongpaul@gmail.com
- From tutorial : https://www.newline.co/fullstack-flask
- Chart API: https://quickchart.io
- Financial API: https://financialmodelingprep.com
- To run testing and code coverage, run: 'pytest --cov=stock_app --cov-report term-missing' on the terminal.
- this app is able to log to files and email error logs
- DEBUG and INFO logs go to info_file.log
- WARNING, ERROR, and CRITICAL logs go to error_file.log and are emailed
- info_file.log and error_file.log rotate everyday

### TO-DO
- fix log testing
- logging to files works on heroku but emailing error logs does not.
- where does the logged info go to on heroku?
- Enable heroku authentication
- better charts with bokeh