from qgis.core import QgsProcessing, QgsProcessingAlgorithm, QgsProcessingMultiStepFeedback, QgsProcessingParameterMultipleLayers, QgsProcessingParameterString
from qgis.core import QgsProcessingParameterVectorDestination, QgsProcessingParameterRasterDestination, QgsProcessingParameterFileDestination
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QCoreApplication
import processing
from . import resources

def tr(message):
    return QCoreApplication.translate('PyRocessing', message)

class PythonAlgorithm(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterMultipleLayers('inputs', tr("Inputs")+" (variable : inputs)", layerType=QgsProcessing.TypeMapLayer, defaultValue=None, optional=True))
        self.addParameter(QgsProcessingParameterString('script', tr('Python script'), multiLine=True, defaultValue=''))
        self.addParameter(QgsProcessingParameterVectorDestination('vector_output', tr("Vector output")+" (variable : vector_output)", type = QgsProcessing.TypeVectorAnyGeometry, createByDefault = False, optional = True))
        self.addParameter(QgsProcessingParameterRasterDestination('raster_output', tr("Raster output")+" (variable : raster_output)", createByDefault = False, optional = True))
        self.addParameter(QgsProcessingParameterFileDestination('file_output', tr("File output")+" (variable : file_output)", createByDefault = False, optional = True))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        results = {}
            
        inputs = self.parameterAsLayerList(parameters, 'inputs', context)
        
        vector_output = self.parameterAsOutputLayer(parameters, 'vector_output', context)
        raster_output = self.parameterAsOutputLayer(parameters, 'raster_output', context)
        file_output = self.parameterAsFileOutput(parameters, 'file_output', context)
            
        exec(parameters['script'])

        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        
        results['vector_output'] = vector_output
        results['raster_output'] = raster_output
        results['file_output'] = file_output
        
        return results

    def name(self):
        return 'pythonalgorithm'

    def displayName(self):
        return tr('Execute Python script')

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return PythonAlgorithm()

    def icon(self):
        return QIcon(':/plugins/pyrocessing/icon.svg')
