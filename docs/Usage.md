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
directory causes an error. Existence of **c3pm.json** as file causes a
termination - file have to be deteled to re-init project.

#### list

List all project's dependencies recursively. So, all the dependencies are
being loaded to look on their own [c3pm.json][c3pm_json] file to get list
of dependencies. At the result, a list of all projects which have to be
loaded is printed with proper data about them.   

[c3pm_json]: c3pm%20json.md