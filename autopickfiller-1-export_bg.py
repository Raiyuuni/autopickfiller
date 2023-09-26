#! /usr/bin/env python

import inkex
import copy
import os
import subprocess
import sys

class AutoPickFiller_ExportBG(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--tab", type=str) # This needs to be added just because the notebook parameter exists. Boring.
        pars.add_argument("--bg_layer", type=str, default="Layer 1")
    
    def export_bg(self, bg_label, svg_dest):
        doc = copy.deepcopy(self.document)
        for layer in doc.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS):
            label = layer.attrib["{%s}label" % layer.nsmap['inkscape']]
            layer.attrib["style"] = "display:none" # Hide all layers...
            if (label == bg_label): # ... unless it is the background layer.
                layer.attrib["style"] = "display:inline"
        
        doc.write(svg_dest)
        
    def effect(self):
        bg_label = self.options.bg_layer        
        svg_dest = os.path.join(self.svg_path(), self.svg.name)[:-4]+"temp.svg"
        self.export_bg(bg_label, svg_dest)
        inkscape_path = sys.executable[:-11]+"inkscape.exe" # In a default (Windows) installation, Python is stored in the same folder as Inkscape.
        
        if os.path.exists(inkscape_path): # If possible, do not require environment variables.
            command = '"%s" --export-type="png" "%s" --export-filename "%s\\apf_tempbg.png"' % (inkscape_path, svg_dest, self.svg_path())
        else:
            command = 'inkscape --export-type="png" "%s" --export-filename "%s\\apf_tempbg.png"' % (svg_dest, self.svg_path())

        p = subprocess.Popen(command)
        
        self.msg("============================================")
        self.msg("IF THE ONLY EXCEPTION BELOW IS \"ResourceWarning\", IGNORE IT.")
        self.msg("============================================")
        
if __name__ == '__main__':
    AutoPickFiller_ExportBG().run()