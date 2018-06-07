
from dboperations import DbOperator
import sys,utils,progressbar




green = "\033[32m"
red = "\033[31m"
reset = "\033[0m"


print("""\r 
              888     888 8888888b.  888      
              888     888 888   Y88b 888      
              888     888 888    888 888      
88888b.d88b.  888     888 888   d88P 888      
888 "888 "88b 888     888 8888888P"  888      
888  888  888 888     888 888 T88b   888      
888  888  888 Y88b. .d88P 888  T88b  888      
888  888  888  "Y88888P"  888   T88b 88888888
""")
print("""Check your browsing health on the {}malformed/malware{} sites.""".format(red,reset))

db = DbOperator()

sys.stdout.write("{}[\]{} Database checking for first launch.".format(red, reset))
sys.stdout.flush()


if db.dbCheck() == False:

    db.connector()
    db.tableCreator()
    sys.stdout.write("\r{}[+]{} Database created for first launch.\n".format(green,reset))
    sys.stdout.flush()

sys.stdout.write("\r{}[+]{} Database checking completed.".format(green, reset))
sys.stdout.flush()
sys.stdout.write("{}[?]{} Will check abuse source file.".format(red,reset))
sys.stdout.flush()

if utils.abuseCheck():
    sys.stdout.write('\r{}[*]{} Sources file have same content.'.format(green,reset))
    sys.stdout.flush()
else:
    sys.stdout.write("\r{}[-]{} Sources file doesn't equal the new temp file.Please wait for updates".format(red,reset))
    sys.stdout.flush()

    utils.abuse()

    sys.stdout.write("\r{}[+]{} Updates completed.\n".format(green, reset))
    sys.stdout.flush()

sys.stdout.write("Starting the connection test\n")
count = db.dbCount()
print("\t"*1+"Found URL: {}".format(count))
bar = progressbar.ProgressBar(max_value=count)

for i in range(1,count):
    url = db.returnItem(i)
    if url== False:
        pass
    else:
        utils.checkConnection(url)
    bar.update(i)

sys.stdout.write('{}[-]{} Test completed and report will generate as soon'.format(red,reset))
sys.stdout.flush()

utils.reportCreator()

sys.stdout.write('\r{}[+]{} Reports generated in project folder'.format(green,reset))
sys.stdout.flush

