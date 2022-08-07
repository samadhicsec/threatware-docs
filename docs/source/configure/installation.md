# Installation

threatware can be installed in 2 different environments:

- CLI (on Linux)
- AWS Lambda

## CLI

Given your environment has a recent version of `python` (3.9 or above, and you should have `pip` installed as well ([instructions](https://pip.pypa.io/en/stable/installation/))) and that a recent version of `git` is installed ([instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)).  You may also want to consider installing threatware in a [virtual environment](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments)

To install threatware:

`python3 -m pip install threatware`

This will make the command `threatware` available in your CLI which you can use to invoke threatware.

## AWS Lambda

Given your environment has:
- a recent version of the [AWS console](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 
- a recent version of [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), and
- a recent version of [docker](https://docs.docker.com/get-docker/)

You will also need to configure the `aws` CLI command with an approriate profile with credentials (whichever AWS role is being used to run the AWS commands it will need several permissions for IAM, ECR, Secrets Manager, Lambda and API Gateway).

1) Clone the threatware repo

    ```shell
    git clone https://github.com/samadhicsec/threatware
    ```

2) Build the docker image

    ```shell
    cd samadhicsec/threatware
    docker build -t threatware-image .
    ```

3) Set some environment variables - this will make the commands below easier.  Replace the values with values relevant to your environment

    ```shell
    # e.g. export AWS_REGION=us-east-1
    export AWS_REGION=<REGION>
    export AWS_PROFILE=<PROFILENAME>
    export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
    ```

4) Login to AWS ECR

    ```shell
    aws ecr get-login-password | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
    ```

5) Create an ECR repository (only need to do this once)

    ```shell
    aws ecr create-repository --repository-name threatware-image
    ```

6) Upload the docker container image

    ```shell
    docker tag threatware-image:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/threatware-image:latest
    docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/threatware-image:latest
    ```

7) Configure AWS Secret Manager

    Create a JSON file for each of git, confluence and googledocs, with the appropriate format as described in [](./authentication.md#authentication-for-threatware-aws-lambda)

    Combine these into a single (escaped) JSON file (the below assumes the above 3 files are named `git.json`, `confluence.json`, `googledocs.json`).  `jq` needs to be [installed](https://stedolan.github.io/jq/download/).

    ```shell
    jq --null-input \
    --arg gitarg "$(jq -c . git.json)" \
    --arg confarg "$(jq -c . confluence.json)" \
    --arg gdarg "$(jq -c . googledocs.json)" \
    '{"git": $gitarg, "confluence": $confarg, "google": $gdarg}' \
    > secret.json
    ```

    Upload the `secret.json` to AWS Secrets Manager

    ```shell
    aws secretsmanager create-secret --name threatware --secret-string file://secret.json
    ```

    Make a note of the ARN of the secret in the output of the command.  This is needed when creating an IAM policy for threatware lambda to read the secret.

8) Create IAM Policy and Role

    We need to create the IAM Role for the lambda and then add the policies giving it the permissions it needs.
    
    First create a policy file that let's lambda assume the role we will create, call it `assume-role.json`:

    ```json assume-role.json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    ```

    Now create the Role:

    ```shell
    aws iam create-role --role-name threatware-role --assume-role-policy-document file://assume-role.json
    ```

    Note the ARN, we need this to create the lambda function.
    
    Next create an IAM Policy to allow threatware lambda to access the secrets.   (entering the ARN of the secret), call it `threatware-policy.json`:

    ```json
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetResourcePolicy",
                "secretsmanager:GetSecretValue",
                "secretsmanager:DescribeSecret",
                "secretsmanager:ListSecretVersionIds"
            ],
            "Resource": [
                "<enter arn for secret from previous step>"
            ]
        },
        {
            "Effect": "Allow",
            "Action": "secretsmanager:ListSecrets",
            "Resource": "*"
        }
        ]
    }
    ```

    Now create the IAM policy

    ```shell
    aws iam create-policy --policy-name threatware-policy --policy-document file://threatware-policy.json
    ```

    Note the ARN, we need that.

    Now we associate the appropriate IAM Policies to the threatware lambda IAM Role

    ```shell
    # Attach the threatware-policy to allow access to secrets
    aws iam attach-role-policy --role-name threatware-role --policy-arn <insert ARN for threatware-policy> 

    # Attach this policy to allow access to CloudWatch for logging (this policy could be tightened to restrict access to specific log groups)
    aws iam attach-role-policy --role-name threatware-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

    # If you intend to deploy the threatware lambda in a VPC you will also need
    aws iam attach-role-policy --role-name threatware-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
    ```

9) Create your own threatware configuration repo following the instructions [](./configuration.md#using-a-custom-git-configuration-repository).  Make a note of the git URL of the repo.

    Make sure the providers/providers_config.yaml is updated with the correct AWS Secret Manager secret name (by default `threatware`) and region (by default `eu-west-2`).

10) Create a lambda function

    Be sure to insert the ARN of the threatware-role and the location of the git repo with your configuration e.g. git@github.com:...

    ```shell
    aws lambda create-function \
    --function-name threatware \
    --role <insert ARN of threatware-role> \
    --code ImageUri=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/threatware-image:latest \
    --timeout 30 \
    --memory-size 512 \
    --publish \
    --package-type Image \
    --environment Variables="{THREATWARE_AWS_SECRET_NAME=threatware,THREATWARE_AWS_SECRET_REGION=$AWS_REGION,THREATWARE_CONFIG_DIR=/tmp/.threatware,THREATWARE_CONFIG_REPO=<Git repo URL>}"
    ```

    Note the lambda ARN

    :::{admonition} Test
    While not essential, you can at this stage test if the lambda function is operating correctly.  This could be useful as if there are any issues with the API Gateway configuration (the next step) then if you have already tested the lambda, at least you know the lambda is working, so any issues must be API Gateway related.

    The easiest was to test the lambda is via the AWS Console, by navigating to the lambda and selecting the "Test" tab.  Select "Create new event" and the "Event JSON" structure looks like:
    ```json
    {
        "queryStringParameters": {
            "action": "...",
            "scheme": "...",
            "docloc": "...",
            "doctemplate": "..."
        }
    }
    ```
    Where the values need to be populated with appropriate values.  Even a test with fake values will be useful in demonstrating the lambda is being invoked.  Next a test using the [](../actions/convert.md) action is the simplest action for testing purposes.

    Another option is to test via the AWS CLI using the command below.  First save the above event JSON in a file called `event.json`.

    ```shell
    aws lambda invoke --cli-binary-format raw-in-base64-out --function-name threatware --payload file://event.json event-output.json
    ```
    :::

