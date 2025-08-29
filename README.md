#  Módulo 6 – Historias y Configuración

Este proyecto es una aplicación **Django** conectada a **MySQL** que implementa un sistema de historias clínicas con **multi-tenant** (soporte para múltiples clínicas), gestión de usuarios y autenticación.

---

## Características

*  **Multi-tenant**: Soporta múltiples clínicas, cada una con sus propios pacientes e historias clínicas.
*  **Autenticación de usuarios**: Inicio y cierre de sesión con Django Auth.
*  **CRUD de historias clínicas**: Crear, leer, actualizar y eliminar registros de pacientes.
*  **Base de datos MySQL**: Datos persistentes y escalables.
*  **Panel de administración Django**: Gestión rápida de modelos.

---

##  Tecnologías utilizadas

* [Python 3.13](https://www.python.org/)
* [Django 5.2](https://www.djangoproject.com/)
* [MySQL 8.0](https://www.mysql.com/)
* [django-multitenant](https://pypi.org/project/django-multitenant/)
* HTML, CSS (Bootstrap opcional)

---

##  Estructura básica

```bash
Modulo-6-Historias-y-Configuracion-/
├── clinic_project/        # Configuración principal de Django
│   ├── settings.py        # Configuración del proyecto
│   ├── urls.py            # Rutas principales
│   └── middleware.py      # Middleware personalizado para multi-tenant
├── clinics/               # App para gestión de clínicas
├── records/               # App para historias clínicas
├── templates/             # Plantillas HTML
├── manage.py              # Script de Django
└── README.md              # Documentación del proyecto
```

---

##  Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/isnteres/Modulo-6-Historias-y-Configuracion-.git
cd Modulo-6-Historias-y-Configuracion-
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

*(Si no tienes `requirements.txt`, instálalas manualmente)*:

```bash
pip install django mysqlclient django-multitenant
```

### 4. Crear base de datos MySQL

Conéctate a MySQL:

```bash
mysql -u root -p
```

Crea la base de datos:

```sql
CREATE DATABASE clinic_db;
```

### 5. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Iniciar servidor

```bash
python manage.py runserver
```

Accede en [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

---

##  Credenciales de prueba

| Usuario | Contraseña |
| ------- | ---------- |
| admin   | admin123   |

---

##  Notas

* Asegúrate de tener **MySQL corriendo** antes de iniciar el proyecto.
* El middleware `CurrentClinicMiddleware` se encarga de filtrar datos según `clinic_id`.
* Se recomienda usar un entorno virtual para evitar conflictos de dependencias.

---


