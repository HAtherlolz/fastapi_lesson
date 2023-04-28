from api.services.email.email import send_email

from config.conf import settings

from pathlib import Path


def send_reg_email(email_to: str) -> None:
    """
        Send email after registration
    """
    project_name = settings.EMAILS_FROM_NAME
    subject = f"{project_name} - Registration email"
    print("--------------------------------", Path(__file__).parent.parent.parent)
    with open(Path(__file__).parent.parent.parent.parent / 'templates' / "emails" / "registration.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "login": email_to,
        }
    )
