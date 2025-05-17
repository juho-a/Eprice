from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# TODO: Move these to a config.secrets file
MAIL_USERNAME="tuomas.m.rei@gmail.com"
MAIL_PASSWORD="ttxy bzlo eabf ngtp"
MAIL_FROM="tuomas.m.rei@gmail.com"
MAIL_PORT=587
MAIL_SERVER="smtp.gmail.com"
MAIL_FROM_NAME="Eprice-verification"

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=True,      # Add this line
    MAIL_SSL_TLS=False       # And this line (set to True if your SMTP requires SSL/TLS)
)

async def send_email_async(email_to: str, verification_code: str):
    '''Send an email asynchronously'''
    subject = 'Verify your email address'
    body = f'''
    <html>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h1>Verify your email address</h1>
            <p>Use the code below to verify your email address:</p>
            <div style="display: inline-block; margin: 20px auto; padding: 16px 32px; background: #f3f3f3; border-radius: 8px; font-size: 2em; letter-spacing: 0.2em; font-weight: bold; color: #333;">
                {verification_code}
            </div>
            <p>Or click the link below to verify directly:</p>
            <a href="http://localhost:5173/auth/verify?email={email_to}&code={verification_code}"
               style="display: inline-block; margin-top: 16px; padding: 12px 24px; background: #2563eb; color: #fff; text-decoration: none; border-radius: 6px; font-size: 1.1em;">
                Verify Email
            </a>
        </body>
    </html>
    '''
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype='html',
    )
    
    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')
