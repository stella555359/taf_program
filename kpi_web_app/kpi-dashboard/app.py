from portal import create_app


app = create_app()


if __name__ == '__main__':
    host = str(app.config.get('KPI_DASHBOARD_HOST') or '0.0.0.0')
    port = int(app.config.get('KPI_DASHBOARD_PORT') or 8010)
    debug = bool(app.config.get('KPI_DASHBOARD_DEBUG'))
    app.run(host=host, port=port, debug=debug)