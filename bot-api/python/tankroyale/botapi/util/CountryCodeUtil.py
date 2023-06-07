# I know is the correct way to do this, but it works for now.
class CountryCodeUtil:

    @staticmethod
    def getLocalCountryCode():    
        return "GB"
    
    @staticmethod
    def toCountryCode(countryCode):
        return countryCode.upper()
    
    

