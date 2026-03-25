import os

class Config:
    def get_anthropic_api_key(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if  api_key == None:
            raise Exception("Non available model")

        return api_key
