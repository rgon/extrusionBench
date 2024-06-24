import FreeCADGui as Gui
import FreeCAD as App
import Part

from config import RESOURCE_FILE_DICT, PROFILE_BASE_DIR, PROFILE_BREP_BASE_DIR

EXTRUSION_OPTIONS_GROUP = 'Extrusion'
PROPERTY_READONLY = 1

class ExtrusionObject:
    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyLength", "Length", EXTRUSION_OPTIONS_GROUP, "Length of the extrusion")
        
        # Dropdown list of available extrusion standards
        obj.addProperty("App::PropertyEnumeration", "Standard", EXTRUSION_OPTIONS_GROUP, "Extrusion standard")
        # Generate Standards from the resource file dict
        obj.Standard = list(RESOURCE_FILE_DICT.keys())
        # '20x20','20x40', '20x60', '20x80',
        #                 '30x30','30x60','30x90',
        #                 '40x40','40x80'

        # Add read only property of width and depth
        obj.addProperty("App::PropertyLength", "Width", "", "Width of the extrusion", PROPERTY_READONLY)
        obj.addProperty("App::PropertyLength", "Depth", "", "Depth of the extrusion", PROPERTY_READONLY)

        # Default Values
        obj.Length = 100.0
        obj.Standard = '20x20'

    def areValuesvalid(self, obj)->bool:
        if obj.Length <= 0:
            return False
        return True

    def execute(self, obj):
        '''Called on document recompute'''
        import FreeCAD as App
        import Part

        if (not self.areValuesvalid(obj)):
            return
        

        width = int(obj.Standard.split('x')[0])
        depth = int(obj.Standard.split('x')[1])

        obj.Width = width
        obj.Depth = depth

        def createUnknownStandard():
            # We create 4 points for the 4 corners:
            v1 = App.Vector(0, 0, 0)
            v2 = App.Vector(width, 0, 0)
            v3 = App.Vector(width,depth, 0)
            v4 = App.Vector(0, depth, 0)

            # We create 4 edges:
            e1 = Part.LineSegment(v1, v2).toShape()
            e2 = Part.LineSegment(v2, v3).toShape()
            e3 = Part.LineSegment(v3, v4).toShape()
            e4 = Part.LineSegment(v4, v1).toShape()

            # We create a face:
            f = Part.Face(Part.Wire([e1, e2, e3, e4]))

            return f

        f = None
        if obj.Standard in RESOURCE_FILE_DICT:
            # Import the standard profile resource sketch as a face
            resource = RESOURCE_FILE_DICT[obj.Standard].replace(PROFILE_BASE_DIR, PROFILE_BREP_BASE_DIR).replace('.stp', '.brp')
            s = Part.read(resource)
            
            # help(s)
            f = s.Faces[0]

        # if (obj.Standard == '20x20'):
        #     # Import the standard profile resource sketch as a face
        #     # BRP files can be generated by extracting a FCSTD file and copying the Sketch.Shape.brp file
        #     resource = 'resources/profiles/20x20.brp'
        #     s = Part.read(resource)

        #     # resource = 'resources/profiles/20x20.FCStd'
        #     # resourcePart = App.open(resource, True)
        #     # s = resourcePart.Sketch.Shape

        #     #         App.ActiveDocument.Sketch.setDatum(7,App.Units.Quantity(str(ylen) + " mm")) # set Y length -- this is the 7th constraint of the "Sketch" sketch
        #     # s.recompute()
            
        #     # Results in no top nor bottom face
        #     # f = s.Shape

        #     # Close the part shape into a face
        #     f = Part.Face(s.Wires)
        else:
            f = createUnknownStandard()

        e = f.extrude(App.Vector(0, 0, obj.Length))

        # All shapes have a Placement too. We give our shape the value of the placement
        # set by the user. This will move/rotate the face automatically.
        e.Placement = obj.Placement

        # All done, we can attribute our shape to the object!
        obj.Shape = e


class AddExtrusionStandard():
    """Add New Standard Extrusion"""

    def GetResources(self):
        return {"Pixmap"  : "./resources/icons/add_extrusion.svg",
                "Accel"   : "Shift+N", # a default shortcut (optional)
                "MenuText": "Create Aluminium Extrusion",
                "ToolTip" : "Create a new parametric aluminium extrusion object"}

    def Activated(self):
        """Do something here"""
        App.Console.PrintMessage("Adding Extrusion!\n")

        doc = App.activeDocument()

        # create extrusionObject and add to doc
        extrusionObject = doc.addObject("Part::FeaturePython", "Extrusion")
        ExtrusionObject(extrusionObject)
        extrusionObject.ViewObject.Proxy = 0 # This is mandatory unless we code the ViewProvider too.

        doc.recompute()

        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

Gui.addCommand("extrusion_standardNew", AddExtrusionStandard())