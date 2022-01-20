import requests


class PingResult:
    def __init__(self, url, status):
        self.url = url
        self.status = status
        self.redirectsTo = ""
        self.redirectChain = [] # array of PingResults
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

    def getRedirectsTo(self):
        return self.redirectsTo

    def getFinalRedirectLocation(self):
        if len(self.redirectChain) == 0:
            return ""

        return self.redirectChain[len(self.redirectChain)-1].getUrl()
    
    def followRedirectChain(self, startLocation):
        location = startLocation
        self.redirectsTo = location

        initialRedirect = PingResult(self.url, self.status)
        initialRedirect.setRedirectsTo(location)
        self.redirectChain.append(initialRedirect)

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
                            if self.containsLocationAlready(self.redirectChain, redirectTo):
                                self.addErrorMessage("Redirect Chain Loops Back to " + redirectTo)
                                # error loops back on itself
                                redirectFinished=True
                        if redirectCount>self.maxRedirects:
                            redirectFinished=True
                            self.addErrorMessage("Max Redirect Count Reached " + str(self.maxRedirects))
                else:
                    location="-"
                    redirectFinished=True                
            except BaseException as err:
                pingStatus = PingResult(location, 502)
                self.addErrorMessage("Could not connect to " + location + " " + repr(err))
                redirectFinished = True

            self.redirectChain.append(pingStatus)

        #add pings to all redirectChain arrays in the chain to allow recursive processing of pingResult redirect chains
        for aPingResult in self.redirectChain:
            foundIt = False
            if aPingResult.getStatusCode() in [301,302, 307, 308]:
                for eachPingResult in self.redirectChain:
                    if foundIt==True:
                        aPingResult.redirectChain.append(eachPingResult)                        
                    if foundIt==False and eachPingResult.getUrl()==aPingResult.getUrl():
                        foundIt=True
                    

        print("done all redirects")    

    def containsLocationAlready(self, arrayOfPingResults, aUrl):
        for pingResult in arrayOfPingResults:
            if aUrl.strip() == pingResult.getUrl():
                return True
        return False
