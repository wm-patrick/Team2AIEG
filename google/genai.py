class Models:
    def generate_content(self, model, contents):
        class R:
            text = "[stub] AI service unavailable in test environment."
        return R()

class Client:
    def __init__(self, api_key=None):
        self.models = Models()
