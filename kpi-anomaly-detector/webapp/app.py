import os

from .portal import create_app


app = create_app()


if __name__ == '__main__':
    host = os.environ.get('KPI_WEB_HOST', '0.0.0.0')
    port = int(os.environ.get('KPI_WEB_PORT', '8000'))
    debug = os.environ.get('KPI_WEB_DEBUG', '').lower() in {'1', 'true', 'yes'}
    app.run(host=host, port=port, debug=debug)