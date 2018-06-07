import requests,dboperations,tempfile,re,os,hashlib,csv

### Parsers Section ###
def abuse():
    get = requests.get('https://urlhaus.abuse.ch/downloads/text/').content
    urls = re.findall('http\:\/\/.*',get.decode())
    try:
        with open('sources/abuse','w') as file:
            file.write([i.rstrip for i in urls])
    except FileNotFoundError:
        os.mkdir('sources')
    finally:
        with open('sources/abuse','w') as file:
            file.write([i.rstrip for i in urls])

    db = dboperations.DbOperator()
    db.connector()

    for i in urls:

        if db.isAdded(i):
            pass
        else:

            db.urlAdd(i)


def abuseCheck():
    get = requests.get('https://urlhaus.abuse.ch/downloads/text/').content
    urls = re.findall('http\:\/\/.*',get.decode())
    file,filepath = tempfile.mkstemp()

    with os.fdopen(file,'w') as tmp:
        tmp.writelines(urls)

    try:
        localfile = hashlib.md5(open('sources/abuse','rb').read()).hexdigest()
        tmpfile = hashlib.md5(open(filepath,'rb').read()).hexdigest()
    except FileNotFoundError:
        return False

    if localfile==tmpfile:
        os.remove(filepath)
        return True

    else:
        return False


### Others ###


def checkConnection(url):
    db = dboperations.DbOperator()
    db.connector()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'tr,en;q=0.8',
        'cache-control': 'max-age=0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
    try:
        req = requests.head(url,headers=headers,timeout=5)
        st = str(req.status_code)
        if st.startswith('2') or st.startswith('3'):
            db.urlChecked(url,st)
            return True
        else:
            req = requests.get(url,headers=headers,timeout=5)
            st = str(req.status_code)
            if st.startswith('2') or st.startswith('3'):
                db.urlChecked(url, st)
                return True
            else:
                return False
    except:
        return False

def reportCreator():
    file = open('reports.csv','w')
    column_header = ['URL','Status Code']
    w = csv.writer(file,delimiter=',',lineterminator='\r\n')

    w.writerow(column_header)

    db = dboperations.DbOperator()
    db.connector()
    allItem = db.getAll()
    w.writerows(allItem)

