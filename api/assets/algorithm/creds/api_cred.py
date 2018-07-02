
class Credentials():
    def __init__(self):
        self.creds = {
            'azure' : {
                'subscription_key' : "3e8bfdcfae0c41569d5c54ec94e8503a",
                'endpoint' : "https://westus2.api.cognitive.microsoft.com/text/analytics/v2.0/"
            }
        }

    def get(self, api):
        return self.creds[api]