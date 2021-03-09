import logging

logging = logging.getLogger(__name__)


def validate_email(emails):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    valid_emails = []
    for email in emails:
        try:
            validate_email(email)
            valid_emails.append(email)
        except ValidationError:
            logging.error("email validation failed for email - {}".format(email))
    return valid_emails


def send_email(emails):
    from django.core.mail import EmailMessage
    logging.info("send mail called")
    subject = "Weather Information"
    message = "Please Find Attached xl sheet of weather information"
    from_address = "ankitkhandelwal185@gmail.com"
    try:
        from django.core import mail
        email = mail.EmailMessage(
            subject,
            message,
            from_address,
            emails,
        )
        email.attach_file('output.xlsx')
        email.send()
        logging.info("Successfully sent email to {}".format(emails))
    except Exception as e:
        logging.error("Exception occurred while sending emails, exception is {}".format(str(e)))