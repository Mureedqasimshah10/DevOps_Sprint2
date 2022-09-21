from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    RemovalPolicy,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_cloudwatch as cloudwatch_,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_cloudwatch_actions as cw_actions_,
    aws_sns_subscriptions as subscriptions_,
    aws_dynamodb as dynamodb_,
    )
from constructs import Construct
from resources import constants as constants
class Sprint2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Creating my lambda function for deploying hw_lambda.py function 
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html
        # Adding removal Policy for the function
        lambda_role = self.create_lambda_role()
        hw_lambda = self.create_lambda("MyFirstLambda", "hw_lambda.lambda_handler", "./resources", lambda_role)
        hw_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        


        # Creating another lambda funciton for structuring the data to put into Dynamo Database
        # Adding removal Policy for the function
        db_lambda = self.create_lambda("QasimDynamoDBLambda", "DynamoDBLambda.lambda_handler", "./resources", lambda_role)
        # db_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        
        # Create a dynamo db table in stack
        # Creating the enviornment variable and passing the parameters
        DBTable = self.create_table()
        tname = DBTable.table_name
        db_lambda.add_environment(key="Alarm_key", value=tname)
        

        # Defining an event 
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Schedule.html
        # Generating event every one minute
        schedule = events_.Schedule.cron()
        # Defining the target for our lambda function and the event
        target = targets_.LambdaFunction(handler=hw_lambda)
        rule = events_.Rule(self, "LambdaEventRule",
        description="This is my rule for generation of auto event for my hw_lambda function",
        schedule=schedule,
        targets=[target]
        )
        
        
        # Creating my SNS topic (i.e. message server to connect with alarm for notification)
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns/Topic.html
        topic = sns_.Topic(self, "Alarmnotification")
    
        
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
        email_address = "qasim.shah.skipq@gmail.com"
        topic.add_subscription(subscriptions_.EmailSubscription(email_address))
        
        
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/LambdaSubscription.html
        topic.add_subscription(subscriptions_.LambdaSubscription(db_lambda))


        for url in constants.URL_TO_MONITOR:
            # Define thrashold and creat alrams
            dimensions={"URL": url}
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
            availMetric = cloudwatch_.Metric(metric_name=constants.URL_MONITOR_METRIC_NAME_AVAILABILITY, 
            namespace=constants.URL_MONITOR_NAMESPACE,  
            dimensions_map=dimensions,
            period=Duration.minutes(1) 
            )
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
            availAlarm = cloudwatch_.Alarm(self, "AvailabilityAlarm"+url,
                comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                threshold=1,
                evaluation_periods=1,
                metric=availMetric
            )
            #  https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            # Configuring alarm with notification services
            availAlarm.add_alarm_action(cw_actions_.SnsAction(topic))



            # Define thrashold and creat alrams
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
            latencyMetric = cloudwatch_.Metric(metric_name=constants.URL_MONITOR_METRIC_NAME_LATENCY, 
            namespace=constants.URL_MONITOR_NAMESPACE,  
            dimensions_map=dimensions,
            period=Duration.minutes(1) 
            )
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
            latencyAlarm = cloudwatch_.Alarm(self, "LatencyAlarm"+url,
                threshold=0.3,
                evaluation_periods=1,
                metric=latencyMetric
            )
            #  https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            # Configuring alarm with notification services
            latencyAlarm.add_alarm_action(cw_actions_.SnsAction(topic))
 
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html
    def create_lambda(self, id_, handler, path, my_role):
        return lambda_.Function(self, id_,
        runtime=lambda_.Runtime.PYTHON_3_8,
        handler=handler,
        code=lambda_.Code.from_asset(path), 
        role= my_role,
        timeout=Duration.seconds(25)
    )
    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html
    def create_lambda_role(self):
        lambda_role = iam_.Role(self, "lambda_role",
        assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
        managed_policies=[ 
                            iam_.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                            iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess')
                        ]
        
    )
        return lambda_role  
    def create_table(self):
        return dynamodb_.Table(self, "AlarmInfoTable",
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Attribute.html#aws_cdk.aws_dynamodb.Attribute
        partition_key = dynamodb_.Attribute(name="AlarmName", type=dynamodb_.AttributeType.STRING),
        # sort_key = dynamodb_.Attribute(name="AlarmTime", type=dynamodb_.AttributeType.STRING),
        removal_policy = RemovalPolicy.DESTROY
    )
