# Proyecto Django — histories_configurations (SQLite)

## Cómo ejecutar
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Endpoints clave:
- `GET /histories_configurations/histories/`
- `POST /histories_configurations/histories/create/` (JSON: { "document_type": 1, "document_number": "12345678" })

Página de prueba:
- `GET /` (renderiza `templates/demo.html` y tiene un botón para hacer fetch)
