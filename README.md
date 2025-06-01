# n8n-workflows-cli

Herramienta de línea de comandos (CLI) para exportar automáticamente todos los workflows de una instancia de n8n organizada por carpetas, usando un túnel SSH para acceder a la base de datos PostgreSQL y la API REST de n8n para obtener los workflows completos.

---

## 🚀 Funcionalidad

- Se conecta por SSH a un VPS donde corre n8n y su base de datos.
- Consulta PostgreSQL para obtener la lista de carpetas y workflows.
- Descarga los workflows reales desde la API REST de n8n.
- Organiza los archivos en carpetas con formato `folder/workflow.json`.
- Limpia previamente el directorio de destino antes de exportar.

---

## 📦 Requisitos

- Python 3.8+
- Acceso SSH al VPS donde está la base de datos de n8n
- API Key personal generada en tu instancia de n8n
- Acceso a la API REST de n8n

---

## 🧰 Instalación

1. Clonar este repositorio:

```bash
git clone git@github.com:jeastman19/n8n-workflows-cli.git
cd n8n-workflows-cli
```

2. Crear y activar un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Variables de entorno

Crear un archivo `.env` con el siguiente contenido:

```env
# SSH para acceder al VPS
SSH_HOST=mi-servidor.com
SSH_PORT=22
SSH_USER=n8n
SSH_KEY_PATH=/home/usuario/.ssh/id_rsa

# PostgreSQL interno de n8n
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=root
DB_PASSWORD=123456

# API REST de n8n
N8N_API_URL=https://n8n.mi-dominio.com
N8N_API_KEY=n8n_pat_xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🧪 Ejecución

```bash
python listar_workflows.py --env /ruta/al/.env --out /ruta/destino
```

Ejemplo:

```bash
python listar_workflows.py --env .env --out ./exported_workflows
```

---

## 📂 Salida esperada

```
exported_workflows/
├── MailMind RAG/
│   ├── Logger.json
│   ├── EmailFetcher - Informes.json
│   └── ...
├── Learn n8n/
│   ├── Web Scrap.json
│   └── ...
```

---

## 🛠️ Notas

- El contenido del directorio de salida se elimina completamente en cada ejecución.
- Cada workflow se descarga directamente desde la API REST, asegurando fidelidad total.
- Los nombres de archivos coinciden con el nombre del workflow en n8n.

---

## 🧾 Licencia

MIT

---

## 🤝 Autor

Jorge Eastman — [@jeastman](https://github.com/jeastman)
