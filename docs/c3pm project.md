## c3pm project

Actually, to be used by c3pm, project have to meet certain requirements.  
c3pm project have to:

1. have a valid [**c3pm.json**][c3pm_json_doc]
2. files **src** and **exports** cannot exist in project directory. That
means that directory **src** and it's subdirectory **exports** can exist in
project directory, or not.

To use c3pm, there are two more requirements:

1. neither file nor directory **.c3pm_clonedir** must exist in project
directory, c3pm have to be able to create a directory with this name and
delete it
2. file **imports** cannot exist in project directory. c3pm have to be able to
delete and create a directory with this name 

[c3pm_json_doc]: c3pm%20json.md