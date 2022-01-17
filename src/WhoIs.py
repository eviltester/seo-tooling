import os # for who is
import whois

# use whois library instead of command line https://github.com/richardpenman/whois
class WhoIs:
    def __init__(self, domainName, auditProject):
        self.domainName = domainName
        self.project = auditProject
    
    def getWhoIsDetails(self):

        self.whoisdetails = whois.whois(self.domainName)
        

    def getExpiryDate(self):
        return self.whoisdetails.expiration_date.strftime("%Y-%m-%d, %H:%M:%S")
        

class WhoIsOSCommand:
    def __init__(self, domainName, auditProject):
        self.domainName = domainName
        self.project = auditProject
    
    def getWhoIsDetails(self):

        whoIsFolder = self.project.getWhoIsFolderName(self.domainName)
        filenamePrefix = "whois-" + self.domainName + "-"

        mostRecent = self.project.getMostRecentFileMatchingIn(filenamePrefix + "*", whoIsFolder)
        
        # if cache then use that
        if mostRecent!=None:
            f = open(mostRecent, "r")
            self.whoIsDetails = f.read()
        else:
            command = 'whois ' + self.domainName
            stream = os.popen(command)
            self.whoIsDetails = stream.read()

            # store to cache
            datePart = date.today().strftime("%Y-%m-%d-%H-%M-%S")
            filename = filenamePrefix + datePart + ".txt"

            os.makedirs(whoIsFolder, exist_ok=True)
            self.project.cacheAsFile(filename, whoIsFolder, self.whoIsDetails)
        

    def getExpiryDate(self):
        whois = self.whoIsDetails
        keyValuePairs = whois.split("\n")
        retVal=""
        for kvp in keyValuePairs:
            if "Registrar Registration Expiration Date" in kvp:
                kv = kvp.split(":")
                retVal += ":".join(kv[1:]).strip()
            if "Registry Expiry Date" in kvp:
                kv = kvp.split(":")
                retVal += ":".join(kv[1:]).strip()
            if "Expiry date" in kvp:
                kv = kvp.split(":")
                retVal += ":".join(kv[1:]).strip()                   
            if len(retVal.strip())>0:
                return retVal
        return ""    
