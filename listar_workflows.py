import os
import json
import shutil
import argparse
import psycopg2
import requests
from pathlib import Path
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv

def cargar_config(dotenv_path):
    if not os.path.isfile(dotenv_path):
        raise FileNotFoundError(f"No se encontró el archivo: {dotenv_path}")
    load_dotenv(dotenv_path)

    api_url = os.getenv("N8N_API_URL").rstrip("/")
    if "/rest" in api_url:
        raise ValueError("❌ N8N_API_URL no debe incluir el sufijo '/rest'. Usá solo el dominio base.")


def obtener_datos():
    with SSHTunnelForwarder(
        (os.getenv("SSH_HOST"), int(os.getenv("SSH_PORT"))),
        ssh_username=os.getenv("SSH_USER"),
        ssh_private_key=os.getenv("SSH_KEY_PATH"),
        remote_bind_address=(os.getenv("DB_HOST"), int(os.getenv("DB_PORT")))
    ) as tunnel:
        conn = psycopg2.connect(
            host="127.0.0.1",
            port=tunnel.local_bind_port,
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()

        query = """
            SELECT f.id, f.name, f."parentFolderId",
                   we.id AS workflow_id, we.name AS workflow_name
            FROM folder f
            INNER JOIN workflow_entity we ON we."parentFolderId" = f.id
            ORDER BY f.name, we.name;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        resultado = {}
        for folder_id, folder_name, parent_id, workflow_id, workflow_name in rows:
            if folder_name not in resultado:
                resultado[folder_name] = {
                    "id": folder_id,
                    "parentFolderId": parent_id,
                    "workflows": []
                }
            resultado[folder_name]["workflows"].append({
                "id": workflow_id,
                "name": workflow_name
            })

        cursor.close()
        conn.close()

    return resultado

def descargar_workflow(workflow_id):
    api_url = os.getenv("N8N_API_URL").rstrip("/")
    api_key = os.getenv("N8N_API_KEY")

    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    response = requests.get(f"{api_url}/workflows/{workflow_id}", headers=headers)
    response.raise_for_status()
    return response.json()

def guardar_workflows(data, output_dir):
    # Limpiar carpeta de salida
    output_path = Path(output_dir)
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    # Crear carpetas y guardar workflows
    for folder_name, info in data.items():
        folder_path = output_path / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        for wf in info["workflows"]:
            workflow_json = descargar_workflow(wf["id"])
            filename = f"{wf['name']}.json"
            print(f"Download workflow: {wf['name']}")
            file_path = folder_path / filename
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(workflow_json, f, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="Exportar workflows de n8n por carpeta desde PostgreSQL y API REST.")
    parser.add_argument("--env", required=True, help="Ruta al archivo .env con credenciales")
    parser.add_argument("--out", required=True, help="Ruta de la carpeta de destino para los workflows")

    args = parser.parse_args()
    cargar_config(args.env)
    data = obtener_datos()
    guardar_workflows(data, args.out)
    print("✅ Workflows exportados exitosamente.")

if __name__ == "__main__":
    main()
