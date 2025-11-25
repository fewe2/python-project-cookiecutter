"""Main application stack."""
{% if cookiecutter.include_cdk == 'yes' %}
from typing import Any

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_logs as logs,
    aws_ssm as ssm,
)
from constructs import Construct


class {{cookiecutter.package_name.title().replace('_', '')}}Stack(Stack):
    """Main application stack with infrastructure example."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        environment_name: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.environment_name = environment_name

        # VPC with public and private subnets
        self.vpc = ec2.Vpc(
            self,
            "VPC",
            max_azs=2,
            nat_gateways=1 if environment_name == "prod" else 0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS if environment_name == "prod" else ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
            ],
        )

        # ECS Cluster
        self.cluster = ecs.Cluster(
            self,
            "Cluster",
            vpc=self.vpc,
            container_insights=True,
        )

        # CloudWatch Log Group
        self.log_group = logs.LogGroup(
            self,
            "LogGroup",
            log_group_name=f"/aws/ecs/{{cookiecutter.project_slug}}-{environment_name}",
            retention=logs.RetentionDays.ONE_WEEK if environment_name != "prod" else logs.RetentionDays.ONE_MONTH,
            removal_policy=cdk.RemovalPolicy.DESTROY if environment_name != "prod" else cdk.RemovalPolicy.RETAIN,
        )

        # Fargate Service with Application Load Balancer
        self.fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "FargateService",
            cluster=self.cluster,
            memory_limit_mib=512 if environment_name != "prod" else 1024,
            cpu=256 if environment_name != "prod" else 512,
            desired_count=1 if environment_name != "prod" else 2,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("../"),
                container_port=8000,
                log_driver=ecs.LogDrivers.aws_logs(
                    stream_prefix="{{cookiecutter.package_name}}",
                    log_group=self.log_group,
                ),
                environment={
                    "ENVIRONMENT": environment_name,
                    "LOG_LEVEL": "INFO" if environment_name == "prod" else "DEBUG",
                },
            ),
            public_load_balancer=True,
            enable_logging=True,
        )

        # Health check configuration
        self.fargate_service.target_group.configure_health_check(
            path="/health",
            healthy_http_codes="200",
        )

        # Auto Scaling
        scalable_target = self.fargate_service.service.auto_scale_task_count(
            min_capacity=1 if environment_name != "prod" else 2,
            max_capacity=2 if environment_name != "prod" else 10,
        )

        scalable_target.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=70,
        )

        scalable_target.scale_on_memory_utilization(
            "MemoryScaling",
            target_utilization_percent=80,
        )

        # Store important values in SSM Parameter Store
        ssm.StringParameter(
            self,
            "LoadBalancerUrl",
            parameter_name=f"/{{cookiecutter.project_slug}}/{environment_name}/load-balancer-url",
            string_value=self.fargate_service.load_balancer.load_balancer_dns_name,
        )

        # Outputs
        cdk.CfnOutput(
            self,
            "LoadBalancerDNS",
            value=self.fargate_service.load_balancer.load_balancer_dns_name,
            description="Load Balancer DNS Name",
        )

        cdk.CfnOutput(
            self,
            "ServiceUrl",
            value=f"http://{self.fargate_service.load_balancer.load_balancer_dns_name}",
            description="Service URL",
        )
{% endif %}