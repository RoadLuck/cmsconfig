import os
import optparse
import logging
import tempfile
"""
Nota del programador:
    Este script solo es funcional si y solo si los archivos a modificar
    no fueron intervenidos manteniendo su orden y forma por defecto.
"""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[5;37;40m'

def welcome_message():
    print(bcolors.HEADER +"   _____ __  __  _____                  __ _       ")
    print("  / ____|  \/  |/ ____|                / _(_)      ")
    print(" | |    | \  / | (___   ___ ___  _ __ | |_ _  __ _ ")
    print(" | |    | |\/| |\___ \ / __/ _ \| '_ \|  _| |/ _` |")
    print(" | |____| |  | |____) | (_| (_) | | | | | | | (_| |")
    print("  \_____|_|  |_|_____/ \___\___/|_| |_|_| |_|\__, |")
    print("                                              __/ |")
    print("                                             |___/ ")
    print(bcolors.WARNING+"             Code By: Road Luck")

Count = 0
Error = 0
def found_dirs(file_name):
    """
Esta funcion busca los directorios que contienen el archivo de configuracion
y retorna un diccionario con el nombre de estos
    """
    global Count
    ruta_app = os.getcwd()
    dir_list = tempfile.TemporaryFile(mode='w+t')
    dir_list.seek(0)
    for dirpath, dirnames, filenames in os.walk(ruta_app):
        for filename in filenames:
            if file_name in filename.lower():
                Count = Count+1
                dir_list.write(dirpath+'\n')

    return dir_list

def modify_file(dir_list, file_name, line_conf, line_found):
    """
Esta funcion se encarga de modificar los archivos encontrados
en los directorios en donde se ubica la cms.
    """
    global Count
    global Error
    dir_list.seek(0)
 
    for directory in dir_list:
        try:
            dir_name = directory.rstrip()+'/'+file_name
            lines = open(dir_name, 'r').readlines()
            index_conf = lines.index(line_found)
            lines[index_conf] = line_conf
            out = open(dir_name, 'w')
            out.writelines(lines)
            out.close()
            logging.info('Modify File: '+ dir_name)
        except:
            Count = Count-1
            Error = Error + 1
            logging.error('File not Found:'+dir_name)
            continue
    return True


def main():
    welcome_message()
    parser = optparse.OptionParser(bcolors.ENDC+'cmsconfig.py'+' --cms <numero_identificador_cms> --ip <host_edit>')
    parser.add_option('--cms', dest='idCms', type='int', help='1-Wordpress, 2-Joomla, 3-Prestashop1.6, 4-Prestashop1.7, 5-Moodle')
    parser.add_option('--nip', dest='newhostIp', type='string',default="localhost", help='Especifique la ip nueva deseada Default:localhost')
    parser.add_option('--oip', dest='oldHostIp', type='string',default="localhost", help='Especifique la ip antigua')
    (options, args) = parser.parse_args()

    cms_id = options.idCms
    ip_host = options.newhostIp
    old_ip_host = options.oldHostIp

    if cms_id == None or ip_host==None:
        print(parser.usage)
        exit(0)
    
    if cms_id==1: #Wordpress
        file_name = "wp-config.php"
        line_conf = "define('DB_HOST', '"+ip_host+"');\n"
        line_found = "define('DB_HOST', '"+old_ip_host+"');\n"
        dir_list = found_dirs(file_name)
        logging.basicConfig(filename="WordpressFile.log", level=logging.INFO)
        check = modify_file(dir_list, file_name, line_conf, line_found)
        
   
    elif cms_id==2: #Joomla
        file_name = "configuration.php"
        line_conf = "\tpublic $host = '"+ip_host+"';\n"
        line_found = "\tpublic $host = '"+old_ip_host+"';\n"
        dir_list = found_dirs(file_name)
        logging.basicConfig(filename="JoomlaFile.log", level=logging.INFO)
        check = modify_file(dir_list, file_name, line_conf, line_found)


    elif cms_id==3: #Prestashop1.6
        file_name = "settings.inc.php"
        line_conf = "define('_DB_SERVER_', '"+ip_host+"');\n"
        line_found = "define('_DB_SERVER_', '"+old_ip_host+"');\n"
        dir_list = found_dirs(file_name)
        logging.basicConfig(filename="Prestashop1.6File.log", level=logging.INFO)
        check = modify_file(dir_list, file_name, line_conf, line_found)
    
    elif cms_id==4: #Prestashop1.7
        file_name = "parameters.php"
        line_conf = "    'database_host' => '"+ip_host+"',\n"
        line_found = "    'database_host' => '"+old_ip_host+"',\n"
        dir_list = found_dirs(file_name)
        logging.basicConfig(filename="Prestashop1.7File.log", level=logging.INFO)
        check = modify_file(dir_list, file_name, line_conf, line_found)
    
    elif cms_id==5:
        file_name = "config.php"
        line_conf = "$CFG->dbhost    = '"+ip_host+"';\n"
        line_found = "$CFG->dbhost    = '"+old_ip_host+"';\n"
        dir_list = found_dirs(file_name)
        logging.basicConfig(filename="MoodleFile.log", level=logging.INFO)
        check = modify_file(dir_list, file_name, line_conf, index_conf)
        
    if check:
        if Count > 1:
            print(bcolors.OKGREEN+"[*] "+str(Count)+" archivos modificados correctamente.")
        else:
            print(bcolors.OKGREEN+"[*] "+str(Count)+" archivo modificado correctamente.")
    print(bcolors.FAIL+"[!] Archivos no modificados: ", str(Error))
    dir_list.close()
        
if __name__ == '__main__':
    main()