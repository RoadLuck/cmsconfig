# CMSconfig
  Code by: Road Luck in Python 3.6.5
  
# Descripción:
Script en python creado con el fin de automatizar el proceso de configurar la ip del servidor de bases de datos de distintas CMS existentes en el mercado. Tales como:
    Wordpress
    Joomla
    Prestashop1.6
    Prestashop1.7
    Moodle
# Uso:
Id CSM: Wordpress: 1, Joomla: 2, Prestashop1.6: 3, Prestashop1.7: 4, Moodle: 5
  
    python3 cmsconfig.py --cms <id_cms> --nip <new_ip_host> --oip <old_ip_host>
  
# Ejemplos
    python3 cmsconfig.py --cms 1 --nip 10.0.1.2 --oip localhost
    python3 cmsconfig.py --cms 5 --oip localhost
