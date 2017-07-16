# Content

This is a simple demo to get data from bter.com

# Install

* download the release tar ball
* extra the tar-ball and execute: cd bter
* install the requirements execute: pip install -r requirements.txt
* extra the tar-ball then execute: python setup.py install
* copy the direct etc which in the tar-ball to any location you like

# Modify the configuration

* as default, you need modify the option: database.connection to specify the database connection-url
* modify the option: log.log\_path to specify the log path

# Start the server:

* python bter-server \<conf\_file\>
* note: the conf\_file is the absolute path of bter.ini

# examples:

* After install bter, I use the directory: /Users/mengalong/code/t/xy as the top path
* In the top_path, there is the directory 'etc' that contains the bter.ini and pipeline.yaml
* Use the command-line to start the server: bter-server /Users/mengalong/code/t/xy/etc/bter/bter.ini &>/dev/null </dev/null &
* My bter.ini like this:
```cython
[DEFAULT]
namespaces = bter

[log]
log_format = %(asctime)s [PID %(process)d] [%(levelname)s] %(name)s:%(lineno)d %(message)s
log_path = /Users/mengalong/code/t/xy/log
log_filename = bter.log
log_level = DEBUG

[database]
connection = file:///Users/mengalong/code/t/xy/log/sample.data?max_bytes=10240000&backup_count=5
```

