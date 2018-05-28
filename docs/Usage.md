## Usage

### [c3pm.json][c3pm_json]

### CLI commands

#### init

Initializes project as c3pm-project.
Creates (if not exist) **src** and **src/exports** directories.
Directory **src/exports** is being created with file **readme.txt**
inside of it, which contains a tip. Creates **c3pm.json** file with
data from user via CLI and empty dependencies list.

If project directory is a git repository (**.git** directory exist
), **imports/&ast;&ast;** and **.c3pm_clonedir/&ast;&ast;** are being
added to **.gitignore** (if they still are not there). If **.gitignore**
does not exist, it is being created.

Existence of **src** or **src/exports** as file and **c3pm.json** as
directory causes an error. Existence of **c3pm.json** as file causes a
termination - file have to be deteled to re-init project.

Example: 
```bash
c3pm init
```

#### list

List all project's dependencies recursively. So, all the dependencies are
being loaded to look on their own [c3pm.json][c3pm_json] file to get list
of dependencies. At the result, a list of all projects which have to be
loaded is printed with proper data about them.

Example:
```bash
c3pm list
```

#### add

Adds a new dependency to project (actually, to it's [c3pm.json][c3pm_json]).
It's first agrument have to specify type of dependency, one of the following:

* ##### git-c3pm
  The following arguments in exactly the following order have to be
  provided: 
  * **name** - a name for dependency, have to be identical to the name of
    project (from [c3pm.json][c3pm_json] of it's git repository)
  * **url** - url of git repository of dependency
  * **version** - at this very moment, have to be exactly "master"
  
  Example:
  ```bash
  c3pm add git-c3pm c3pm_test_libmath https://github.com/c3pm/c3pm_test_libmath.git master
  ```

#### remove

Removes existing dependency from project (it's [c3pm.json][c3pm_json]). Two
arguments have to be provided: dependencies name and it's version.

Exapmle:
```bash
c3pm remove c3pm_test_libmath
```

### CLI commands usage examples

#### init

```
~/CLionProjects/c3pm_test_libmath$ ls -la
total 20
drwxrwxr-x  4 oleh oleh 4096 May 27 22:37 .
drwxrwxr-x 13 oleh oleh 4096 May 27 22:37 ..
drwxrwxr-x  8 oleh oleh 4096 May 27 22:38 .git
drwxrwxr-x  2 oleh oleh 4096 May 27 22:38 .idea
-rw-rw-r--  1 oleh oleh   64 May 27 22:37 README.md
~/CLionProjects/c3pm_test_libmath$ c3pm init
Project name>c3pm_test_libmath
Author>Oleh Kurachenko
Description>Test project of type "git-c3pm" for c3pm project
Project URL>https://github.com/c3pm/c3pm_test_libmath.git
Project e-mail>oleh.kurachenko@gmail.com
License (empty line if not exist)>
c3pm: srcdirectory created
c3pm: src/exports directory created
c3pm: src/exports/readme.txt written
c3pm: .gitinore written
c3pm: c3pm.json successfully written
~/CLionProjects/c3pm_test_libmath$ ls -la
total 32
drwxrwxr-x  5 oleh oleh 4096 May 27 22:52 .
drwxrwxr-x 13 oleh oleh 4096 May 27 22:37 ..
-rw-rw-r--  1 oleh oleh  369 May 27 22:52 c3pm.json
drwxrwxr-x  8 oleh oleh 4096 May 27 22:38 .git
-rw-rw-r--  1 oleh oleh   29 May 27 22:52 .gitignore
drwxrwxr-x  2 oleh oleh 4096 May 27 22:52 .idea
-rw-rw-r--  1 oleh oleh   64 May 27 22:37 README.md
drwxrwxr-x  3 oleh oleh 4096 May 27 22:52 src
~/CLionProjects/c3pm_test_libmath$ cat c3pm.json 
{
    "name": "c3pm_test_libmath",
    "author": "Oleh Kurachenko",
    "version": "0.0.1",
    "description": "Test project of type \"git-c3pm\" for c3pm project",
    "url": "https://github.com/c3pm/c3pm_test_libmath.git",
    "email": "oleh.kurachenko@gmail.com",
    "dependencies": {},
    "c3pm_version": "v0.2",
    "whatIsC3pm": "https://github.com/c3pm/c3pm"
}~/CLionProjects/c3pm_test_libmath$ cat .gitignore 
imports/**
.c3pm_clonedir/**
~/CLionProjects/c3pm_test_libmath$ tree
.
├── c3pm.json
├── README.md
└── src
    └── exports
        └── readme.txt

2 directories, 3 files
```

#### list

```
~/CLionProjects/c3pm_test_polinomial$ c3pm list
c3pm: Listing all dependencies for project c3pm_test_polinomial
c3pm: cloning ~root~project~->c3pm_test_libmath (https://github.com/c3pm/c3pm_test_libmath.git) to c3pm_test_libmath
Cloning into 'c3pm_test_libmath'...
remote: Counting objects: 19, done.
remote: Compressing objects: 100% (13/13), done.
remote: Total 19 (delta 2), reused 16 (delta 2), pack-reused 0
Unpacking objects: 100% (19/19), done.
Checking connectivity... done.
c3pm: ~root~project~->c3pm_test_libmath cloned
Dependencies for c3pm_test_polinomial:
├─── c3pm_test_libmath-> type: git-c3pm, url: https://github.com/c3pm/c3pm_test_libmath.git, version: master
```

#### add

#### git-c3pm

```
~/CLionProjects/c3pm_test_polinomial$ cat c3pm.json 
{
    "name": "c3pm_test_polinomial",
    "author": "Oleh Kurachenko",
    "version": "0.0.1",
    "description": "Test project of type \"git-c3pm\" for project c3pm",
    "url": "https://github.com/c3pm/c3pm_test_polinomial.git",
    "email": "oleh.kurachenko@gmail.com",
    "dependencies": {},
    "c3pm_version": "v0.2",
    "whatIsC3pm": "https://github.com/c3pm/c3pm"
}~/CLionProjects/c3pm_test_polinomial$ c3pm add git-c3pm c3pm_test_libmath https://github.com/c3pm/c3pm_test_libmath.git master
c3pm: cloning repository for new dependency "c3pm_test_libmath" (https://github.com/c3pm/c3pm_test_libmath.git) to ~tempdir~
Cloning into '~tempdir~'...
remote: Counting objects: 19, done.
remote: Compressing objects: 100% (13/13), done.
remote: Total 19 (delta 2), reused 16 (delta 2), pack-reused 0
Unpacking objects: 100% (19/19), done.
Checking connectivity... done.
c3pm: repository for new dependency "c3pm_test_libmath" cloned
c3pm: dependency c3pm_test_libmath (type: git-c3pm, url: https://github.com/c3pm/c3pm_test_libmath.git, version: master) successfully added to project
~/CLionProjects/c3pm_test_polinomial$ cat c3pm.json 
{
    "name": "c3pm_test_polinomial",
    "author": "Oleh Kurachenko",
    "version": "0.0.1",
    "description": "Test project of type \"git-c3pm\" for project c3pm",
    "url": "https://github.com/c3pm/c3pm_test_polinomial.git",
    "email": "oleh.kurachenko@gmail.com",
    "dependencies": {
        "c3pm_test_libmath": {
            "type": "git-c3pm",
            "url": "https://github.com/c3pm/c3pm_test_libmath.git",
            "version": "master"
        }
    },
    "c3pm_version": "v0.2",
    "whatIsC3pm": "https://github.com/c3pm/c3pm"
}
```

#### remove

```
~/CLionProjects/c3pm_test_polinomial$ cat c3pm.json 
{
    "name": "c3pm_test_polinomial",
    "author": "Oleh Kurachenko",
    "version": "0.0.1",
    "description": "Test project of type \"git-c3pm\" for project c3pm",
    "url": "https://github.com/c3pm/c3pm_test_polinomial.git",
    "email": "oleh.kurachenko@gmail.com",
    "dependencies": {
        "c3pm_test_libmath": {
            "type": "git-c3pm",
            "url": "https://github.com/c3pm/c3pm_test_libmath.git",
            "version": "master"
        }
    },
    "c3pm_version": "v0.2",
    "whatIsC3pm": "https://github.com/c3pm/c3pm"
}~/CLionProjects/c3pm_test_polinomial$ c3pm remove c3pm_test_libmath master
directory to be removed: c3pm_test_libmath -> type: git-c3pm , url: https://github.com/c3pm/c3pm_test_libmath.git , version: master
c3pm: dependency c3pm_test_libmath(version master successfully removed
~/CLionProjects/c3pm_test_polinomial$ cat c3pm.json 
{
    "name": "c3pm_test_polinomial",
    "author": "Oleh Kurachenko",
    "version": "0.0.1",
    "description": "Test project of type \"git-c3pm\" for project c3pm",
    "url": "https://github.com/c3pm/c3pm_test_polinomial.git",
    "email": "oleh.kurachenko@gmail.com",
    "dependencies": {},
    "c3pm_version": "v0.2",
    "whatIsC3pm": "https://github.com/c3pm/c3pm"
}
```

[c3pm_json]: c3pm%20json.md