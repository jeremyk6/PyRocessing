from qgis.core import QgsApplication, QgsProcessingProvider, QgsProcessingModelAlgorithm
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QTranslator, QSettings, QCoreApplication, QLocale, qVersion
from .pythonalgorithm import PythonAlgorithm
import os
from . import resources

class Provider(QgsProcessingProvider):

    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(PythonAlgorithm())
    
    def id(self, *args, **kwargs):
        return 'pyrocessing'
    
    def name(self, *args, **kwargs):
    
        return 'PyRocessing'
    
    def icon(self):
        return QIcon(':/plugins/pyrocessing/icon.svg')


class PyRocessing():

    def __init__(self):
        overrideLocale = QSettings().value("locale/overrideFlag", False, type=bool)
        if not overrideLocale: locale = QLocale.system().name()
        else:
            locale = QSettings().value("locale/userLocale", "")
            if locale.__class__.__name__=='QVariant': locale= 'en'
        locale = locale[0:2]
        locale_path = os.path.join(
            os.path.dirname(__file__),
            'i18n',
            '{}.qm'.format(locale))

        self.translator = None
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.provider = None

    def initProcessing(self):
        self.provider = Provider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)