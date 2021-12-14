# About utils

This folder contains Lambda functions used for different purposes. For details on each function, refer to the README file in each folder.


# Development notes

AWS provides a cloud based IDE called Cloud9 that can be used for developing and testing Lambda functions as well as deployment and execution of each function. If you're using Cloud9, follow the guidlines below.

## Development and testing

A typical directory structure on Cloud9 looks as follows.

```
|-- main
    |-- function1
        |-- handler.py
        |-- ...
    |-- function2
        |-- handler.py
        |-- ...
    |-- .gitignore    
    |-- __init__.py
    |-- README.md
    |-- requirements.txt
    |-- template.yaml
```

**\_\_init\_\_.py ->** A standard Python package initialization file.  
**template.yaml ->** SAM template that Cloud9 will use to deploy the function in addition to other required services such as Lambda exeution roles and CloudWatch configuration.  
**requirements.txt->** A standard file for installing Python modules. This file should only include Python packages that are not available within Lambda execution environment.  
**README.md->** Explains what this function is intended to do as well as any additional requirements.  
**.gitignore->** Cloud9 creates various files for debugging and deployment. Add those files/folders to gitignore so they're not subbmited into code repository.  


### Running the code on Cloud9  

Cloud9 comes with Python virtualenv already installed which allows you to use Python libs locally installed in your project instead of system Python libs. Using virtualenv lets you generate a clean list of lib dependencies at the end of your development that will be defined in 'requirements.txt' file. To run your code on Cloud9, first upload the entire 'main' folder to your Cloud9 environment. Open up a terminal and do the following.

```bash
Admin:~/environment $ cd main
Admin:~/environment/main $ virtualenv venv
```

You will now be able to click on the Play button in Cloud9 to execute your code. To install additional Python libs such as 'requests', do the following.

```bash
Admin:~/environment $ cd main
Admin:~/environment/main $ source ./venv/bin/activate
(venv) Admin:~/environment/main $ pip install requests
```

After you're done with your development, export your Python lib dependencies to 'requirements.txt'
```bash
(venv) Admin:~/environment/main $ pip freeze > requirements.txt
```

**Important Note:** Makre sure you're within virtualenv environment when you run 'pip freeze'. If you're not then all the system Python libs wil be exported to 'requirements.txt' file.


## Code submission

Your code should only contain files mentioned in the directory structure above. You do not need to submit 'venv' or '.debug' folders or any other files that are automatically generated. Make sure you explain in README file if there are any special instructions on how to deploy and test the code. 
