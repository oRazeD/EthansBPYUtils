# EthansBPYUtils
EthansBPYUtils is an incredibly loose collection of refined BPY-based functions and classes that perform; in most cases, frequently used operations. Some files such as materials.py are scraped directly from other add-ons and as such aren't currently usable in any capacity and only exist as an inlet for future ideas. This library will mainly be updated as I develop my other existing add-ons serving as a functionality bridge between them. EthansBPYUtils also comes with some example scripts that I've scraped from around online. You are welcome to use any of the code in this repo however you so wish under GPL licensing.

## How to Use
EthansBPYUtils is not loaded with [PIP](https://pypi.org/project/pip) or anything like that, but you can either add this library as a [Git Submodule](https://www.git-scm.com/book/en/v2/Git-Tools-Submodules) to your own repo or just manually download the files. If using the Git Submodule method, simply update the pointers to recieve updates from this repo as they are committed.

## My Development Setup
My IDE (coding software) of choice is [Visual Studio Code](https://code.visualstudio.com) with the Blender Development plugin installed for efficiently testing changed code. I also use [fake_bpy_module](https://github.com/nutti/fake-bpy-module) for proper syntax highlighting. Some resources I recommend for learning how to code within the API are listed in the following section.

## Random Development Resources
As far as utilities not specifically included in this repository, I will update this README to include any resources I find that I'd like share or explore myself in the future:

- [Scripting for Artists](https://studio.blender.org/training/scripting-for-artists) - If you already know Python but aren't familiar with BPY specifically, I always recommend Dr Sybrens tutorial series on developing add-ons. He offers clear and concise guidance on learning the API all the while being an extremely veteran coder giving useful code design advice along the way. You can also watch [this](https://youtu.be/mYrPqrFY7mA) talk for a more advanced but conference-like learning experience
- [BlenderShare/templates](https://github.com/BlenderShare/templates) - Code Snippets/Add-on Templates (seems a bit outdated)
- [blender_addon_updater](https://github.com/CGCookie/blender-addon-updater) - Tool that adds automatic add-on update functionality for end users
- [io_export_blend](https://github.com/CGCookie/io_export_blend) - Tool for exporting selections to a new blend file
- [download-directory](https://download-directory.github.io) - Simple web tool for directly downloading specific pages of a GitHub repo
- [ChatGPT](https://openai.com/blog/chatgpt) - Genuinely a good alternative resource for develepment assistance, warning that it will frequently give confidently incorrect responses and unless guided will often reference the pre-2.8 BPY Python API


## Add-ons I frequently use
While not entirely relevant to the purpose of this repository, I realized I have no location online where I share my favorite stuff. These add-ons are geared towards your average game artists toolkit being focused mostly on modeling, unwrapping, file handling, and rendering. I'll attempt to keep this list optimized and minimal as my workflow evolves. I will prioritize using only GitHub links and will substitute the paid only tools with Gumroad/Blender Market links where applicable:

### Generic
- [Screenshot Saver](https://github.com/oRazeD/ScreenshotSaver) - Made by Me!
- [Vertex Colors Plus](https://github.com/oRazeD/VertexColorsPlus) - Made by Me!
- [Bake to Vertex Color](https://3dbystedt.gumroad.com/l/zdgxg)
- Copy Attributes Menu - Built-in!
- Node Wrangler - Built-in!
- Edit Linked Library - Built-in!
- Material Utilities - Built-in!

### Generic Modeling
- [Pie Menus Plus](https://github.com/oRazeD/PieMenusPlus) - Made by Me!
- [Pie Menu Editor](https://roaoao.gumroad.com/l/pie_menu_editor)
- [Batch Ops](https://moth3r.gumroad.com/l/batchops)
- [Retopoflow](https://github.com/CGCookie/retopoflow)
- LoopTools - Built-in!
- BoolTool - Built-in!
- Extra Objects (Mesh & Curve) - Built-in!

### Mesh Manipulation
- [ReBevel](https://bartoszstyperek.gumroad.com/l/rebevel)
- [Rotate Face](https://bartoszstyperek.gumroad.com/l/rotate_face)
- [Slide Edge](https://kushiro.gumroad.com/l/oaykc)
- [Volume Preserving Smoothing](https://bartoszstyperek.gumroad.com/l/vol_smooth)
- [NGon Loop Select](https://amanbairwal.gumroad.com/l/NGonLoopSelect)
- [EdgeFlow](https://github.com/BenjaminSauder/EdgeFlow) - Not currently maintained
- [Hidesato Offset Edges](https://blenderartists.org/uploads/short-url/9Yp52n5oOiPPF5nKPHsZVo8XZJw.py) - DD link, not currently maintained
- [MACHIN3tools](https://machin3.gumroad.com/l/MACHIN3tools)
- [MESHMachine](https://machin3.gumroad.com/l/MESHmachine)
- [Hard Ops](https://masterxeon1001.gumroad.com/l/hardops)
- F2 - Built-in!

### UV Unwrapping
- [DreamUV](https://github.com/leukbaars/DreamUV)
- [UVToolkit](https://github.com/oRazeD/UVToolkit) - Not currently maintained, reuploaded by me
- [UVPackmaster 3](https://glukoz.gumroad.com/l/uvpackmaster3)
- [Texel Density Checker](https://github.com/mrven/Blender-Texel-Density-Checker)

### Rendering
- [Photographer](https://chafouin.gumroad.com/l/HPrCY)
- [Rotate HDRI](https://alexbel.gumroad.com/l/XQYEl) - Not currently maintained
- Copy Render Settings - Built-in!

### I/O
- [Better FBX](https://www.blendermarket.com/products/better-fbx-importer--exporter)
- [GoB](https://github.com/JoseConseco/GoB)
- Import Images as Planes - Built-in!

### Cloud-based User Preferences
- Blender Cloud - Built-in!
- Blender ID Auth - Built-in!

### Blender Development
- Icon Viewer - Built-in!
- Math Vis (Console) - Built-in!