# c3pm

### Idea

This will be a new, super simple package manager to handle multiple
dependencies especially for C/C++ programming language. The most
important thing about it is that it do not try to handle your
compilation and binaries. It will deal primary with your source code.

### [Usage][usagePage]

### Technical concept

:heavy_exclamation_mark::wrench: At this moment, this technical concept is not
fully implemented!

#### Context

Basically, we include/import/parse/ect. one file from another by 
(in some way) writing a path to that file.

Lest assume that we have
project **A** containing files **a.cpp** & **a.h**, and project 
**B** containing **b.cpp** & **b.h**. 

```
~(root)
├─── A
│    ├─── a.cpp
│    └─── a.h
└─── B
     ├─── b.cpp
     └─── b.h
```

Including (lets continue using C++ language) **b.h** from **b.cpp**
is obvious:

```cpp
//  Filename: b.cpp
#include < b.h >
```

#### Approach #1

Now, lets consider that we work with project **B** now and want to add 
**A** as a dependency. The simplest way to do this is  (I am talking
about automatic process, form the point of view of that process) to
download B and to place it in the same directory as **B**. 

Now, we are able to include our **a.h** in this way:

```cpp
//  Filename: b.cpp
#include < ../A/a.h >
#include < b.h >
```

But, it causes a lot of problems:
1. We are placing something outside our project directory, so it'll
cause an error it there is already a directory with the same name, but
more generally - we'll be unable to understand, which directories in
**~(root)** are real project and which one are their dependencies.
2. If different projects have different dependencies with the same
directories names, we'll be unable to place them in the same directory,
having the same simple include (in ```#include < ../A/a.h >``` we'll)
have to rename ```A``` in all the project code.

So, obviously, we cannot do it like this.

#### Approach #2

Ok, lets go another way. For every project which have dependencies,
we'll create a file, which contains a list of them
(like **package.json**), and when we want dependencies to be downloaded,
a new directory **imports** will be created in project directory, and so,
imports files will be added to directories with their names. Just like
this:

##### Non-updated:
```
~(root)
└─── B
     ├─── b.cpp
     ├─── b.h
     └─── c3pm.json
```

##### Updated:
```
~(root)
└─── B
     ├─── imports
     │    └─── A
     │         ├─── a.cpp
     │         └─── a.h
     ├─── b.cpp
     ├─── b.h
     └─── c3pm.json
```

##### c3pm.json
```json
{
    "name": "B",
    "dependencies": [
        "A"
    ]
}
```

So, we'll create directory **imports** for all dependencies,
recursively.

So, we are able to include our **a.h** in this way:

```cpp
//  Filename: b.cpp
#include < imports/A/a.h >
#include < b.h >
```

It looks really good. But, there is a serious problem again: multiple
copies. Lets consider an example. We'll have also projects **C** 
& **D**, similar to **A** & **B**. We'll also have the next
dependencies list:

##### B/c3pm.json
```json
{
    "name": "B",
    "dependencies": [
        "A"
    ]
}
``` 

##### C/c3pm.json
```json
{
    "name": "C",
    "dependencies": [
        "A",
        "B"
    ]
}
``` 

##### D/c3pm.json
```json
{
    "name": "D",
    "dependencies": [
        "A",
        "B",
        "C"
    ]
}
``` 

After download of all dependencies for project **D**, 
we'll have next file tree:

```
~(root)
└─── D
     ├─── imports
     │    ├─── A
     │    │    ├─── a.cpp
     │    │    └─── a.h
     │    ├─── B
     │    │    ├─── imports
     │    │    │    └─── A
     │    │    │         ├─── a.cpp
     │    │    │         └─── a.h
     │    │    ├─── b.cpp
     │    │    ├─── b.h
     │    │    └─── c3pm.json
     │    └─── C
     │         ├─── imports
     │         │    ├─── A
     │         │    │    ├─── a.cpp
     │         │    │    └─── a.h
     │         │    └─── B
     │         │         ├─── imports
     │         │         │    └─── A
     │         │         │         ├─── a.cpp
     │         │         │         └─── a.h
     │         │         ├─── b.cpp
     │         │         ├─── b.h
     │         │         └─── c3pm.json
     │         ├─── c.cpp
     │         ├─── c.h
     │         └─── c3pm.json        
     ├─── d.cpp
     ├─── d.h
     └─── c3pm.json
```

Four copies of **a.cpp** & **a.h**, two copies of **b.cpp** & **b.h**.
Despite this copies are being made automatically, it can cause a
serious problems with memory, download and compilation time.

#### Final approach

It seems that a good idea is to have only one copy of each dependency form
any level of enclosure in **imports**. That means that including a file from
dependency in project have to be identical to including a file form another 
dependency in one dependency.

Here is an example:

##### Non-updated:
```
~(root)
└─── B
     ├─── src
     │    └─── exports
     │         ├ b.h
     │         └ b.cpp
     └─── c3pm.json
```

##### Updated:
```
~(root)
└─── B
     ├─── src
     │    └─── exports
     │         ├ b.h
     │         └ b.cpp
     ├─── imports
     │    └─── A
     │         ├ a.h
     │         └ a.cpp
     └─── c3pm.json
```

##### Example form "Approach #2" in our new manner:

```
~(root)
└─── D
     ├─── src
     │    └─── exports
     │         ├ d.h
     │         └ d.cpp
     ├─── imports
     │    ├─── A
     │    │    ├ a.h
     │    │    └ a.cpp
     │    ├─── B
     │    │    ├ b.h
     │    │    └ b.cpp
     │    └─── C
     │         ├ c.h
     │         └ c.cpp
     └─── c3pm.json
```

Now, our path to file in dependency is indential both for any file in
**src/exports** and in **imports/&ast;**:

##### b.cpp
```cpp
//  Filename: b.cpp
#include < ../../imports/A/a.h >
#include < b.h >
```

##### d.cpp
```cpp
//  Filename: d.cpp
#include < ../../imports/A/a.h >
#include < ../../imports/B/b.h >
#include < ../../imports/C/c.h >
#include < d.h >
```

So, when the project **A** is taken as dependency by other project, containment of
it's **src/exports** is taken, and copied to **imports/A** of the new project.
So, you can have all your project code in one directory **src**, but only 
containment of **src/exports** will be taken. That allow to have unittests, for 
example, in **src**

##### With some other code:

```
~(root)
└─── D
     ├─── src
     │    ├─── exports
     │    │    ├ d.h
     │    │    └ d.cpp
     │    └─── unittest
     │         └ d_unittest.py
     ├─── imports
     │    ├─── A
     │    │    ├ a.h
     │    │    └ a.cpp
     │    ├─── B
     │    │    ├ b.h
     │    │    └ b.cpp
     │    └─── C
     │         ├ c.h
     │         └ c.cpp
     └─── c3pm.json
```

[usagePage]: docs/Usage.md