#!/usr/bin/python3
import random
import re
import requests
import socket
import string
import time
import json
import sys

from analyser import Form

# Install the following libraries:
#  pip install gevent
#  pip install requests
#  pip install lxml

def argumentieren(commandLine):
    """
    gets the value of all arguments on command line 

    :param list: command line
    :return: url, min and max values defined by the command line
    """
    # Define verbose
    global verboseprint
    verboseprint = print if ("-verbose" in sys.argv or "-v" in sys.argv) else lambda *a, **k: None
    if "-v" in sys.argv: sys.argv.remove("-v")  
    if "-verbose" in sys.argv: sys.argv.remove("-verbose")
    
    # Define min and max execution time
    minValue = int(getArgumentValue(commandLine,"-min")) if "-min" in sys.argv else 1 #
    maxValue = int(getArgumentValue(commandLine,"-max")) if "-max" in sys.argv else 300 #
    
    # Verifies the call format and return the argument values
    if((len(commandLine) != 2) or (minValue > maxValue)):
        print("Wrong call")
        sys.exit(0)
    return str(sys.argv[1]), minValue, maxValue

def getArgumentValue(list, argument):
    """
    gets the value of an argument on a list 

    :param list: list of arguments
    :return: value of the specified argument
    """
    # Iterates to get argument and value
    valueIndex = sys.argv.index(argument) + 1
    argumentValue = sys.argv.pop(valueIndex) # argument value

    # Remove the argument used 
    sys.argv.remove(argument)

    # Return the value
    return argumentValue

