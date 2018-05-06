## Usage

### [c3pm.json][c3pm_json]

### CLI commands

#### init

Initializes project as c3pm-project.
Creates (if not exist) **src** and **src/exports** directories,
and **c3pm.json** file with data form uservia CLI and empty
dependencies list.

If project directory is a git repository (**.git** directory exist
), **imports/&ast;&ast;** and **.c3pm_clonedir/&ast;&ast;** are being
added to **.gitignore** (if they still are not there). If **.gitignore**
does not exist, it is being created.

Existence of **src** or **src/exports** as file and **c3pm.json** as
directory causes an error.

[c3pm_json]: c3pm_json.md