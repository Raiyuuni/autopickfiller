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



![](https://github.com/Raiyuuni/autopickfiller/assets/65428607/3f5df713-8d14-4834-ab3e-dc7f74bd4763)

When the first script is complete, a new window will pop up reporting a ResourceWarning exception. Dismiss it and close the extension's window.
- The script uses an Inkscape subprocess to export the background layer. The exception happens because the script does not wait for (and ends before) the subprocess.

You can check 




## Limitations
test

## Credits
- regebro, author of [svg.path](https://github.com/jespino/inkscape-export-layers)
- jespino, author of [Inkscape Export Layers](https://github.com/jespino/inkscape-export-layers)