class WasteFlooding():
    def __init__(self, url, minTime, maxTime):        
        self.url = url
        self.r = self.bait(self.url)
        if self.r==False:
            print("Incorrect url")
            self.empty = True
            return
        else:
            self.empty = False
        self.pipes = []
        self.forms = []
        self.scavenger(self.r.text,self.url)
        self.printAttackStructure() # --verbose
        self.countTime = 0
        self.minTime = minTime
        self.maxTime = maxTime

    def randomString(self, stringLength=6):
        """
        generates a random string 

        :param stringLength: Size of the string
        :return: Random String
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    def bait(self, url):
        """
        tests the first connection 

        :param url: destination url
        :return: Random String
        """
        url = url.replace("http://","")
        url = url.replace("https://","")
        
        hdr = {'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}
        
        # First request; gather data
        try:
            response = requests.get('https://'+url, stream=True, headers=hdr)
        except (requests.exceptions.SSLError, socket.error):
            response = requests.get('https://'+url, verify=False, stream=True, headers=hdr)

        if response.status_code == 200:
            return response
        else:
            return False

    def generateValue(self, minValue, maxValue):
        """
        generates the random value using validations, the only validation included now is CPF 

        :param minValue: minimum string size
        :param maxValue: maximum string size
        :return: random data
        """
        if(maxValue==11):
            cpf = [random.randint(0, 9) for x in range(9)]
            for _ in range(2):                                                          
                val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11                                                                              
                cpf.append(11 - val if val > 1 else 0)
            return '%s%s%s%s%s%s%s%s%s%s%s' % tuple(cpf)
        else:
            return random.randrange(10**(minValue-1),(10**(maxValue))-1)

    def flood(self):
        """
        floods the phishing form 

        :return:
        """
        # Arrange flood pipes
        if not self.pipes:
            self.pipes = self.getPipes()
        usedPipes = []
        
        hdr = {'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1','Connection':'close'}

        # BETA: output file testing
        #outFileBase = open("output.txt", "a+")
        #outFile = []
        #for index,form in enumerate(self.forms):
        #    outFile.append(open("output"+str(index)+".txt", "a+"))

        print("Waste Flooding\n Random times "+str(self.minTime)+"-"+str(self.maxTime)+" seconds")
        for index,form in enumerate(self.forms):
            # Set pipes
            pipe80 = self.pipes[0][random.randrange(0,len(self.pipes[0]))]['ip'] + ':80'
            pipe443 = self.pipes[1][random.randrange(0,len(self.pipes[1]))]['ip'] + ':443'
            plumbing = dict([('http',pipe80), ('https',pipe443)])

            # Generate the clutter
            clutter = dict.fromkeys(form.params.keys(),[])
            for param in clutter:
                clutter[param] = int(self.generateValue(int(form.params[param][0]),int(form.params[param][1])))
            
            # Remove any left schemes and sort a random one
            self.url = self.url.replace("https://","")
            self.url = self.url.replace("http://","")

            # Send the Waste
            try:
                rWaste = requests.post(form.actionUrl, data=clutter, proxies=plumbing, headers=hdr)
            except requests.exceptions.ProxyError:
                pipe80 = self.pipes[0][random.randrange(0,len(self.pipes))]['ip'] + ':80'
                pipe443 = self.pipes[1][random.randrange(0,len(self.pipes))]['ip'] + ':443'
                plumbing = dict([('http',pipe80), ('https',pipe443)])
                rWaste = requests.post(form.actionUrl, data=clutter, proxies=plumbing, headers=hdr)
            finally:
                rWaste.status_code == "400"
                     
            # Attack information
            print('+ Proxy: '+ pipe80 + ' and ' + pipe443 + ' for ' + form.action) # --verbose
            print('|  Waste: '+str(clutter)) # --verbose

            # Shows the result            
            if (rWaste.status_code == 200):
                print("|  OK") # --verbose                
                # output test
                #outFile[index].write(str(pipe80)+";"+str(timeWait)+";"+str(clutter)+"\n")
                #outFileBase.write(str(pipe80)+";"+str(timeWait)+";"+str(clutter)+"\n")
            else:
                print("|  ERROR") # --verbose
            
            # Define the min and max waiting time
            timeWait = self.randomPause()
            # outFile[index].write(str(pipe80)+";"+str(pipe80 in usedPipes)+";"+str(timeWait)+";"+str(clutter)+"\n")
            # outFileBase.write(str(pipe80)+";"+str(pipe80 in usedPipes)+";"+str(timeWait)+";"+str(clutter)+"\n")
            usedPipes.append(pipe80)
            self.countTime += timeWait
            if self.countTime > (3600*24):
                quit()
    
    def getPipes(self):
        """
        uses the proxy collection generated by getproxies 

        :return: a collection of proxies
        """
        f = open("GetProxies/proxies.json", "r")
        if f:
            content = f.read()
            proxies = json.loads(content)
            httpProxies = [d for d in proxies if d['port'] == 80]
            httpsProxies = [d for d in proxies if d['port'] == 443]
            return (httpProxies,httpsProxies)
            
    def printAttackStructure(self):
        """
        Prints the attack structure

        :return:
        """
        for form in self.forms:
            verboseprint("+ URL: "+form.file[-85:])
            verboseprint("|\tAction: "+form.action[-75:])
            verboseprint("|\tInputs: ")
            for param in form.params:
                verboseprint("|\t\t"+param+" - Range: "+str(form.params[param]))
            
    def randomPause(self):
        """
        Wait a random time on a defined range

        :param min: minimum waiting time (seconds)
        :param max: maximum waiting time (seconds)
        :return:
        """
        timeWait = random.randrange(self.minTime,self.maxTime)
        print("Waiting "+str(timeWait)+" seconds")
        time.sleep(timeWait)
        return timeWait

    def scavenger(self,text,url):
        """
        Searches the form on the HTML page source

        :param url: source url
        :return:
        """
        while text.find('<form') != -1:
            self.empty = False
            # Add the new Form found to the list
            self.forms.append(Form.Formalyse(text,url))
            if len(self.forms) > 1:
                for param in self.forms[-2].params:
                    if param in self.forms[-1].params:
                        self.forms[-1].params[param] = self.forms[-2].params[param]
            
            # Search for another form in the next url
            r = self.bait(self.forms[-1].actionUrl)
            if(r == False):
                return
            else:
                text = r.text
                url = self.forms[-1].actionUrl
        else:
            return      
        
        
if __name__ == '__main__':
    
    # Get all arguments
    url, minTime, maxTime = argumentieren(sys.argv)
    
    # Starts the waste object
    waste = WasteFlooding(url, minTime, maxTime)

    # Starts the flooding
    while not waste.empty:
        waste.flood()