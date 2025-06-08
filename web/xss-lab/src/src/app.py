from flask import Flask, render_template, request
import urllib.parse
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re

app = Flask(__name__)

def filter_2(payload):
    regex = ".*(script|(</.*>)).*"
    if re.match(regex, payload):
        return "Nope"
    return payload

def filter_3(payload):
    regex = ".*(://|script|(</.*>)|(on\w+\s*=)).*"
    if re.match(regex, payload):
        return "Nope"
    return payload

def filter_4(payload):
    regex = "(?i:(.*(/|script|(</.*>)|document|cookie|eval|string|(\"|'|`).*(('.+')|(\".+\")|(`.+`)).*(\"|'|`)).*))|(on\w+\s*=)|\+|!"
    if re.match(regex, payload):
        return "Nope"
    return payload

@app.route('/', methods=['GET', 'POST'])
def xss1():
    if request.method == 'GET':
        payload = request.args.get('payload')
        if not payload:
            payload = ""
        return render_template("xss1.html", payload=payload)
    elif request.method == 'POST':
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox") # linux only
            chrome_options.add_argument("--headless=new") # for Chrome >= 109
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("http://localhost/")
            url = "http://localhost/?payload=" + urllib.parse.quote_plus(request.form["payload"])
            driver.add_cookie({"name": "xss2", "value": "/0d566d04bbc014c2d1d0902ad50a4122", "domain": "localhost"})
            driver.get(url)
            #print(driver.page_source.encode("utf-8"))
            driver.quit()
            return 'Page visited!'
        except:
            return 'An error occured.'


@app.route("/0d566d04bbc014c2d1d0902ad50a4122", methods=['GET', 'POST'])
def xss2():
    if request.method == 'GET':
        payload = request.args.get('payload')
        if not payload:
            payload = ""
        return render_template("xss2.html", payload=filter_2(payload))
    elif request.method == 'POST':
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox") # linux only
            chrome_options.add_argument("--headless=new") # for Chrome >= 109
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("http://localhost/")
            url = "http://localhost/0d566d04bbc014c2d1d0902ad50a4122?payload=" + urllib.parse.quote_plus(request.form["payload"])
            driver.add_cookie({"name": "xss3", "value": "/5d1aaeadf1b52b4f2ab7042f3319a267", "domain": "localhost"})
            driver.get(url)
            #print(driver.page_source.encode("utf-8"))
            driver.quit()
            return 'Page visited!'
        except:
            return 'An error occured.'
        
@app.route("/5d1aaeadf1b52b4f2ab7042f3319a267", methods=['GET', 'POST'])
def xss3():
    if request.method == 'GET':
        payload = request.args.get('payload')
        if not payload:
            payload = ""
        return render_template("xss3.html", payload=filter_3(payload))
    elif request.method == 'POST':
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox") # linux only
            chrome_options.add_argument("--headless=new") # for Chrome >= 109
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("http://localhost/")
            url = "http://localhost/5d1aaeadf1b52b4f2ab7042f3319a267?payload=" + urllib.parse.quote_plus(request.form["payload"])
            driver.add_cookie({"name": "xss4", "value": "/b355082fc794c4d1d2b6c02e04163090", "domain": "localhost"})
            driver.get(url)
            #print(driver.page_source.encode("utf-8"))
            driver.quit()
            return 'Page visited!'
        except:
            return 'An error occured.'
        
@app.route("/b355082fc794c4d1d2b6c02e04163090", methods=['GET', 'POST'])
def xss4():
    if request.method == 'GET':
        payload = request.args.get('payload')
        if not payload:
            payload = ""
        return render_template("xss4.html", payload=filter_4(payload))
    elif request.method == 'POST':
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox") # linux only
            chrome_options.add_argument("--headless=new") # for Chrome >= 109
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("http://localhost/")
            url = "http://localhost/b355082fc794c4d1d2b6c02e04163090?payload=" + urllib.parse.quote_plus(request.form["payload"])
            driver.add_cookie({"name": "flag", "value": "N0PS{n0w_Y0u_4r3_x55_Pr0}", "domain": "localhost"})
            driver.get(url)
            #print(driver.page_source.encode("utf-8"))
            driver.quit()
            return 'Page visited!'
        except:
            return 'An error occured.'

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)