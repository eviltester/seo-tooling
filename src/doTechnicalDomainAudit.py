import advertools
import json

from datetime import date

from DomainParser import DomainParser
from AuditProject import AuditProject
from TechnicalAuditor import TechnicalAuditor
from WhoIs import WhoIs
from PortfolioSite import PortfolioSite
from PingResult import PingResult
from DomainHttpsRedirectChecker import DomainHTTPsRedirectChecker
from CommandArgsParse import TechAuditCommandLineParamsConfig

'''
auditProjectData = {
    # e.g. "projectName" : 'talotics',
    "projectName" : '',
    "sitemapUrls" : [],
    # e.g. "portfolioSiteUrls" : ['talotics.com'],
    "portfolioSiteUrls" : [],
    # e.g. "siteAliases" : {'talotics.com':['digitalonlinetactics.com']
    "siteAliases" : {}
}

with open ("default-project.json", "w") as outputFile:
    json.dump(auditProjectData, outputFile, indent=4)
'''

# todo: pass in a url from command line can do basic audit from this
# todo: pass in a url and aliases list from command line

auditProject = TechAuditCommandLineParamsConfig().getAuditProject()


# todo pass in filename from command line
# only if file exists







# todo: create folder for project data
# todo: cache data in project folder and read from cache if still relevant
# todo: types of urls: base, canonical, synonym, temporary synonym, alias
# todo: also add canonical urls e.g. https://www.talotics.com
    

technicalAuditor = TechnicalAuditor(auditProject)

print("Starting Audit")
print("Auditing Domains List")
technicalAuditor.auditDomainsList()
print("Auditing SSL Certificates")
technicalAuditor.auditBaseDomainSSLCertificates()
print("Auditing Base Domain Who is Entries")
technicalAuditor.auditBaseDomainWhoIsEntries()
print("Auditing Urls and Redirects")
technicalAuditor.auditPingUrlCombosAndRedirects()

# generatee a markdown report

print("\n## Domains\n")
for reportStatement in technicalAuditor.getResultsAuditDomainsList():
    print("* " + reportStatement)


print("\n## SSL Certificate Expiry\n")
for reportStatement in technicalAuditor.getResultsAuditBaseDomainSSLCertificates():
    print("* " +reportStatement)
print("\n")

 
print("\n## Domain Expiry\n")
for reportStatement in technicalAuditor.getResultsAuditBaseDomainWhoIsEntries():
    print("* " + reportStatement)
print("\n") 


# check all sites are available
# todo: store the 'ping results' and don't 'ping' within a certain configurable period
# todo: report errors, allow configuring what is a 'valid' response
# todo: check http, https, www combinations

# todo: implement as checklist
# [] url supports https
# [] http url redirects to https
# [] canonical (either www. or base is enforced through redirect)
# [] https is valid
# [] canonical url configured in bing, gogole search, analytics etc.
# [] ssl expiry
# [] for main pages check final redirect endpoint matches the canonical on the page



# check all urls handle http and https
# todo: if given a canonical then check that url redirect to canonical
# todo: report errors/warnings e.g. http not redirected to https



print("## Ping Urls\n")


def printRedirectChain(pingResult):
    indentPrefix = ""
    indentAmount=0

    if pingResult.hasRedirects():
        for redirect in pingResult.getRedirectChain().values():
            indentPrefix = indentAmount * "   "
            redirectInfo = ""
            if len(redirect.getRedirectsTo())>0:
                redirectInfo = " redirects to " + redirect.getRedirectsTo()
            else:
                redirectInfo = " terminates with "
            print(indentPrefix + "* " + redirect.getUrl() + redirectInfo + " (" + str(redirect.getStatusCode()) + ")")
            indentAmount = indentAmount+1
                        

# dict of DomainHTTPsRedirectChecker objects
pingResults = technicalAuditor.getAuditPingResults() 
for result in pingResults.values():
    print("\n### " + result.getDomain())

    # array of ping results
    statusChecks = result.getPingStatusChecks()

    for pingResult in statusChecks:
        # output ping
        print("\n* GET " + pingResult.getUrl() + " status code " + str(pingResult.getStatusCode()))
        # output redirect info
        if pingResult.hasRedirects():
            printRedirectChain(pingResult)
        # output errors
        errorsToReport = pingResult.getErrorMessages()
        if(len(errorsToReport)>0):
            print("* Errors")
            for anError in errorsToReport:
                print("   * " + anError)

print("\n")    





   






    # stream = os.popen(command)
    # whois = stream.read()
    
    # keyValuePairs = whois.split("\n")
    # for kvp in keyValuePairs:
    #     if "Expiration Date" in kvp:
    #         print( tld)
    #         kv = kvp.split(":")
    #         print(kv[1])


# todo: read the sitemap url to file and cache for local manipulation
# todo: cache the dataframe for sitemap and re-read from disk rather than url
# see to json and read json for dataframe caching https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html
'''
for sitemapUrl in auditProject.getSitemapUrls():
    sitemapDataFrame = advertools.sitemap_to_df(sitemapUrl, recursive=True)
    print(sitemapDataFrame.columns)
    print(sitemapDataFrame)
'''    

# Page Audit
# title
# description
# social media meta data
# canonical
# links - broken, text used to link, rel attribute
# images - broken, alt, dimensions vs rendered dimensions, kb size vs compressed size

# Content Audit