11) Configure the API Gateway

    ::::{admonition} Tip
    The far easier way to configure API Gateway to invoke the lambda is to use the AWS Console.  Navigate to the lambda, select "Add Trigger", choose API Gateway, and choose "REST API" and "Open" Security.

    :::{admonition} Warning
    :class: warning
    If configuring an API Gateway via the AWS Console, the IP restriction needs to be added manually. Navigate to the API in the API Gateway section, select "Resource Policy" and copy in the contents of `ip-restriction.json` (below).  Replace the shell variables in the contents and enter the IP range restriction.
    :::
    ::::

    ```shell
    export AG_API_ID=$(aws apigateway create-rest-api --name 'threatware-API' --description 'API to access threatware lambda' --query 'id' --output text)
    ```

    Create a local file with the policy we need to attach to the API Gateway.  This policy includes an IP restriction on who can invoke the API.  Call it `ip-restriction.json`

    Be sure to replace the IP range in the example file below (you can leave the variables as they are).

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": "*",
                "Action": "execute-api:Invoke",
                "Resource": "arn:aws:execute-api:$AWS_REGION:$AWS_ACCOUNT_ID:$AG_API_ID/*/*/*"
            },
            {
                "Effect": "Deny",
                "Principal": "*",
                "Action": "execute-api:Invoke",
                "Resource": "arn:aws:execute-api:$AWS_REGION:$AWS_ACCOUNT_ID:$AG_API_ID/*/*/*",
                "Condition": {
                    "NotIpAddress": {
                        "aws:SourceIp": "<insert IP address or CIDR block>"
                    }
                }
            }
        ]
    }
    ```
    
    Let's substitute the variables in the file

    ```shell
    envsubst <ip-restriction.json >ip-restriction-sub.json
    ```

    Update the policy for the API

    ```shell
    aws apigateway update-rest-api --rest-api-id $AG_API_ID --patch-operations op=replace,path=/policy,value="$(jq @json -c . ip-restriction-sub.json)"
    ```

    We need to add a path so threatware can be called

    ```shell
    export APIG_RESOURCE_ID=$(aws apigateway create-resource --rest-api-id $AG_API_ID --parent-id $(aws apigateway get-resources --rest-api-id $AG_API_ID --query 'items[?path==`/`].id' --output text) --path-part 'threatware' --query id --output text)
    ```

    Add the HTTP method (we all any method)

    ```shell
    aws apigateway put-method --rest-api-id $AG_API_ID --resource-id $APIG_RESOURCE_ID --http-method ANY --authorization-type "NONE"
    aws apigateway put-method-response --rest-api-id $AG_API_ID --resource-id $APIG_RESOURCE_ID --http-method ANY --status-code 200
    ```

    Create the IAM role and policy for the API to invoke the lambda.  Create `apig-assumerole.json` using:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "apigateway.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
            }
        ]
    }
    ```

    ```shell
    export APIG_ROLE_ARN=$(aws iam create-role --role-name apig-role --assume-role-policy-document file://apig-assumerole.json --query Role.Arn --output text)
    ```

    Create a policy allow invocation of the lambda called `apig-lambda-policy.json`:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "lambda:InvokeFunction",
                "Resource": "<insert lambda ARN>"
            }
        ]
    }
    ```

    ```shell
    aws iam create-policy --policy-name apig-lambda-policy --policy-document file://apig-lambda-policy.json

    aws iam attach-role-policy --role-name apig-role --policy-arn "arn:aws:iam::$AWS_ACCOUNT_ID:policy/apig-lambda-policy"  
    ```

    Add an integration so the resource can call the lambda

    ```shell
    aws apigateway put-integration --rest-api-id $AG_API_ID --resource-id $APIG_RESOURCE_ID --http-method "ANY" --type AWS_PROXY --integration-http-method POST --uri "arn:aws:apigateway:$AWS_REGION:lambda:path/2015-03-31/functions/arn:aws:lambda:$AWS_REGION:$AWS_ACCOUNT_ID:function:threatware/invocations" --credentials $APIG_ROLE_ARN
    aws apigateway put-integration-response --rest-api-id $AG_API_ID --resource-id $APIG_RESOURCE_ID --http-method ANY --status-code 200 --selection-pattern ""
    ```

    Create a deployment and associate with a stage

    ```shell
    aws apigateway create-deployment --rest-api-id $AG_API_ID --stage-name default
    ```

12) Test the threatware lambda can be called 

    ```shell
    curl https://$AG_API_ID.execute-api.$AWS_REGION.amazonaws.com/default/threatware?action=convert
    ```

    This should return an error message about missing parameters, which means the lambda is being invoked successfully.  
    
    A response of "Internal Server Error" may mean a problem with the configuration. First thing to check is APIGateway in AWS Console, via Resources menu, select "ANY" under "/threatware" and use the "Test" functionality which will show logs for a APIGateway call.