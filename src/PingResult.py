import requests

class PingResult:
    def __init__(self, url, status):
        self.url = url
        self.status = status
        self.redirectsTo = ""
        self.redirectChain = {} # dict of PingResults with key of location url
        self.redirectError = []
        self.maxRedirects = 10
        
    def getStatusCode(self):
        return self.status

    def getUrl(self):
        return self.url

    def getRedirectChain(self):
        return self.redirectChain

    def hasRedirects(self):
        return len(self.redirectChain)>0
        
    def addErrorMessage(self, message):
        self.redirectError.append(message)

    def getErrorMessages(self):
        return self.redirectError    

    def setRedirectsTo(self, redirectLocation):
        self.redirectsTo = redirectLocation
    
    def followRedirectChain(self, location):
        self.redirectsTo = location

        initialRedirect = PingResult(self.url, self.status)
        initialRedirect.setRedirectsTo(location)
        self.redirectChain[location] = initialRedirect

        redirectCount=0
        redirectFinished = False
        while not redirectFinished:
            redirectCount+=1

            try:
                response = requests.head(location)
                pingStatus = PingResult(location, response.status_code)
                print("   * " + location + " - " + str(response.status_code))
                if response.status_code in [301,302, 307, 308]:
                    # it is a redirect response
                        if("location" in response.headers):
                            redirectTo = response.headers['location']
                            pingStatus.setRedirectsTo(redirectTo)
                            location = redirectTo
                            if(redirectTo in self.redirectChain.keys()):
                                self.addErrorMessage("Redirect Chain Loops Back to " + redirectTo)
                                # error loops back on itself
                                redirectFinished=True
                        if redirectCount>self.maxRedirects:
                            redirectFinished=True
                            self.addErrorMessage("Max Redirect Count Reached " + str(self.maxRedirects))
                else:
                    redirectFinished=True                
            except BaseException as err:
                pingStatus = PingResult(location, 502)
                self.addErrorMessage("Could not connect to " + location + " " + repr(err))
                redirectFinished = True

            self.redirectChain[location] = pingStatus
