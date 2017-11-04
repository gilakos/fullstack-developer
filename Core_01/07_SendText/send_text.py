from twilio.rest import Client
import creds

client = Client(creds.account_sid, creds.auth_token)

message = client.messages.create(
    to=creds.recipient,
    from_="+16503963995",
    body="Greetings from your friendly Astra Bot! Let's make it rain!",
    media_url="https://media.giphy.com/media/3osxYamKD88c6pXdfO/giphy.gif")

print(message.sid)