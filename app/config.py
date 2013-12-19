from app.models import Config

# Create Config object if necessary.
if len(Config.objects) < 1:
    config = Config()
    config.save()

def config():
    """
    Loads the Config.
    Loading it on the fly means the latest
    configuration will always be used.
    """
    return Config.objects[0]
