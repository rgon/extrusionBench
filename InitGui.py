import os
import FreeCADGui as Gui
import FreeCAD as App
import Part

from config import PROFILE_BASE_DIR, PROFILE_BREP_BASE_DIR

class ExtrusionWorkbench(Gui.Workbench):
    """
    class which gets initiated at startup of the gui
    """
    MenuText = "Extrusion Workbench"
    ToolTip = "Simple Workbench for creating parametric aluminum extrusion objects"
    Icon = "./resources/icons/wb_icon.svg"
    toolbox = []

    def _generateBrepFile(self, file:str, resultDir):
        s = Part.read(file)

        maxFacePointCount = 0
        maxFace = None

        # Find the face with the most points = base face
        for face in s.Faces:
            if len(face.Vertexes) > maxFacePointCount:
                maxFacePointCount = len(face.Vertexes)
                maxFace = face
        
        if maxFace is not None:
            maxFace.exportBrep(os.path.join(resultDir, os.path.basename(file).replace('.stp', '.brp')))

    def _generateBrepFiles(self, baseDir:str, resultDir:str):
        '''
        Iterates over the profile step files
        Opens them and gets their face with the most points -> base face
        Exports the base face to a brep file
        '''
        # ensure the result directory exists
        if not os.path.exists(resultDir):
            os.mkdir(resultDir)
        
        for root, dirs, files in os.walk(baseDir):
            for file in files:
                if file.endswith('.stp'):
                    self._generateBrepFile(os.path.join(root, file), resultDir)


    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        """
        This function is called at the first activation of the workbench.
        here is the place to import all the commands
        """
        from config import PROFILE_BASE_DIR, PROFILE_BREP_BASE_DIR

        # Add translations path
        # Gui.addLanguagePath(paths.TRANSLATIONSPATH)
        # Gui.updateLocale()

        # App.Console.PrintMessage("Switching to workbench_starterkit")

        self.appendToolbar("Tools", self.toolbox)
        self.appendMenu("Tools", self.toolbox)

        import extrusion_standardNew
        partCommands = [
            'extrusion_standardNew',
        ]
        # Create toolbars
        self.appendToolbar(
               'extrusion_parts',
               partCommands
               )

        # IF the BREP files are not present, generate them
        if not os.path.exists(PROFILE_BREP_BASE_DIR):
            App.Console.PrintMessage("Generating BREP files for profiles\n")
            os.mkdir(PROFILE_BREP_BASE_DIR)
            self._generateBrepFiles(f'{PROFILE_BASE_DIR}/dold', f'{PROFILE_BREP_BASE_DIR}/dold')


    def Activated(self):
        '''
        code which should be computed when a user switch to this workbench
        '''
        pass

    def Deactivated(self):
        '''
        code which should be computed when this workbench is deactivated
        '''
        pass


Gui.addWorkbench(ExtrusionWorkbench())
