# -*- coding: utf-8 -*-
# Terminal color definitions

class fg:
    BLACK   = '\033[30m'
    RED     = '\033[31m'
    GREEN   = '\033[32m'
    YELLOW  = '\033[33m'
    BLUE    = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN    = '\033[36m'
    WHITE   = '\033[37m'
    RESET   = '\033[39m'

class bg:
    BLACK   = '\033[40m'
    RED     = '\033[41m'
    GREEN   = '\033[42m'
    YELLOW  = '\033[43m'
    BLUE    = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN    = '\033[46m'
    WHITE   = '\033[47m'
    RESET   = '\033[49m'

class style:
    BRIGHT    = '\033[1m'
    DIM       = '\033[2m'
    NORMAL    = '\033[22m'
    RESET_ALL = '\033[0m'


comando_help = """
\033[1m\033[34m            +----------------------------------------------+ 
\033[1m\033[34m            | \033[1m\033[33mCOMANDI DISPONIBILI                          \033[1m\033[34m| 
\033[1m\033[34m            | \033[1m\033[33m                                             \033[1m\033[34m| 
\033[1m\033[34m            | \033[1m\033[33m!help - visualizza i comandi disponibili     \033[1m\033[34m|
\033[1m\033[34m            | \033[1m\033[33m!show - visualizza gli utenti connessi       \033[1m\033[34m|
\033[1m\033[34m            | \033[1m\033[33m!whoami - visualizza il proprio nickname     \033[1m\033[34m|              
\033[1m\033[34m            | \033[1m\033[33m!connect <nickname> - inizia una chat        \033[1m\033[34m| 
\033[1m\033[34m            | \033[1m\033[33m!disconnect - chiudi la chat in corso        \033[1m\033[34m| 
\033[1m\033[34m            | \033[1m\033[33m!quit - esci dal programma                   \033[1m\033[34m| 
\033[1m\033[34m            | \033[1m\033[33m                                             \033[1m\033[34m| 
\033[1m\033[34m            +----------------------------------------------+ """


messaggio_welcome = """

  _______   _______       _______                                         __              __   
 |   _   | |   _   |     |   _   | .--.--. .-----. .-----. .----. .----. |  |--. .---.-. |  |_ 
 |.  |___| |.  |___|     |   1___| |  |  | |  _  | |  -__| |   _| |  __| |     | |  _  | |   _|
 |.  |   | |.  |   |     |____   | |_____| |   __| |_____| |__|   |____| |__|__| |___._| |____|
 |:  1   | |:  1   |     |:  1   |         |__|                                                
 |::.. . | |::.. . |     |::.. . |                                                             
 `-------' `-------'     `-------'                                                             
                                                                                               

"""


messaggio_welcome_server = fg.BLUE + style.BRIGHT + """
                          )                
 (      (          (   ( /(  (      *   )  
 )\ )   )\ )       )\  )\()) )\   ` )  /(  
(()/(  (()/(     (((_)((_)((((_)(  ( )(_)) 
 /(_))_ /(_))_   )\___ _((_)\ _ )\(_(_())  
(_)) __(_)) __| ((/ __| || (_)_\(_)_   _|  
  | (_ | | (_ |  | (__| __ |/ _ \   | |    
   \___|  \___|   \___|_||_/_/ \_\  |_|    
                                           
 (            (                     (      
 )\ )         )\ )                  )\ )   
(()/(   (    (()/(   (   (    (    (()/(   
 /(_))  )\    /(_))  )\  )\   )\    /(_))  
(_))   ((_)  (_))   ((_)((_) ((_)  (_))    
/ __|  | __| | _ \  \ \ / /  | __| | _ \   
\__ \  | _|  |   /   \ V /   | _|  |   /   
|___/  |___| |_|_\    \_/    |___| |_|_\   
                                           
""" + fg.RESET + style.RESET_ALL


messaggio_registration_ok = """
    +---------------------------+
    |  \033[1m\033[33mRegistered successfully\033[34m\033[1m  |
    |      \033[1m\033[33mwith the server\033[34m\033[1m      |
    +---------------------------+
"""


messaggio_client_ready = """
        \\\\\\///
        / _  _\\
      (| (.)(.)|)
.---.OOOo--()--oOOO.---.
|                      |
|     \033[1m\033[33mClient Ready\033[34m\033[1m     |
|      CHAT IT UP      |
|                      |
'---.oooO--------------'
     (   )   Oooo.
      \ (    (   )
       \_)    ) /
             (_/
"""



comando_help2 = '\n' \
                '+------------------------------------------+\r\n' \
                '| COMANDI DISPONIBILI                      |\r\n' \
                '|                                          |\r\n' \
                '| !help - visualizza i comandi disponibili |\r\n' \
                '| !connect <nickname> - inizia una chat    |\r\n' \
                '| !disconnect - chiudi la chat in corso    |\r\n' \
                '| !quit - esci dal programma               |\r\n' \
                '|                                          |\r\n' \
                '+------------------------------------------+\r\n'

