import argparse
import os.path

from AuditProject import AuditProject


class TechAuditCommandLineParamsConfig:

    def __init__(self):
        self.dictargs = {}
        self.auditProject = AuditProject(None)
        self.parseArgs()
        self.args = []
        self.dictargs={}

    def parseArgs(self):

        parser = argparse.ArgumentParser(description='Technical Audit')
        parser.add_argument('-name', help='name of project')
        parser.add_argument('-domain', help='a domain to scan e.g. talotics.com')
        parser.add_argument('-aliases', help='a list of aliases for the domain', nargs='*')
        parser.add_argument('-config', help='config file details json file')

        self.args = parser.parse_args()
        self.dictargs = vars(self.args)



        self.setFromDictArgs(self.dictargs)

    def setFromDictArgs(self, dict):      

        self.configFile = None  

        if "config" in dict and dict["config"] is not None:
            self.configFile = dict["config"]
        else:
            # if default config file exists
            defaultFile = "default-project.json"
            if os.path.isfile(defaultFile):
                self.configFile = defaultFile            

        if self.configFile is not None:
            self.auditProject.loadConfigFile(self.configFile)
        else:
            if "name" in dict and dict["name"] is not None:
                self.auditProject.setName(dict["name"])
            else:
                self.auditProject.setName("default-project")

            if "domain" in dict and dict["domain"] is not None:
                self.auditProject.addDomain(dict["domain"])

                if "aliases" in dict and dict["aliases"] is not None:
                    if len(dict["aliases"] >0):
                        self.auditProject.addDomain(dict["domain"])
        
        return self
    
    def getAuditProject(self):
        return self.auditProject