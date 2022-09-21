
# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

# Learning of Second Week
* In this week, we created the Web Health Monitoring application for the four URLs.
* First of all, I have created another lambda function to monitor the web `SkipQ.org` latency and availability.
* After that published metrics for monitoring latency and availability of the url(s) using `SDK boto3 client`.
* It will publish the availability and latency using Cloudwatch client
* After that I have created the alarms for the letancy and availability metrices and as alarm are the part of infrastructure so that's why we created them in the stack file.
* I have threshold the metric that we have uploaded over cloud watch. I did this because if something goes wrong we are able to monitor it. For this purpose, I have created the alarms and  as alarms are part of infrastructure so for good programming practice they should be created in the stack. Then I applied the notification services to the function so that if an alarm is raised, it will notify us via email. So I have successfully connected the monitoring of the services with notification services.
* After that I Revised the designed Lambda Function in order to deploy the Web Health monitoring application for four URLs and created alarms for all four of them as well.
* Created an SNS Topic and subscribed to it via my email in order to receive notifications when an alarm is raised by any four of the URL for either of the metric.
* Created a DynamoDB table as well as another Lambda function to parse the alarm information after which the latency and availability metrics would be passed on to store within the DynamoDB database.
* Set up an environment variable to access the created DynamoDB from within the Lambda Function. 
* Observe the final output.
# Enviornment Setup 
In order to deploy a function over AWS from a local machine, AWS CDK must be setup since that allows us to define our infrastructure as code. Doing so requires following a few steps. Please note, some steps are specific only to windows and can be skipped if the user is running Linux.

* Installing the Linux Subsystem on Windows.
* Downloading VS Code as the IDE and it's extension "WSL-Remote" to run VS Code within the Linux Subsystem.
* Installing Python3.
* Installing the AWS Command Line Interface Version 2 (AWS CLI V2).
* Cloning this Github repository.
* Installing Node Version Manager (NVM) to download and install Node.js and Node Packet Manager (npm) to install Javascript packages.
* Installing the aws-cdk package via NPM.
* Installing and creating a virual environment on the Linux Console and installing the required dependencies.

The deployed code will use three services to show its working:
* The CloudWatch service will contain the logs for every minute the application is deployed and will publish the two Web Health monitoring metrics for each URL: Availability and Latency.
* The CloudWatch service will also display the alarms that will get triggered when either of the metric, for any URL, does not satisfy the specified thresholds.
* The DynamoDB Table will show table entries being created everytime an Alarm is triggered. These entries will provide information regarding the alarm raised.
# How to Run
You go outside. But since we're developers and physically cannot, I will detail below how to run QasimSprint1.

* Configure your AWS
* Within the MoonSprint1 directory, there are two python files that are of importance: 'qasim_sprint1_stack.py' which defines the entire infrastructure that we intend to create and "HelloWorldLambda.py" which is the application [Lambda Function] that we want the Lambda service to run.
* Synthize a template through AWS CDK
* Deploy the CDK template.

# Important Question

## What is Latency?
* Latency describes the amount of delay on a network or Internet connection. Low latency implies that there are no or almost no delays. High latency implies that there are many delays.

## What is Availability?
* Website availability (also called website uptime) refers to the ability of the users to access and use a website or web service.

## What is Boto3 Client?
* Boto3 client is a low-level service class to connect to AWS service. It provides similar methods available in the AWS API. All the methods available in the AWS API are available in the Boto3 client.

Enjoy!
