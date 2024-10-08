import nuke

def hideViewerLines():
    for n in nuke.allNodes("Viewer"):
        n['hide_input'].setValue(1)