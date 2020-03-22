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
    dir_list = []

    for dirpath, dirnames, filenames in os.walk(ruta_app):
        for filename in filenames:
            if file_name in filename.lower():
                Count = Count+1
                dir_list.append(dirpath)
    return dir_list

def modify_file(dir_list, file_name, line_conf, index_conf):
    """
Esta funcion se encarga de modificar los archivos encontrados
en los directorios en donde se ubica la cms.
    """
    global Count
    global Error
    for directory in dir_list:
        try:
            lines = open(os.path.join(directory)+'/'+file_name, 'r').readlines()
            lines[index_conf] = line_conf
            out = open(os.path.join(directory)+'/'+file_name, 'w')
            out.writelines(lines)
            out.close()
            logging.info('Modify File: '+directory+'/'+file_name)
            return True
        except:
            Count = Count-1
            Error = Error + 1
            #print("File not Found: ",os.path.join(directory)+'/'+file_name)
            logging.error('File not Found:'+directory+'/'+file_name)
            continue
    


def main():
    welcome_message()
    parser = optparse.OptionParser(bcolors.ENDC+'cmsconfig.py'+' --cms <numero_identificador_cms> --ip <host_edit>')
    parser.add_option('--cms', dest='idCms', type='int', help='1-Wordpress, 2-Joomla, 3-Prestashop1.6, 4-Prestashop1.7, 5-Moodle')
    parser.add_option('--ip', dest='hostIp', type='string',default="localhost", help='Especifique la ip deseada Default:localhost')
    (options, args) = parser.parse_args()

    cms_id = options.idCms
    ip_host = options.hostIp

    if cms_id == None or ip_host==None:
        print(parser.usage)
        exit(0)
    
    if cms_id==1: #Wordpress
        file_name = "wp-config.php"
        line_conf = "define('DB_HOST', '"+ip_host+"');\n"
        index_conf = 31
        dir_list = found_dirs(file_name)
        logging.basicConfig(filename="WordpressFile.log", level=logging.INFO)
        check = modify_file(dir_list, file_name, line_conf, index_conf)
   
    elif cms_id==2: #Joomla
        file_name = "configuration.php"
        line_conf = "\tpublic $host = '"+ip_host+"';\n"
        index_conf = 15
        dir_list = found_dirs(file_name)
        logging.basicConfig(filename="JoomlaFile.log", level=logging.INFO)
        check = modify_file(dir_list, file_name, line_conf, index_conf)


    elif cms_id==3: #Prestashop1.6
        file_name = "settings.inc.php"
        line_conf = "define('_DB_SERVER_', '"+ip_host+"');\n"
        index_conf = 1
        dir_list = found_dirs(file_name)
        logging.basicConfig(filename="Prestashop1.6File.log", level=logging.INFO)
        check = modify_file(dir_list, file_name, line_conf, index_conf)
    
    elif cms_id==4: #Prestashop1.7
        file_name = "parameters.php"
        line_conf = "    'database_host' => '"+ip_host+"',\n"
        index_conf = 3
        dir_list = found_dirs(file_name)
        logging.basicConfig(filename="Prestashop1.7File.log", level=logging.INFO)
        check = modify_file(dir_list, file_name, line_conf, index_conf)
    
    elif cms_id==5:
        file_name = "config.php"
        line_conf = "$CFG->dbhost    = '"+ip_host+"';\n"
        index_conf = 8
        dir_list = found_dirs(file_name)
        logging.basicConfig(filename="MoodleFile.log", level=logging.INFO)
        check = modify_file(dir_list, file_name, line_conf, index_conf)
        
    if check:
        if Count > 1:
            print(bcolors.OKGREEN+"[*] "+str(Count)+" archivos modificados correctamente.")
        else:
            print(bcolors.OKGREEN+"[*] "+str(Count)+" archivo modificado correctamente.")
        print(bcolors.FAIL+"[!] Archivos no modificados: ", str(Error))
if __name__ == '__main__':
    main()