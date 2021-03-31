#!/usr/bin/python3

import os
import shutil
import logging as log
import sys
from socrate import system, conf

log.basicConfig(stream=sys.stderr, level=os.environ.get("LOG_LEVEL", "WARNING"))

# Actual startup script
try:
  os.environ["FRONT_ADDRESS"] = system.resolve_address(os.environ.get("HOST_FRONT", "front"))
except NameError:
  os.environ["FRONT_ADDRESS"] = None

os.environ["IMAP_ADDRESS"] = system.resolve_address(os.environ.get("HOST_IMAP", "imap"))
os.environ["SMTP_ADDRESS"] = system.resolve_address(os.environ.get("HOST_SMTP", "imap"))

os.environ["MAX_FILESIZE"] = str(int(int(os.environ.get("MESSAGE_SIZE_LIMIT"))*0.66/1048576))

try:
    domains = os.environ.get("MAIL_DOMAINS")
except NameError:
    domains = None

try:
    overrides = os.environ.get("OVERRIDES_CONFIG")
except NameError:
    overrides = False

if domains is None:
  base = "/data/_data_/_default_/"
  shutil.rmtree(base + "domains/", ignore_errors=True)
  os.makedirs(base + "domains", exist_ok=True)
  os.makedirs(base + "configs", exist_ok=True)

  if not overrides:
    conf.jinja("/default.ini", os.environ, base + "domains/default.ini")
    conf.jinja("/application.ini", os.environ, base + "configs/application.ini")
    conf.jinja("/php.ini", os.environ, "/usr/local/etc/php/conf.d/rainloop.ini")

else:
  os.system("touch /var/www/html/MULTIPLY")
  os.system("chown www-data:www-data /var/www/html/MULTIPLY")

os.system("chown -R www-data:www-data /data")

os.execv("/usr/local/bin/apache2-foreground", ["apache2-foreground"])
