web: gunicorn sirius_project.wsgi:application --log-file -
release: python manage.py migrate && python manage.py populate_initial_data

