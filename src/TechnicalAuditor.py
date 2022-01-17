from DomainParser import DomainParser 
import ssl, socket
from WhoIs import WhoIs
from DomainHttpsRedirectChecker import DomainHTTPsRedirectChecker

class TechnicalAuditor:

    def __init__(self, auditProject):
         self.auditProject = auditProject
         self.auditDomainListReportLines = []
         self.auditBaseDomainSSLCertificatesReportLines = []
         self.auditWhoIsReportLines = []

    def auditDomainsList(self):
        domains = []
        for siteDomain in self.auditProject.getPortfolioSiteDomains():
            domains.append(siteDomain)

        for synonymDomain in self.auditProject.getAllSynonymDomains():
            domains.append(synonymDomain)

        self.auditDomainListReportLines = []

        for domain in domains:            
            parsedUrl = DomainParser(domain)
            if parsedUrl.hasSubdomain():
                 self.auditDomainListReportLines.append( domain + " is not a base level domain it has a subdomain of " + parsedUrl.getSubdomain())
            else:
                self.auditDomainListReportLines.append( domain + " is a base level domain" + parsedUrl.getSubdomain())

        return self.auditDomainListReportLines

    def getResultsAuditDomainsList(self):
        return self.auditDomainListReportLines


    def auditBaseDomainSSLCertificates(self):
        self.auditBaseDomainSSLCertificatesReportLines = self.checkDomainSSLCertificates(
                                                            self.auditProject.getAllBaseDomains())
        return self.auditBaseDomainSSLCertificatesReportLines      

    def getResultsAuditBaseDomainSSLCertificates(self):
        return self.auditBaseDomainSSLCertificatesReportLines                                                              

    # TODO: create and SSL Certificate Checker class
    # SSL https://stackoverflow.com/questions/30862099/how-can-i-get-certificate-issuer-information-in-python
    def checkDomainSSLCertificates(self, domains):

        sslReportLines = []

        for tld in domains:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=tld) as s:
                s.connect((tld, 443))
                cert = s.getpeercert()
            #print(cert)
            sslReportLines.append( tld + " " + cert['notAfter'])
        
        self.auditDomainSSLCertificatesReportLines = sslReportLines

        return sslReportLines      


    def auditBaseDomainWhoIsEntries(self):
        self.auditWhoIsReportLines = self.checkWhoIsEntries(self.auditProject.getAllBaseDomains())
        return self.auditWhoIsReportLines

    def getResultsAuditBaseDomainWhoIsEntries(self):
        return self.auditWhoIsReportLines        

    # todo: check if command line whois works before using it
    # todo: cache whois details
    def checkWhoIsEntries(self, domains):        
        whoIsReportLines = []

        for baseDomain in domains:
            #command = 'whois ' + tld
            # print(command)
            whois = WhoIs(baseDomain, self.auditProject)
            whois.getWhoIsDetails()
            #print(whois.getExpiryDate())
            whoIsReportLines.append( baseDomain + " expires on " + whois.getExpiryDate() + " https://who.is/whois/" + baseDomain)    

        return whoIsReportLines

    def auditPingUrlCombosAndRedirects(self):
        pingUrls = self.auditProject.getAllDomains()   

        self.auditPingResults = {}

        for url in pingUrls:
            ping = DomainHTTPsRedirectChecker(url)
            ping.ping()
            self.auditPingResults[ping.getDomain()] = ping

        return self.auditPingResults

    def getAuditPingResults(self):
        return self.auditPingResults        

