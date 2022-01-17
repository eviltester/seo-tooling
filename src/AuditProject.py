import os
import glob
import json
from DomainParser import DomainParser

class AuditProject:

    # project
    #  seo-audit-project.txt
    #  /whois
    #     /domain
    #        /whois-domain-timestamp.txt

    # handle no default data passed into constructor1python
    
    def __init__(self, data):

        self.blankProjectData = {
            "projectName" : "",
            # array of fully qualified url strings
            "sitemapUrls" : [],
            # array of domain name strings e.g. ['talotics.com']
            "portfolioSiteUrls" : [],
            # dictionary of domain to arry of other domains e.g.
            # {'talotics.com':['digitalonlinetactics.com']}
            "siteAliases" : {}
        }

        
        self.name = ""
        self.sitemapUrls = []            
        self.portfolioSiteUrls = []             
        self.siteAliases = {}       

        if data is not None:
            self.setFromData(data)

        self.rootfolder = os.getcwd()
        self.projectPath = os.path.join(self.rootfolder, self.name)

        # automatically define portfolio site objects
        '''         portfolioSites = {}

                for site in portfolioSiteUrls:
                    portfolioSites[site] = PortfolioSite(site)

                for siteWithSynonyms in synonymsForSite.keys():
                    site = portfolioSites[siteWithSynonyms]
                    for synonym in synonymsForSite[siteWithSynonyms]:
                        site.alsoKnownAs(synonym)
        '''             

    def setFromData(self,data):

        # todo: check they are the correct type before assignment

        if "projectName" in data:
            self.name = data['projectName']

        if "sitemapUrls" in data:    
            self.sitemapUrls.extend(data['sitemapUrls'])

        if "portfolioSiteUrls" in data:    
            self.portfolioSiteUrls.extend(data['portfolioSiteUrls'])

        if "siteAliases" in data:    
            self.siteAliases.update(data['siteAliases'])


    def loadConfigFile(self, file):
        print(repr(file))
        if os.path.isfile(file):
            with open (file, "r") as inputFile:
                auditProjectData = json.load(inputFile)
                self.setFromData(auditProjectData)
        else:
            print("Can not open config file " + file)


    def setName(self, aName):
        self.name = aName
        
    def addDomain(self, aDomain):
        self.portfolioSiteUrls.append(aDomain)

    def addDomainAliases(self, aDomain, aliasesArray):
        self.siteAliases[aDomain] = aliasesArray.copy()

    def getPortfolioSiteDomains(self):
        return self.portfolioSiteUrls

    def getAllDomains(self):
        return self.getDomains()['domains']

    def getAllSubDomains(self):
        return self.getDomains()['subdomains']

    def getAllBaseDomains(self):
        return self.getDomains()['basedomains']        

    def getDomains(self):
        # {'basedomains': [],  'subdomains': [], 'domains': []}

        basedomains = []
        subdomains = []
        domains = []

        domainToCheck = []

        for siteUrl in self.portfolioSiteUrls:
            domainToCheck.append(siteUrl)

        domainToCheck.extend(self.getAllSynonymDomains())            

        for aDomain in domainToCheck:            
            parsedUrl = DomainParser(aDomain)
            if parsedUrl.hasSubdomain():
                subdomains.append(aDomain)
            else:
                basedomains.append(aDomain)
            domains.append(aDomain)

        return {'basedomains': basedomains,  'subdomains': subdomains, 'domains': domains}

    def getAllSynonymDomains(self):
        domains = []
        for siteDomain in self.siteAliases:
            for synonymDomain in self.siteAliases[siteDomain]:
                domains.append(synonymDomain)
        return domains
    
    def getSitemapUrls(self):
        return self.sitemapUrls

    def getBlankProjectData(self):
        return self.getBlankProjectData

    def getProjectData(self):
        return {
                "projectName" : self.name,
                "sitemapUrls" : self.sitemapUrls,
                "portfolioSiteUrls" : self.portfolioSiteUrls,
                "siteAliases" : self.siteAliases
            }
        

    def makeProjectFolder(self):
        os.makedirs(self.projectPath, exist_ok=True)
    
    def getMostRecentFileMatchingIn(self, match, destination):
        # '/path/to/folder/*'
        # destination - '/path/to/folder'
        # match - *
        globIs = os.path.join(destination, match)

        listOfFiles = glob.glob(globIs)
        if len(listOfFiles)==0:
            return None

        latestFile = max(listOfFiles, key=os.path.getctime)
        return latestFile

    def cacheAsFile(self, filename, folder, contents):
        os.makedirs(folder, exist_ok=True)
        file = os.path.join(folder, filename)
        with open(file, "w") as text_file:
            text_file.write(contents)

    def getCachedFile(self, filename, folder, contents):
        return ""

    def existsInCache(self, filename, folder, contents):
        return False

    def getWhoIsFolderName(self, domain):
        return os.path.join(self.projectPath, "whois", domain)   