Setting Environment

# Installation

## Step 1. Install Python 3 (version 3.7)

- Link: [[https://www.python.org/downloads/]]
- Install requirements:

```
pip install boto3
```

```
pip install stripe
```

## Step 2. Install NodeJS (version 12)

- Link: [[https://nodejs.org/en/]]

## Step 3. Install AWS CLI & Configure

### Install

- For Window: [[https://awscli.amazonaws.com/AWSCLIV2.msi]]
- For MacOS: [[https://awscli.amazonaws.com/AWSCLIV2.pkg]]
- For Linux:

```
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```

```
$ unzip awscliv2.zip
```

```
$ sudo ./aws/install
```

### Configure

Contact your admin to get AWS account

- Run ```
  $ aws configure --profile isso-admin

````
- Input key ( **Need AWS account - get Access Key & Secret Access Key from AWS IAM** )
> AWS Access Key ID [None]: [Input Access Key which you get from your admin]
> AWS Secret Access Key [None]: [Input Secret Access Key which you get from your admin]
> Default region name [None]: ap-northeast-1
> Default output format [None]: json

## Step 4. Install AWS SAM & Docker
### Prerequisite
- AWS CLI
- AWS account & IAM User with Administrator Permissions
- Docker

### Setup
#### Follow link instruction to setup (skip step 1 & 2)
- For Window: [[https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-windows.html]]
- For MacOS: [[https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-mac.html]]
- For Linux: [[https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html]]

## Step 5. Install Sourcetree & Clone repository
### Install Sourcetree
- Follow link & download: [[https://www.sourcetreeapp.com/]]
- Execute file & install

### Configure key Git Backlog
- Login to Backlog
- Follow link: [[https://dgm.backlog.com/userBasicAuthPasswords]]
- Follow image step
![image][backlog1.png]
![image][backlog2.png]

### Clone repository
- For Window:
![image][backlog5.png]
- For MacOS:
![image][backlog3.png]
![image][backlog4.png]
![image][backlog6.png]

-------------
#### Note
* Link git: [[https://dgm.backlog.com/git/ISSO_ALFA/isso_0.1.git]]
* Authorize git
    * Username: [ **Email backlog** ]
    * Password: [ **Copied password from previous step** ]
* From now `isso_0.1` mean the root [[https://dgm.backlog.com/git/ISSO_ALFA/isso_0.1.git]]

## Step 6. Install Visual Studio Code (VS code)
- Link: [[https://code.visualstudio.com/]]
- Install VSCode extensions at `isso_0.1/.vscode/extensions.json`
- Install requirements for ESLint:
```cd isso_0.1```
```npm i```

## Step 7. Install package front-end
- Open VS code
- Select open folder & choose isso_0.1
- For Window: use ``` Ctrl + ~ ``` to open terminal
- For MacOS: use ``` Control + ~ ``` to open terminal
- Run ```cd ~/ISSO/package/webapp && npm i ``` to install package
- In directory **packages/webapp**
- Create file  **.env.development.local**  like image.(blank content, create if not exits)
![image][Screen Shot 2020-09-09 at 16.55.15.png]

# Run local
## Setup back-end & DB
- Run ```cd isso_0.1```
- Run ```npm i``` (If have new package installed or updated)
- Run ``` python cloudformation/scripts/deploy_isso.py [env_name] ```  ( **Note**: [env_name] Any name is fine (only a-z except [staging, prod, canary], should be name of developer )
    - example: ``` python cloudformation/scripts/deploy_isso.py yourname ```
- Run ``` python cloudformation/scripts/publish_layer_version.py [env_name] ```
- Run ``` python cloudformation/scripts/update_webapp_env.py [env_name] ```

confirm DB after finish:
![image][Screen Shot 2020-10-06 at 10.50.00.png]

## Run application
- In terminal move to directory **/ISSO/packages/webapp**
- Run ``` npm run serve ```
- Image when finish.

![image][Screen Shot 2020-09-09 at 15.12.02.png]

-After that open link http://localhost:8080/signin

![image][Screen Shot 2020-09-09 at 15.12.41.png]

-Create Tenant: http://localhost:8080/system/create-tenant

![image][Screen Shot 2020-10-06 at 10.52.17.png]

# Deploy & update code (development enviroment)
- Run ```cd isso_0.1```
- If have a new package installed or updated in `isso_0.1/package.json` file
    - Run ```npm i``` (Can skip this command if your packages are up to date)
- Run ``` python cloudformation/scripts/deploy_isso.py [env_name] ```
  **Note**: [env_name] Any name is fine (only a-z except prod/canary/staging/prestaging/dev)
    - example: ``` python cloudformation/scripts/deploy_isso.py yourname ```
- If have a new package installed or updated in `isso_0.1/packages` folder
    - Run ``` python cloudformation/scripts/publish_layer_version.py [env_name] ``` (Optional)

# Deploy prod/canary/staging/prestaging
(In the Vietnamese team, IAM users have been limited, to only some users that have the right to deploy)
When deploying prod/canary/staging have message confirm like below image, please enter `y` to continue.
![image][image (3).png]

- Run ```cd isso_0.1```
- If have a new package installed or updated in `isso_0.1/package.json` file
    - Run ```npm i``` (Can skip this command if your packages are up to date)
- Run ```python cloudformation/scripts/deploy_isso.py [env_name] --deploy-webapp```
  **Note**: [env_name] is prod/canary/staging/prestaging
    - example: ``` python cloudformation/scripts/deploy_isso.py staging --deploy-webapp```
- If have a new package installed or updated in `isso_0.1/packages` folder
    - Run ```python cloudformation/scripts/publish_layer_version.py [env_name]``` (Optional)

# Create admin account
- Run ``` python scripts/create_sys_admin_user.py [env_name] --email [email] --password [password] --given-name [given_name] --family-name [family_name]```

# Create table DynamoDB (using AWS CloudFormation)
- Open file  **dynamodb-tables.template**  in folder ```cloudformation/templates/```
- Edit/Add in template file ( **Document CloudFormation DynamoDB** :  [LINK](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html) )
- Update file script  **deploy_dynamodb_tables.py** in folder ```cloudformation/scripts/``` like image below
![image][dynamodb_scripts.png]

- Run ``` python scripts/deploy_dynamodb_tables.py [env_name] ```

# Make Create Branch | Git Rule
- Confirm Git Flow in here https://dgm.backlog.com/wiki/ISSO_ALFA/How+to+use+Git+Repositry
- Checkout branch from develop to get newest code
![image][create-branch.png]
    - 1: Click on 1 of the 2 places to create a branch
    - 2: Name the branch according to recommended usage (Branch name is task issue)
        - ex: feature/ISSO_ALFA-xxx to make feature xxx
    - 3: Click Create Branch button

# Make Stage and Commit | Git Rule
## Stage
- From local branch:
![image][staged.png]
    - 1: Click the "Commit" button to check the preparation before committing
    - 2: This frame contains the file that has changed
    - 3: Check carefully changed files need to be commit and staged by nearby left checkbox

## Commit
- From local branch:
![image][commit.png]
    - 1: Check again changed files before committing
    - 2: At the message frame, write message about change (follow structure)
    - 3: Click button to push immediately
    - 4: Click "Commit" button to commit and push to remote


# Make Pull Request | Git Rule
 **- After finish test your task in local.**
- Merge develop to your branch again and then pull request.
- Go to url:  [LINK -  Git Remote](https://dgm.backlog.com/git/ISSO_ALFA)
- Choose repositories you want to pull request and click "Pull request" button
![image][git remote.png]
- Click make pull request at icon "+"
![image][pull request list.png]
- Create pull request
![image][pull request.png]
    - 1: Choose branch you need merge to  (develop)
    - 2: Choose your local branch to need be merged (ex feature/ISSO_ALFA-xxx)
    - 3: Choose your assignee to check code before merging (In Viet Nam team will Assign for Nhat Chau or Tam Nguyen)
    - 4: Click make "Pull request" button

# Review source code when merge Pull Request
- Check commit change carefully in here
![image][Screen Shot 2020-10-08 at 11.25.09.png]

- If have conflict:
    - Go back to source branch and merge target branch into that.
    - Fix conflict and commit , push current branch again.
    - Reload link pull request check if conflict is removed.
- If conflict is solved or no conflict exist, press merge and fill in comment (optional), and finally merge.
 **- Then test again in local**
- If ok deploy to STG or Canary.
-------------------
````
