# MORCoRE

MORCoRE is search-based refactoring tool for recommending refactoring operations towards a target repository snapshot.

It based on multi-objective evolutionary algorithm (MOEA), the refactorings recommended achieve 3 objectives:
1. Improving code quality
2. Preserving semantic coherence
3. Require low review effort


## Requirement
python 3.8 and later

## Build
1. **Clone this repository and install dependencies**

```
$ git clone https://github.com/MashiroCl/MORCOpy
$ cd MORCOpy
$ pip install -r requirements.txt
```
note: you can find jmetalpy [here](https://github.com/jMetal/jMetalPy), download the [jmetal 1.5.7 package](https://github.com/jMetal/jMetalPy/releases/tag/v1.5.7), and use pip to install it.


2. **Creating a personal access token**

MORCoRE uses the GitHub API, it needs the personal access token to extract pull requests.

For how to get personal access token, please refer to [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

3. **Set the token as a environment variable**

After you get the token, set it as an environment variable, and named the variable as **MORCoRE**

For MacOS:
```
$ echo "export MORCoRE=<personal-access-token>" >> ~/.bash_profile
$ source ~/.bash_profile
```

For Linux:
```
exportMORCoRE=<personal-access-token>
```


## Run
1. Extract abstract representation and call graph for the target repository snapshot.

Required: <repo_path>: cloned repository path <repo_url>: GitHub url for the repository

```
$ python3 command.py -r <repo_path> -u <repo_url> -m extract
```

2. Search refactoring sequences
```
$ python3 command.py -n <repo_name> -i <max_evaluation_number> -p <platform_name> -m search
```

