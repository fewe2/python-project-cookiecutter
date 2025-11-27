"""Main application stack with Lambda, SQS, and S3."""
{% if cookiecutter.include_cdk == 'yes' %}
from typing import Any

import aws_cdk as cdk
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_lambda_event_sources as lambda_event_sources,
    aws_logs as logs,
    aws_s3 as s3,
    aws_sqs as sqs,
    aws_ssm as ssm,
)
from constructs import Construct


class {{cookiecutter.package_name.title().replace('_', '')}}Stack(Stack):
    """Main application stack. Example with Lambda, SQS, and S3."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        environment_name: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.environment_name = environment_name

        # S3 Bucket for data storage
        self.bucket = s3.Bucket(
            self,
            "DataBucket",
            bucket_name=f"{{cookiecutter.project_slug}}-{environment_name}-data-{cdk.Aws.ACCOUNT_ID}",
            versioned=environment_name == "prod",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=cdk.RemovalPolicy.DESTROY if environment_name != "prod" else cdk.RemovalPolicy.RETAIN,
            auto_delete_objects=environment_name != "prod",
        )

        # Dead Letter Queue
        self.dlq = sqs.Queue(
            self,
            "DeadLetterQueue",
            queue_name=f"{{cookiecutter.project_slug}}-{environment_name}-dlq",
            retention_period=Duration.days(14),
        )

        # SQS Queue
        self.queue = sqs.Queue(
            self,
            "ProcessingQueue",
            queue_name=f"{{cookiecutter.project_slug}}-{environment_name}-queue",
            visibility_timeout=Duration.minutes(5),
            dead_letter_queue=sqs.DeadLetterQueue(
                max_receive_count=3,
                queue=self.dlq,
            ),
        )

        # CloudWatch Log Group
        self.log_group = logs.LogGroup(
            self,
            "LogGroup",
            log_group_name=f"/aws/lambda/{{cookiecutter.project_slug}}-{environment_name}",
            retention=logs.RetentionDays.ONE_WEEK if environment_name != "prod" else logs.RetentionDays.ONE_MONTH,
            removal_policy=cdk.RemovalPolicy.DESTROY if environment_name != "prod" else cdk.RemovalPolicy.RETAIN,
        )

        # Lambda execution role
        self.lambda_role = iam.Role(
            self,
            "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            ],
        )

        # Grant S3 permissions
        self.bucket.grant_read_write(self.lambda_role)

        # Grant SQS permissions
        self.queue.grant_consume_messages(self.lambda_role)
        self.dlq.grant_send_messages(self.lambda_role)

        # Lambda layer for dependencies (production only)
        self.dependencies_layer = lambda_.LayerVersion(
            self,
            "DependenciesLayer",
            code=lambda_.Code.from_asset(
                "../",
                bundling=cdk.BundlingOptions(
                    image=lambda_.Runtime.PYTHON_{{cookiecutter.python_version.replace('.', '_').upper()}}.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "pip install . --target /asset-output/python",
                    ],
                ),
            ),
            compatible_runtimes=[lambda_.Runtime.PYTHON_{{cookiecutter.python_version.replace('.', '_').upper()}}],
            description=f"Dependencies for {environment_name}",
        )

        # Lambda function
        self.lambda_function = lambda_.Function(
            self,
            "ProcessorFunction",
            function_name=f"{{cookiecutter.project_slug}}-{environment_name}-processor",
            runtime=lambda_.Runtime.PYTHON_{{cookiecutter.python_version.replace('.', '_').upper()}},
            handler="handlers.processor.handler",
            code=lambda_.Code.from_asset("../src"),
            role=self.lambda_role,
            layers=[self.dependencies_layer],
            timeout=Duration.minutes(5),
            memory_size=256 if environment_name != "prod" else 512,
            log_group=self.log_group,
            environment={
                "ENVIRONMENT": environment_name,
                "LOG_LEVEL": "INFO" if environment_name == "prod" else "DEBUG",
                "BUCKET_NAME": self.bucket.bucket_name,
                "QUEUE_URL": self.queue.queue_url,
            },
        )

        # SQS event source for Lambda
        self.lambda_function.add_event_source(
            lambda_event_sources.SqsEventSource(
                self.queue,
                batch_size=10 if environment_name == "prod" else 5,
                max_batching_window=Duration.seconds(5),
            )
        )

        # Store important values in SSM Parameter Store
        ssm.StringParameter(
            self,
            "BucketName",
            parameter_name=f"/{{cookiecutter.project_slug}}/{environment_name}/bucket-name",
            string_value=self.bucket.bucket_name,
        )

        ssm.StringParameter(
            self,
            "QueueUrl",
            parameter_name=f"/{{cookiecutter.project_slug}}/{environment_name}/queue-url",
            string_value=self.queue.queue_url,
        )

        ssm.StringParameter(
            self,
            "LambdaArn",
            parameter_name=f"/{{cookiecutter.project_slug}}/{environment_name}/lambda-arn",
            string_value=self.lambda_function.function_arn,
        )

        # Outputs
        cdk.CfnOutput(
            self,
            "BucketName",
            value=self.bucket.bucket_name,
            description="S3 Bucket Name",
        )

        cdk.CfnOutput(
            self,
            "QueueUrl",
            value=self.queue.queue_url,
            description="SQS Queue URL",
        )

        cdk.CfnOutput(
            self,
            "LambdaFunctionArn",
            value=self.lambda_function.function_arn,
            description="Lambda Function ARN",
        )
{% endif %}