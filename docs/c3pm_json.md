## c3pm.json file

### Concept

As [npm][npm website]'s [**package.json**][npm website/json], **c3pm.json**
is simply a file that stores information about project and it's dependencies.

Here how it typically looks like:

```json
{
    "name": "cpppm_test_repo3",
    "author": "Oleh Kurachenko",
    "version": "0.0.1",
    "description": "Project dependencies for cpppm_test_repo3",
    "url": "https://github.com/OlehKurachenko/cpppm_test_repo3.git",
    "email": "oleh.kurachenko@gmail.com",
    "dependencies": [
        {
            "type": "git-c3pm",
            "url": "https://github.com/OlehKurachenko/cpppm_test_repo2.git",
            "version": "master"
        }
    ],
    "c3pm_version": "v0.2",
    "whatIsC3pm": "https://github.com/OlehKurachenko/c3pm"
}
```

### Fields

Mandatory field are marked with *

#### name*

A project's name, used as directory name in **imports** (by default)

#### author*

Author's name

#### version*

A current project version.

#### license

A project's license.

#### description

A short description of a project

#### url

A project's url

#### e-mail

Project's e-mail

#### c3pm_version*

A version of c3pm.json standard used in this very c3pm.json

#### whatIsC3pm

Optional field, a url of c3pm project

#### dependencies

A list of dependencies records. Each record must have field **"type"**.

In this moment, the next dependencies types are supported:

* ##### git-c3pm
  A dependncy must be a project in git reporitory, with proper c3pm-project
  structure (must have **src/exports** and **c3pm.json**).
  
  **url&ast;**: url of git repository, which can be cloned.
  
  **version&ast;**: branch, tag or commit which will be taken.  
  :heavy_exclamation_mark::wrench: At this very moment, it HAVE to be
  master


[npm website]: https://www.npmjs.com/
[npm website/json]: https://docs.npmjs.com/getting-started/using-a-package.json
