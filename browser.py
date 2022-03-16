from operator import sub
from re import search
from sunau import AUDIO_UNKNOWN_SIZE
from flask import Flask, request_started, request, render_template
import requests
from bs4 import BeautifulSoup
import urllib
app = Flask(__name__)

naughtysetting = True
allowmalware = False

@app.route('/')
def my_form():
    return render_template('template.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    print(text)

    return render_template('resultpage.html')

proxies = {
  "http": "http://127.0.0.1:8000",
  "https": "http://127.0.0.1:8000"
}
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 SecureSurf/28.0)'
    }
@app.route('/<path:path>')
def home(path):
    adultblocked = 0
    malwareblocked = 0
    Root_injector = open("inject.txt", "r") #ROOT INJECTOR
    overwrite = open("injectoverwrite.txt", "r") #TITLE OVERWRITER
    rootinjectedtext = Root_injector.read() #READ ROOT INJECTED TEXT
    overwritedtext = overwrite.read() #READ OVERWRITE INJECTED TEXT
    Root_injector.close() 
    overwrite.close()
    chosenweb = requests.get(path, headers=headers)#,*proxies=proxies,verify=False)
    print(path)
    malwebs = open("malwarewebsites.txt", "r")
    malwords = malwebs.readlines()
    
    for malword in malwords:
        malword = malword.replace("\n", "")
        if malword in chosenweb.text:
            print('String contains malword from list.')
            print(malword)
            if allowmalware == True:
                break
            else:
                return render_template('malwareblockpage.html')
    adultwebs = open("adultwebsites.txt", "r")
    naughtywords = adultwebs.readlines()
    for substring in naughtywords:
        substring = substring.replace("\n", "")
        if substring in chosenweb.text:
            print('String contains substring from list.')
            print(substring)
            if naughtysetting == False:
                adultblocked = 1
            else:
                adultblocked = 0
        else:
            adultblocked = 0
        if adultblocked == 1:
            return """<script>alert("This site contains pornographic material. To view it you must turn naughty setting on")</script>"""
        else:
            return """
            <script>console.log(""" + """USING SECURESURF 1.0""" + """)</script> 
            """ + rootinjectedtext + chosenweb.text.replace('href="/','href="http://localhost:8080/' + path + "/").replace('"/sp/', path + "/sp/").replace('href="/video','href="http://localhost:8080/' + path + "/video") + overwritedtext

  
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=8080)
