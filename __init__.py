bl_info = {
    "name": "Quantum Batch Export",
    "description": "Exports internal images with a certain prefix, into a given directory",
    "author": "Saphi",
    "version": (0, 0, 2),
    "blender": (4, 2, 0),
    "category": "Output",
    "location": "Output > Quantum Export",
    "doc_url": "https://github.com/SaphiBlue/QExport"
}

import bpy
import os

def QExportMain(context):
    props = context.scene.qexport
    for image in bpy.data.images:
        if(image.name.startswith(props.prefix)):
            try:
                tempImage = image.copy()
                tempImage.file_format = 'PNG'
                tempImage.filepath = os.path.join(props.outDir, image.name + ".png")
                tempImage.save()
                bpy.data.images.remove(tempImage)
            except:
                print("Unable to export" + image.name) 


class QExportOperator(bpy.types.Operator):
    bl_idname = "qexport.export"
    bl_label = "Export"

    def execute(self, context):
        QExportMain(context)
        return {'FINISHED'}


class QExportGlobalProps(bpy.types.PropertyGroup):
    outDir: bpy.props.StringProperty(
        name = "Output",
        description = "Name of output directory",
        default = "//Baked/",
        subtype = 'DIR_PATH',)
    prefix: bpy.props.StringProperty(
        name = "Prefix",
        description = "Prefix",
        default = "Baked",)

class QExportPanel(bpy.types.Panel):

    bl_label = "Quantum Export"
    bl_idname = "QEXPORT_PT_Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"



    def draw(self, context):
        
        props = context.scene.qexport
        
        layout = self.layout

        scene = context.scene

        # Create a simple row.
        row = layout.row()                
        row.prop(props, "outDir")
        row = layout.row()
        row.prop(props, "prefix")
        row = layout.row()
        
        row.operator("qexport.export")

def register():
    bpy.utils.register_class(QExportPanel)
    
    bpy.utils.register_class(QExportGlobalProps)
    
    bpy.utils.register_class(QExportOperator)

    bpy.types.Scene.qexport = bpy.props.PointerProperty(type = QExportGlobalProps)

def unregister():
    bpy.utils.unregister_class(QExportPanel)

    bpy.utils.unregister_class(QExportGlobalProps)
    
    bpy.utils.unregister_class(QExportOperator)
    
    del bpy.types.Scene.qexport


if __name__ == "__main__":
    register()
