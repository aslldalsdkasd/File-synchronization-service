# Инструкция

### Все реализовано одним классом ###
### Загрузка, обновление, удаление реализовано в методах ###

### В [config.ini](config.ini) нужно указать токен, 
    name_dir название папки на диске (его не обязательно создавать самому, при добавлении файла он создасться сам)
###

### dir_path нужно указать директорию откуда нужно перекидывать файлы
    а также log_path путь в котором будут лежать логи
###

###### примеры вывода при load:
    2026-04-22 21:41:30,983 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): cloud-api.yandex.net:443
    2026-04-22 21:41:32,145 - urllib3.connectionpool - DEBUG - https://cloud-api.yandex.net:443 "GET /v1/disk/resources/upload?path=/TESTDIRTEXT/test_text.txt&overwrite=true HTTP/1.1" 200 None
    2026-04-22 21:41:32,147 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): cloud-api.yandex.net:443
    2026-04-22 21:41:33,375 - urllib3.connectionpool - DEBUG - https://cloud-api.yandex.net:443 "GET /v1/disk/resources/?path=TESTDIRTEXT HTTP/1.1" 200 None
    2026-04-22 21:41:33,376 - class_sync - INFO - folder exists
    2026-04-22 21:41:33,380 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): uploader10sas.disk.yandex.net:443
    2026-04-22 21:41:34,703 - urllib3.connectionpool - DEBUG - https://uploader10sas.disk.yandex.net:443 "PUT /upload-target/20260422T214045.473.utd.4a66on3nuaoqjw6vmeb5u57ew-k10sas.8792393 HTTP/1.1" 201 None
    2026-04-22 21:41:34,704 - class_sync - INFO - Upload test_text.txt -> /TESTDIRTEXT/test_text.txt
    
    reload:
    2026-04-22 21:41:34,707 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): cloud-api.yandex.net:443
    2026-04-22 21:41:35,728 - urllib3.connectionpool - DEBUG - https://cloud-api.yandex.net:443 "GET /v1/disk/resources/upload?path=/TESTDIRTEXT/test_text.txt&overwrite=true HTTP/1.1" 200 None
    2026-04-22 21:41:35,731 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): uploader58sas.disk.yandex.net:443
    2026-04-22 21:41:36,957 - urllib3.connectionpool - DEBUG - https://uploader58sas.disk.yandex.net:443 "PUT /upload-target/20260422T214049.006.utd.69shdl9bywubv01x6d35owfbi-k58sas.8732936 HTTP/1.1" 201 None
    2026-04-22 21:41:36,959 - class_sync - INFO - Reload test_text.txt -> /TESTDIRTEXT/test_text.txt
    
    delete:
    2026-04-22 21:41:38,600 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): cloud-api.yandex.net:443
    2026-04-22 21:41:40,745 - urllib3.connectionpool - DEBUG - https://cloud-api.yandex.net:443 "DELETE /v1/disk/resources/?path=%2FTESTDIRTEXT%2Ftest_text.txt&permanently=true HTTP/1.1" 204 0
    2026-04-22 21:41:40,746 - class_sync - INFO - Delete test_text.txt -> /TESTDIRTEXT/test_text.txt
    
    get_info:
    2026-04-22 21:41:36,962 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): cloud-api.yandex.net:443
    2026-04-22 21:41:38,596 - urllib3.connectionpool - DEBUG - https://cloud-api.yandex.net:443 "GET /v1/disk/resources/?path=%2FTESTDIRTEXT HTTP/1.1" 200 None
    2026-04-22 21:41:38,597 - class_sync - INFO - test_text.txt - file 