from urllib.parse import urlparse

class DomainParser:

    def __init__(self, domain):
        self.domain = domain
        if not domain.startswith("https://") and not domain.startswith("http://"):
            self.domain = "https://" + domain
        self.parsedUrl = urlparse(self.domain)
        self.allocateParts()

    def allocateParts(self):
        self.domainPart = ""
        self.subdomain = ""

        parts = self.parsedUrl.netloc.split(".")
        # last two are the domain

        tldindex = -2
        tldDomainPartsLen=2

        # if there are any more special case top level domains then handle them here
        if(self.domain.endswith(".co.uk")):
            tldindex=-3
            tldDomainPartsLen=3

        #todo: remove any port and add to self.port
        if len(parts)>=tldDomainPartsLen:
            self.domainPart = ".".join(parts[tldindex:])

        if len(parts)>tldDomainPartsLen:
            self.subdomain = ".".join(parts[:tldindex])

    def hasSubdomain(self):
        return self.subdomain!=""

    def getSubdomain(self):
        return self.subdomain

    def getDomain(self):
        return self.domainPart