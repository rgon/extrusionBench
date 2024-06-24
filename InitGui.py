import os
import FreeCADGui as Gui
import FreeCAD as App


class ExtrusionWorkbench(Gui.Workbench):
    """
    class which gets initiated at startup of the gui
    """
    MenuText = "Extrusion Workbench"
    ToolTip = "Simple Workbench for creating parametric aluminum extrusion objects"
    Icon = "./resources/icons/wb_icon.svg"
    toolbox = []

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        """
        This function is called at the first activation of the workbench.
        here is the place to import all the commands
        """
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
