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

