from .core_text import Text


def email_approver(approver_email, template_url):
    import webbrowser
    import urllib.parse

    subject = 'Request for access to Gryphon template'

    url_data = urllib.parse.urlencode(
        dict(
            to=approver_email,
            subject=subject,
            body=Text.access_request_email_template.replace("{template_url}", template_url)
        ),
        quote_via=urllib.parse.quote
    )

    webbrowser.open(f"mailto:?{url_data}", new=0)

