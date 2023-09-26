# AutoPickFiller
**TL;DR:** An Inkscape extension for automatically filling closed paths with colors picked from a layer underneath.

## Full Description
AutoPickFiller is a tool that makes creating low poly art a little easier.

When a reference layer is used to set the paths' fill colors, picking and setting each color manually is a [highly](https://www.youtube.com/watch?v=7hcxuwDKo6I) [repetitive](https://www.youtube.com/watch?v=YdqndZ6T3MA) and error-prone task.

AutoPickFiller makes this process automatic by exporting the reference layer as an image and picking its colors using Python's pillow library.

## Installation
Download both .inx and .py files and move them to Inkscape's user extensions directory.

In Inkscape 1.3, the directory is listed at: `Edit > Preferences > System: User extensions`

Restart Inkscape to make the new extension available.

## Usage
AutoPickFiller is located in `Extensions > Color > Auto Pick Filler`, where it's broken down in two parts.

### 1 - Export Background
![](https://github.com/Raiyuuni/autopickfiller/assets/65428607/f0aacc7c-ec5a-4669-a92c-d5d266d533bd)
- Write down the name of your reference layer.
- If the field is left blank, the script assumes the reference layer is `Layer 1`.

---

![](https://github.com/Raiyuuni/autopickfiller/assets/65428607/3f5df713-8d14-4834-ab3e-dc7f74bd4763)

When the first script is complete, a new window will pop up reporting a ResourceWarning exception. Dismiss it and close the extension's window.
- The script uses an Inkscape subprocess to export the background layer. The exception happens because the script does not wait for (and ends before) the subprocess.

---

You can check whether the script has run successfully by going to your current file's directory. Two new files have been generated:

![](https://github.com/Raiyuuni/autopickfiller/assets/65428607/0ef86c3c-b4ee-4534-a7fb-7950e92d071c)
- A copy of your .svg file with all layers disabled, except for the reference layer
- A .png file of your reference layer

Both of these files will be automatically deleted by the next script.

---

### 2 - Fill Selected Paths
Select all paths to be recolored and run the second script. No further action is required.

<details> 
  <summary><b>Spoiler:</b> Here's an example of the expected changes.</summary>
   <img src="https://github.com/Raiyuuni/autopickfiller/assets/65428607/ec014430-3f00-4125-9664-8072c0f780e0"  width="60%" height="60%">
   <img src="https://github.com/Raiyuuni/autopickfiller/assets/65428607/60d683f0-b0ae-4be7-8b29-10014261e441"  width="60%" height="60%">
</details>

## Limitations
**Export Background**
- This script runs a simple test to locate `Inkscape.exe` using its built-in Python interpreter as a reference. In a default Windows 10 installation, both programs are located in the same folder.
- If `Inkscape.exe` isn't found, the script defaults to calling it via an environment variable, which may need to be manually set up.

**Fill Selected Paths**
- This script can only convert **paths** made out of **straight line segments**. It will not work on shapes, Bézier curves or arcs.

## Credits
- regebro, author of [svg.path](https://github.com/jespino/inkscape-export-layers)
- jespino, author of [Inkscape Export Layers](https://github.com/jespino/inkscape-export-layers)
