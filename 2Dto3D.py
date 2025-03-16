# #!/usr/bin/env python

# import vtk


# def main():

#     '''
#     A class holding colors and their names. 
#     '''
#     colors = vtk.vtkNamedColors()

#     dicom_dir= 'ct' #path to dcom image folder
#     iso_value = 1500 
#     if iso_value is None and dicom_dir is not None:
#         print('An ISO value is needed.')
#         return ()

#     volume = vtk.vtkImageData()
#     if dicom_dir is None:
#         pass

#     else:
#         reader = vtk.vtkDICOMImageReader()
#         reader.SetDirectoryName(dicom_dir)
#         reader.Update()
#         volume.DeepCopy(reader.GetOutput())

#     surface = vtk.vtkMarchingCubes()
#     surface.SetInputData(volume)
#     surface.ComputeNormalsOn()
#     surface.SetValue(0, iso_value)

#     renderer = vtk.vtkRenderer()
#     renderer.SetBackground(colors.GetColor3d('DarkSlateGray'))

#     render_window = vtk.vtkRenderWindow()
#     render_window.AddRenderer(renderer)
#     render_window.SetWindowName('MarchingCubes')

#     interactor = vtk.vtkRenderWindowInteractor()
#     interactor.SetRenderWindow(render_window)

#     mapper = vtk.vtkPolyDataMapper()
#     mapper.SetInputConnection(surface.GetOutputPort())
#     mapper.ScalarVisibilityOff()

#     actor = vtk.vtkActor()
#     actor.SetMapper(mapper)
#     actor.GetProperty().SetColor(colors.GetColor3d('MistyRose'))

#     renderer.AddActor(actor)

#     render_window.Render()
#     interactor.Start()




# if __name__ == '__main__':
#     main()


import vtk
import tkinter as tk
from tkinter import ttk

def main():
    '''
    A class holding colors and their names.
    '''
    colors = vtk.vtkNamedColors()

    dicom_dir = 'ct'  # Path to DICOM image folder
    iso_values = [500, 1000, 1500]  # Iso-values for different structures: muscle, brain, bone
    structure_colors = {
        'muscle': colors.GetColor3d('Tomato'),
        'brain': colors.GetColor3d('LightSteelBlue'),
        'skull': colors.GetColor3d('Wheat')
    }

    if dicom_dir is None:
        print('No DICOM directory provided.')
        return

    volume = vtk.vtkImageData()

    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(dicom_dir)
    reader.Update()
    volume.DeepCopy(reader.GetOutput())

    renderer = vtk.vtkRenderer()
    renderer.SetBackground(colors.GetColor3d('DarkSlateGray'))

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetWindowName('MarchingCubes')

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    actors = {}  # Dictionary to store actors for each structure

    # Loop through iso-values and create actors
    for iso_value in iso_values:
        surface = vtk.vtkMarchingCubes()
        surface.SetInputData(volume)
        surface.ComputeNormalsOn()
        surface.SetValue(0, iso_value)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(surface.GetOutputPort())
        mapper.ScalarVisibilityOff()

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Assign colors based on iso-value
        if iso_value == 500:  # Muscle/Soft tissues
            actor.GetProperty().SetColor(structure_colors['muscle'])
            actors['muscle'] = actor
        elif iso_value == 1000:  # Brain
            actor.GetProperty().SetColor(structure_colors['brain'])
            actors['brain'] = actor
        elif iso_value == 1500:  # Bone (Skull)
            actor.GetProperty().SetColor(structure_colors['skull'])
            actors['skull'] = actor

        # Initially add all actors to renderer
        renderer.AddActor(actor)

    # Function to toggle structure visibility based on button press
    def toggle_visibility(structure):
        if structure == 'all':
            for actor in actors.values():
                actor.SetVisibility(True)  # Show all actors
        else:
            for actor_name, actor in actors.items():
                actor.SetVisibility(True if actor_name == structure else False)
        render_window.Render()

    # Create the GUI
    root = tk.Tk()
    root.title("Structure Visibility")

    # Button to toggle skull visibility
    skull_button = ttk.Button(root, text="Show Skull", command=lambda: toggle_visibility('skull'))
    skull_button.pack(padx=10, pady=10)

    # Button to toggle muscle visibility
    muscle_button = ttk.Button(root, text="Show Muscle", command=lambda: toggle_visibility('muscle'))
    muscle_button.pack(padx=10, pady=10)

    # Button to toggle brain visibility
    brain_button = ttk.Button(root, text="Show Brain", command=lambda: toggle_visibility('brain'))
    brain_button.pack(padx=10, pady=10)

    # Button to show all structures
    all_button = ttk.Button(root, text="Show All", command=lambda: toggle_visibility('all'))
    all_button.pack(padx=10, pady=10)

    # Start the Tkinter window
    root.after(100, lambda: render_window.Render())  # Make sure the VTK window is rendered
    root.mainloop()

    # Start the interactor to display the VTK window
    interactor.Start()


if __name__ == '__main__':
    main()