from pathlib import Path

import requests
from log import logger
import logging.config
import configparser
from urllib.parse import quote

logging.config.dictConfig(logger)
log = logging.getLogger(__name__)


class Synchronization:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini", encoding="utf-8")
        self.token = config["TOKEN"]["token"]
        self.path = Path(config["DEFAULT"]["dir_path"])
        self.dir_name = config["DEFAULT"]["name_dir"]
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources/"
        self.headers = {
            "Authorization": f"OAuth {self.token}",
        }
        self.auth = None

    def load(self, path):
        local_path = Path(path)
        if not local_path.exists():
            raise FileNotFoundError(local_path)
        rel_path = local_path.relative_to(self.path)
        cloud_path = f"/{self.dir_name}/{rel_path}"
        get_url = f"{self.base_url}upload?path={quote(cloud_path)}&overwrite=false"

        response = requests.get(get_url, headers=self.headers)
        if response.status_code == 401:
            log.error("You are not authorized, invalid token")
            return

        if not self.check_folder():
            self.create_folder(get_url)

        if response.status_code == 409:
            log.info(f"Файл {cloud_path} уже существует пропускаем")
            return
        response.raise_for_status()
        upload_url = response.json()["href"]
        with open(local_path, "rb") as file:
            upload_response = requests.put(upload_url, files={"file": file})
            upload_response.raise_for_status()
            log.info(f"Upload {path} -> {cloud_path}")

    def reload(self, path):
        local_path = Path(path)
        if not local_path.exists():
            raise FileNotFoundError(local_path)
        rel_path = local_path.relative_to(self.path)
        cloud_path = f"/{self.dir_name}/{rel_path}"
        get_url = f"{self.base_url}upload?path={quote(cloud_path)}&overwrite=true"
        response = requests.get(get_url, headers=self.headers)
        if response.status_code == 401:
            log.error("You are not authorized, invalid token")
            return
        if response.status_code == 404:
            self.create_folder(get_url)
        response.raise_for_status()
        reload_url = response.json()["href"]
        with open(local_path, "rb") as file:
            response = requests.put(
                reload_url, files={"file": file}, headers=self.headers
            )
            response.raise_for_status()
            log.info(f"Reload {path} -> {cloud_path}")

    def delete(self, filename):
        local_path = Path(filename)
        rel_path = local_path.relative_to(self.path)
        cloud_path = f"/{self.dir_name}/{rel_path}"
        url_delete = f"{self.base_url}"
        params = {"path": cloud_path, "permanently": "true"}
        response = requests.delete(url_delete, headers=self.headers, params=params)
        if response.status_code == 401:
            log.error("You are not authorized, invalid token")
            return
        response.raise_for_status()
        log.info(f"Delete {filename} -> {cloud_path}")

    def get_info(self):
        cloud_path = f"/{self.dir_name}"
        get_url = f"{self.base_url}"
        response = requests.get(
            get_url,
            headers=self.headers,
            params={
                "path": quote(cloud_path),
            },
        )
        if response.status_code == 401:
            log.error("You are not authorized, invalid token")
            return
        response.raise_for_status()
        data = response.json()
        items = data.get("_embedded", {}).get("items", [])
        if len(items) == 0:
            log.info("files not found")
        for item in items:
            log.info(f"{item['name']} - {item['type']}")

    def create_folder(self, get_url):
        log.warning(f"Folder for {self.dir_name} is missing, create {self.dir_name}")
        create_url = f"{self.base_url}?path={quote(self.dir_name)}"
        response = requests.put(create_url, headers=self.headers)
        response.raise_for_status()
        log.info("Папка создана")
        response = requests.get(get_url, headers=self.headers)
        return True

    def check_folder(self):
        url = f"{self.base_url}"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        item_type = data.get("type", "")
        if item_type != "file":
            log.info("folder exists")
            return True
        else:
            log.info("folder not exists")
            return False


if __name__ == "__main__":
    Path("logs").mkdir(exist_ok=True)
    sync = Synchronization()
    sync.delete("log.py")
    sync.get_info()
    sync.load("log.py")
    sync.get_info()
