
# Create WebHook for the Discord Channel: https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks

# Copy the discord.Webhook.from_url

# Send messages

from discord import SyncWebhook


class discord:

    def __init__(self, url: str) -> None:
        self.url = url


    def send(self, message: str) -> None:
        try:
            webhook = SyncWebhook.from_url(self.url)
            webhook.send(message)
        except Exception as e:
            # Print any error messages to stdout
            print(e)