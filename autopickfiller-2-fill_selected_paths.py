#! /usr/bin/env python

import inkex
import PIL
from PIL import Image
import os
import re

class AutoPickFiller_FillSelectedPaths(inkex.EffectExtension):       
    def _path_splitter(self,path):
        my_data = re.split(r"([MmLlHhVvZz])",path)
            # Parentheses: keep the separators in the output list
            # Brackets: match any of the characters within
        del my_data[0] # Remove empty strings
        del my_data[-1]
        
        tokens = []
        for x in my_data:
            x = x.strip()
            if x in "MmLlHhVv":
                token = (x,) # Command waiting for an argument
            
            elif x not in "Zz":
                token += (x,) # Add argument
                tokens.append(token)
  
        return tokens
        
    def _token_unchainer(self,tokens): # This version converts Mm commands (explicit and implicit) into Ll   
        newTokens = []
        for token in tokens:
            if " " not in token[1]: # Prepare individual tokens
                if token[0] == "M":
                    newToken = ("L", token[1])
        
                elif token[0] == "m":
                    newToken = ("l", token[1])
                
                else:
                    newToken = token
        
                newTokens.append(newToken)
            
            else: # Break down coordinate chains into tokens
                args = token[1].split() # Split by whitespaces
                for arg in args:
                    if token[0] == "M":
                        tokenLink = ("L", arg)
                    
                    elif token[0] == "m":
                        tokenLink = ("l", arg)
                    
                    else:
                        tokenLink = (token[0], arg)
                    
                    newTokens.append(tokenLink)
                    
        return newTokens

    def _convert_coordinates(self,tokens):
        tokenList = []
        for token in tokens:
            tokenXY = []
            tokenCrumbs = token[1].split(",") # Split coordinate pairs into individual strings
            for i in range(len(tokenCrumbs)):
                tokenCrumbs[i] = float(tokenCrumbs[i]) # Convert strings to numbers
                
            tokenList.append([token[0],tokenCrumbs])
        
        return tokenList
        
    def _parse_nodes(self,tokens):
        nodeList = []
        for token in tokens:
            command = token[0]
            relative = command.islower() # Test whether the coordinates are absolute or relative
            command = command.upper()
            index = tokens.index(token)
        
            if command == "L":
                pos = token[1]
                if (relative and not index == 0):
                    pos = [x + y for x, y in zip(pos, current_pos)]
                current_pos = pos
        
            elif command == "H":
                hpos = token[1][0]
                if (relative and not index == 0):
                    hpos += current_pos[0]
                current_pos = [hpos,current_pos[1]]
        
            elif command == "V":
                vpos = token[1][0]
                if (relative and not index == 0):
                    vpos += current_pos[1]
                current_pos = [current_pos[0],vpos]
        
            nodeList.append(current_pos)
        
        return nodeList
        
    def effect(self):
        svg_dest = os.path.join(self.svg_path(), self.svg.name)[:-4]+"temp.svg"
        png_dest = os.path.join(self.svg_path(), "apf_tempbg.png")
        
        im = Image.open(png_dest)
        
        x0 = self.svg.get_viewbox()[0] # Top left coordinates of the viewBox (absolute units)
        y0 = self.svg.get_viewbox()[1]
        scale = self.svg.inkscape_scale # Ratio between viewBox width and page width (pixels)

        for elem in self.svg.selection.filter(inkex.PathElement): # Loop for all paths in the selection
            path_data = elem.get("d")     
            
            tokens = self._path_splitter(path_data)
            tokens2 = self._token_unchainer(tokens)
            tokens3 = self._convert_coordinates(tokens2)
            nodes = self._parse_nodes(tokens3)
            self.msg(tokens)
            self.msg(tokens2)
            self.msg(tokens3)
            self.msg(nodes)
            
            x = []
            y = []
            for node in nodes:
                x.append(node[0])
                y.append(node[1])
              
            xm = sum(x)/len(x) # Centroid coordinates - viewBox absolute units
            ym = sum(y)/len(y)
            xp = round((xm - x0) * scale) # Centroid coordinates - pixels. Rounded to use in getpixel.
            yp = round((ym - y0) * scale)
            
            width = self.svg.viewport_width
            height = self.svg.viewport_height
            
            if xp < 0: # Check if the sample point is inside the image's boundaries
                xp = 0
            elif xp >= width: 
                xp = width - 1
            
            if yp < 0:
                yp = 0
            elif yp >= height:
                yp = height - 1
            
            r, g, b, a = im.getpixel((xp,yp)) # outputs RGBA values
            color = "rgb(%s, %s, %s)" % (r, g, b) # convert to RGB
            
            elem.style['fill'] = color
            elem.style['fill-opacity'] = 1
            elem.style['stroke-opacity'] = 0
            elem.style['opacity'] = 1
        
        im.close()
        os.remove(svg_dest) # Remove temporary files
        os.remove(png_dest)
        
if __name__ == '__main__':
    AutoPickFiller_FillSelectedPaths().run()