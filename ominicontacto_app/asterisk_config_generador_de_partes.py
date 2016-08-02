# -*- coding: utf-8 -*-

"""
Genera archivos de configuración para Asterisk: dialplan y queues.
"""

from __future__ import unicode_literals

import os
import pprint

from django.conf import settings
from ominicontacto_app.errors import OmlError
from ominicontacto_app.models import Queue
import logging as _logging


logger = _logging.getLogger(__name__)


class NoSePuedeCrearDialplanError(OmlError):
    """Indica que no se pudo crear el dialplan."""
    pass


class GeneradorDePedazo(object):
    """Generador de pedazo generico"""

    def get_template(self):
        raise(NotImplementedError())

    def get_parametros(self):
        raise(NotImplementedError())

    def _reportar_key_error(self):
        try:
            logger.exception("Clase: %s.\nTemplate:\n%s\n Params: %s",
                             str(self.__class__),
                             self.get_template(),
                             pprint.pformat(self.get_parametros()))
        except:
            pass

    def generar_pedazo(self):
        template = self.get_template()
        template = "\n".join(t.strip() for t in template.splitlines())
        try:
            return template.format(**self.get_parametros())
        except KeyError:
            self._reportar_key_error()
            raise


#==============================================================================
# Failed
#==============================================================================


class GeneradorDePedazoDeDialplanParaFailed(GeneradorDePedazo):
    """Interfaz / Clase abstracta para generar el pedazo de dialplan
    fallido para una campana.
    """

    def __init__(self, parametros):
        self._parametros = parametros


class GeneradorParaFailed(GeneradorDePedazoDeDialplanParaFailed):

    def get_template(self):
        return """

        ;----------------------------------------------------------------------
        ; TEMPLATE_FAILED-{oml_queue_name}
        ;   Autogenerado {date}
        ;
        ; La generacion de configuracion para la queue {oml_queue_name}
        ;   a fallado.
        ;
        ; {traceback_lines}
        ;
        ;----------------------------------------------------------------------


        """

    def get_parametros(self):
        return self._parametros


# ########################################################################### #
# Factory para las Queue.

class GeneradorDePedazoDeQueueFactory(object):

    def crear_generador_para_queue(self, parametros):
        return GeneradorParaQueue(parametros)

    def crear_generador_para_failed(self, parametros):
        return GeneradorParaFailed(parametros)


#==============================================================================
# Queue
#==============================================================================


class GeneradorDePedazoDeQueue(GeneradorDePedazo):
    """Interfaz / Clase abstracta para generar el pedazo de queue para una
    campana.
    """

    def __init__(self, parametros):
        self._parametros = parametros


class GeneradorParaQueue(GeneradorDePedazoDeQueue):

    def get_template(self):
        return """

        ;----------------------------------------------------------------------
        ; TEMPLATE_DIALPLAN_START_QUEUE-{oml_queue_name}
        ;   Autogenerado {date}
        ;----------------------------------------------------------------------

        exten => {oml_queue_id_asterisk},1,NoOp(cola {oml_queue_name})
        same => n,Set(__MONITOR_FILENAME=/var/spool/asterisk/monitor/q${{EXTEN}}-${{STRFTIME(${{EPOCH}},,%Y%m%d-%H%M%S)}}-${{UNIQUEID}})
        same => n,Set(__MONITOR_EXEC=/usr/local/parselog/update_mix_mixmonitor.pl ^{{}}UNIQUEID}} ^{{}}MIXMONITOR_FILENAME}})
        same => n,SIPAddHeader(Origin:IN)
        same => n,SIPAddHeader(IDCliente:${{IDCliente}})
        same => n,Queue({oml_queue_name},{oml_queue_wait},tT)
        """

    def get_parametros(self):
        return self._parametros