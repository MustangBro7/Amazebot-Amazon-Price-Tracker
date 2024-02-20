from your_app import app  # Import your Flask app object

if __name__ == '__main__':
    from gunicorn.app.base import Config
    from gunicorn.app.logging import LoggingFormatter

    class CustomConfig(Config):
        # Adjust these values as needed
        workers = 3
        threads = 2
        loglevel = 'info'
        access_log_format = LoggingFormatter.default_format

    config = CustomConfig()
    app.run(debug=False, config=config)
