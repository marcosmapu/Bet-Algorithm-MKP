import logging
import sys
from logging import FileHandler
from logging import Formatter

LOG_FORMAT = ("%(message)s")
LOG_LEVEL = logging.INFO

# messaging logger
RESULTADOS_LOG_FILE = str(sys.argv[1])+".log"


resultados_logger = logging.getLogger(str(sys.argv[1]))
resultados_logger.setLevel(LOG_LEVEL)
resultados_logger_file_handler = FileHandler(RESULTADOS_LOG_FILE)
resultados_logger_file_handler.setLevel(LOG_LEVEL)
resultados_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
resultados_logger.addHandler(resultados_logger_file_handler)

# payments logger
PROGRESSO_LOG_FILE = str(sys.argv[1])+"_progresso_rodadas.log"
progresso_logger = logging.getLogger(str(sys.argv[1])+"_progresso_rodadas")

progresso_logger.setLevel(LOG_LEVEL)
progresso_file_handler = FileHandler(PROGRESSO_LOG_FILE)
progresso_file_handler.setLevel(LOG_LEVEL)
progresso_file_handler.setFormatter(Formatter(LOG_FORMAT))
progresso_logger.addHandler(progresso_file_handler)

#1 FASE

RESULTADOS_1FASE_LOG_FILE = str(sys.argv[1])+"_1fase.log"


resultados_1fase_logger = logging.getLogger(str(sys.argv[1])+"_1fase")
resultados_1fase_logger.setLevel(LOG_LEVEL)
resultados_1fase_logger_file_handler = FileHandler(RESULTADOS_1FASE_LOG_FILE)
resultados_1fase_logger_file_handler.setLevel(LOG_LEVEL)
resultados_1fase_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
resultados_1fase_logger.addHandler(resultados_1fase_logger_file_handler)




PROGRESSO_1FASE_LOG_FILE = str(sys.argv[1])+"_progresso_rodadas_1fase.log"
progresso_1fase_logger = logging.getLogger(str(sys.argv[1])+"_progresso_rodadas_1fase")

progresso_1fase_logger.setLevel(LOG_LEVEL)
progresso_1fase_file_handler = FileHandler(PROGRESSO_1FASE_LOG_FILE)
progresso_1fase_file_handler.setLevel(LOG_LEVEL)
progresso_1fase_file_handler.setFormatter(Formatter(LOG_FORMAT))
progresso_1fase_logger.addHandler(progresso_1fase_file_handler)


#ANDRE

OUTPUT_ANDRE_LOG_FILE = "output_" + str(sys.argv[1]) + ".log"
output_andre_logger = logging.getLogger("output_" + str(sys.argv[1]))
output_andre_logger.setLevel(LOG_LEVEL)
output_andre_file_handler = FileHandler(OUTPUT_ANDRE_LOG_FILE)
output_andre_file_handler.setFormatter(Formatter(LOG_FORMAT))
output_andre_logger.addHandler(output_andre_file_handler)