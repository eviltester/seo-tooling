class PortfolioSite:

    def __init__(self, url):
        self.url = url
        self.synonyms = []

    def alsoKnownAs(self, synonym):
        self.synonyms.append(synonym)

    def getUrl(self):
        return self.url

    def hasSynonyms(self):
        return len(self.synonyms)>0

    def getSynonyms(self):
        return self.synonyms