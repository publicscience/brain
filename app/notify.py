from app import app

cfg = app.config

# Email error messages.
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler((cfg['MAIL_HOST'], cfg['MAIL_PORT']), 'dont-talk-back@'+cfg['MAIL_HOST'], cfg['MAIL_TARGETS'], 'brain is floudering!', (cfg['MAIL_USER'], cfg['MAIL_PASS']))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

