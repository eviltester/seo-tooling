import requests

from DomainParser import DomainParser
from PingResult import PingResult


class DomainHTTPsRedirectChecker:

    def __init__(self, tld):
        self.url = tld
        if tld.startswith("https://"):
            self.url = self.url.replace("https://","")
        if tld.startswith("http://"):
            self.url = self.url.replace("http://","")
        # remove any trailing back slash            
        self.url = self.url.replace("/","")   
        self.checks = []     

    def getDomain(self):
        return self.url        

    def ping(self):

        domain = DomainParser(self.url)
        schemes = ["https://", "http://", "https://www.", "http://www."]

        if domain.hasSubdomain():
            schemes = ["https://", "http://"]

        trailers = [""]

        # for each scheme, for each trailer
        # ping the URL, check status, follow redirect chain
        for scheme in schemes:
            for trailer in trailers:
                url = scheme + self.url + trailer

                # print("Pinging: " + url)
                response = requests.head(url)
                pingStatus = PingResult(url, response.status_code)
                self.checks.append(pingStatus)
                print("* " + url + " - " + str(response.status_code))

                if response.status_code in [301,302, 303, 307, 308]:
                    if("location" in response.headers):
                        redirectTo = response.headers['location']
                        pingStatus.followRedirectChain(redirectTo)
                else:
                    if url.startswith("http:"):
                        pingStatus.addErrorMessage(" HTTP should redirect to HTTPS")

                if len(pingStatus.redirectError)>0:
                    for message in pingStatus.getErrorMessages():
                        print("   * WARNING " + message)

                print("")

    def getPingStatusChecks(self):
        return self.checks
