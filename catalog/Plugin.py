

class Plugin:
    def __init__(self, pluginId, bundleId, name):
        self.pluginId = pluginId
        self.bundleId = bundleId
        self.description = ""
        self.shortDescription = ""
        self.version = [0, 0]
        self.details = None
        self.tags = []
        self.presets = None
        self.rate = 0
        self.defautImagePath = None
        self.sampleImagesPath = []

    def setDescription(self, description):
        self.description = description

    def addPluginDetails(self, details):
        self.details = details

    def printBundle():
        print "Plugin :"
        print "pluginId:", self.pluginId
        print "bundleId:", self.bundleId
        print "description:", self.description
        print "shortDescription:", self.shortDescription
        print "version:", self.version
        print "details:", self.details
        print "tags:", self.tags
        print "presets:", self.presets
        print "rate:", self.rate
        print "defautImagePath:", self.defautImagePath
        print "sampleImagesPath:", self.sampleImagesPath
