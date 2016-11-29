import ConfigParser, logging, datetime, os

from flask import Flask, render_template, request

import mediacloud

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
log_file_path = os.path.join(basedir,'logs','mcserver.log')
logging.basicConfig(filename=log_file_path,level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("search-form.html")

@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    startday_string = request.form['startday']
    startday = int(startday_string)
    startmonth_string = request.form['startmonth']
    startmonth = int(startmonth_string)
    startyear_string = request.form['startyear']
    startyear = int(startyear_string)
    endday_string = request.form['endday']
    endday = int(endday_string)
    endmonth_string = request.form['endmonth']
    endmonth = int(endmonth_string)
    endyear_string = request.form['endyear']
    endyear = int(endyear_string)
    
    now = datetime.datetime.now()
    results = mc.sentenceCount(keywords, 
        solr_filter=[mc.publish_date_query( datetime.date( startyear, startmonth, startday), 
                                            datetime.date( endyear, endmonth, endday) ),
                     'media_sets_id:1' ], split=true)
    return render_template("search-results.html", 
        keywords=keywords, sentenceCount=results['split'] )


if __name__ == "__main__":
    app.debug = True
    app.run()