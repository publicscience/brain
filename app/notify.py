from app import app

# Email error messages.
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler((MAIL_HOST, MAIL_PORT), 'dont-talk-back@'+MAIL_HOST, MAIL_TARGETS, 'brain is floudering!', (MAIL_USER, MAIL_PASS))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

