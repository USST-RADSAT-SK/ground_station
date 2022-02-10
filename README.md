# ground_station
All code pertaining to the ground station for the RADSAT-SK can be found in this repository. The ground station code will have the ability to send commands and receive telemetry from the RADSAT-SK.


## Table of Contents
1. [Setting Up Your Repo](#Setting-Up-Your-Repo)
2. [How to Contribute](#How-to-Contribute)
    1. [Issues](#Issues)
    2. [Projects (and Managing Issues)](#Projects-and-Managing-Issues)
3. [Branching](#Branching)
    1. [Procedure](#Procedure)
    2. [Naming](#Naming)
4. [Coding Standard](#Coding-Standard)
    1. [Indentation](#Indentation)
    2. [Variables](#Variables)
    3. [Files](#Files)

## Setting Up Your Repository
1. Get WSL (Windows Subsystem for Linux) or Git Bash for your computer
2. Using one of the aforementioned programs, navigate to where you'd like the repository to exist
3. Run ```git clone https://github.com/USST-RADSAT-SK/ground_station.git``` (downloads the repository to your computer)
4. Navigate to the repo: ```cd ground_station```
5. pip install black

Now your repo should be all set up! Check out our "How to Contribute" and "Branching" sections below and coordinate with the Software and Command Team Lead(s) for further guidance.


## How to Contribute
### Issues
Issues are how we track software development tasks. Issues are typically either feature or bug related. E.g. "Implement Uplink Command Task" or "Fix Recieving Bug".
Issues can be created by going to the "Issues" tab within GitHub, and selecting "New Issue". Be sure to coordinate with your Team Lead(s) if you're unsure about this process though.

Be sure to assign the appropriate Project to the Issue being created; e.g. for an Recieve bugfix, that would likely go into the "Software" Project. If you're unsure of what projec it goes under, contact your Team Lead(s).

### Projects (and Managing Issues)
GitHub has a "Projects" tab, up top near the "Issues" tab. A Project is essentially a KanBan board that tracks individual Issues (and PRs). Issues and PRs can either be "To-Do", "In Progress", "In Review" or "Done". If you're looking for something new to work on, take a look at the items in the "To-Do" list of any Project! All you have to do is drag the Issue into the "In Progress" state. Be sure to communicate with the Software Team and Team Lead if you're not super familair with the process. Don't forget to assign yourself (and anyone else you're working with) on the Issue as well, so the Team knows what you're working.

When you finish (your first attempt at) the task, create a Pull Request of your working branch into alpha. Also move your issue from the "In Progress" state into the "In Review" state. Communicate with the software Team and Team Lead, and your Team Lead will facilitate reviewing and approving the PR and placing the task into the "Done" state.


## Branching
 
### Procedure
1. In your local repo run ```git checkout alpha``` (you may have to commit, stash, or throw away uncommitted changes on your current branch)
2. Run ```git pull``` (makes sure you have the latest code)
2. run ```git checkout -b "<your branch name>"``` (creates a new branch)
3. The first time that you try to push on the branch it will throw an error. Just follow the instructions to set the upstream branch.

### Naming
All branches **MUST** follow the few branch naming rules. Those rules are:
- No captials
- No underscores
- Use hyphens instead of spaces
- Must prepend new branch into one of six directories (see below)

GitHub (and most other Git platforms) allow you to use branch folders, simply by uses forward slashes. Some examples of *good* branch names:
- ```admin/restructure-directories```
- ```software/gun_radio_init```
- ```RF/antenna_installment```
- ```test/setting_up_a_fm_reciever```

Notice that all six of the directories used are based off of the Project names for the RADSAT-SK GitHub repo (minus hotfix, which is for quick fixes on alpha or beta branches).



## Coding Standard
Our coding standard is based on the Black coding style found [here](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html).

We have a coding standard so that everyone's code looks the same and is easily readable. Commits made to the project not adhering to these standards may not be allowed to be pushed. Source code from a third party will not be expected to follow these standards.

Like all rules, some exceptions can be allowed. The most important takeaway is that your code should be consistent and easy to read.

### Variables
#### Naming
Variable names should be descriptive and abbreviations should almost always be avoided. Exemptions may apply to loop variables.

All variable and function names are in camel case (first word lowercase, follwing words capitalized):

This is true for most variables and constants. However, for macros (and some enumerable types), the name is in all caps with underscores in between words:

As seen above, make sure to always wrap macros in brackets, and explicitly cast their type.

Most enums will have "global" scope, so you'll usually want to prepend their enumeration names with the name of the enum itself: 

ALso note that the enumeration values are all explictly defined; this is highly recommend for readability and to prevent mistakes.

In functions, most variables that will be used throughout the function should be declared at the *top* of the function. Exceptions may include variable declarations within the scope of an if or for loop.

### Files
#### File Naming
To prevent namespace collisions and to make it extra obvious what code is "local" (rather than imported), all locally created files **MUST** be prepended with the R character. After that, they follow the CapitalCase convention (each word starts with a capital, everything else is lowercase). Absolutely no underscores or hyphens in file names. 

Names should also be short and sweet. Acronyms are fine, but are still subject to CapitalCase conventions. 

Some good examples:
- RCommand.py
- RRecieve.py

#### File Section Separators
To increase readability (especially in larger files), multi-line function separators should be used. Ideally, these are used in all files. Do not use the separators to define a section if the section is empty, however. See the main examples of sections that are used:
``` 
/***************************************************************************************************
                                            DEFINITIONS                                             
***************************************************************************************************/

/***************************************************************************************************
                                       PRIVATE FUNCTION STUBS                                       
***************************************************************************************************/

/***************************************************************************************************
                                             PUBLIC API                                             
***************************************************************************************************/

/***************************************************************************************************
                                          PRIVATE FUNCTIONS                                          
***************************************************************************************************/
```
Each line ends after exactly 100 characters, and the words are centered.
These are not strictly enforced, but are highly recommended. Consistency is the most important thing.


