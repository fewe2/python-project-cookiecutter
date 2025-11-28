{% if cookiecutter.include_cdk == 'yes' %}# Infrastructure Documentation

!!! warning "Example Setup"
    The infrastructure provided is an **example setup** to showcase the structure and best practices for AWS CDK deployments. It includes a Lambda function with SQS, S3, and CloudWatch integration as a reference implementation.
    
    **You should customize this infrastructure according to your specific use case:**
    
    - Modify resources in `infrastructure/stacks/` to match your requirements
    - Add/remove AWS services as needed
    - Adjust security policies and IAM roles
    - Configure networking (VPC, subnets, security groups)
    - Add monitoring, alarms, and dashboards
    - Implement your business logic in the Lambda handlers
    
    This template provides the foundation - build your actual infrastructure on top of it!

## Overview

This project uses AWS CDK (Cloud Development Kit) for infrastructure as code. The infrastructure is defined in Python and deployed to AWS.

## Viewing Your Infrastructure

!!! tip "Infrastructure as Code = Self-Documenting"
    Your infrastructure is defined in `infrastructure/stacks/` - **the code IS the documentation**. Instead of maintaining separate docs, read the CDK code directly:
    
    ```bash
    # View your stack definition
    cat infrastructure/stacks/*_stack.py
    
    # See what will be deployed
    make cdk-diff
    
    # List all resources
    make cdk-list
    ```

### Example Starting Point

The template includes a basic example with:
- Lambda function with SQS trigger
- S3 bucket for storage
- CloudWatch logging
- IAM roles with least-privilege

**This is just a starting point** - modify `infrastructure/stacks/` to match your needs.

## Environments

The project supports multiple environments:

- **dev**: Development environment
- **staging**: Staging environment (optional)
- **prod**: Production environment
- **feature-***: Feature branch environments

Environment is determined by the `ENVIRONMENT` variable in CI/CD.

## Deployment

### Prerequisites

1. AWS credentials configured
2. AWS CDK CLI installed: `npm install -g aws-cdk`
3. Bootstrap CDK (once per account/region): `make cdk-bootstrap`

### Deploy

```bash
# Set environment
export ENVIRONMENT=dev

# Deploy all stacks
make cdk-deploy

# Or deploy specific stack
cd infrastructure
cdk deploy {{cookiecutter.project_slug}}-dev
```

### View Changes

```bash
make cdk-diff
```

### Destroy

```bash
make cdk-destroy
```

## Understanding Your Stack

### Inspect Deployed Resources

```bash
# View synthesized CloudFormation template
make cdk-synth

# See what resources exist
aws cloudformation describe-stack-resources \
  --stack-name {{cookiecutter.project_slug}}-dev

# View stack outputs
aws cloudformation describe-stacks \
  --stack-name {{cookiecutter.project_slug}}-dev \
  --query 'Stacks[0].Outputs'
```

### CDK Code Structure

Your infrastructure is defined in Python:

```python
# infrastructure/stacks/your_stack.py
class YourStack(Stack):
    def __init__(self, scope, construct_id, **kwargs):
        # All resources defined here
        # Read this file to see what's deployed!
```

**Benefits of Infrastructure as Code:**
- Code is always up-to-date (it's what's deployed)
- Version controlled with Git
- Reviewed in merge requests
- No separate docs to maintain

## CI/CD Deployment

### Automatic Deployments

- **main branch** → prod environment
- **develop branch** → dev environment
- **staging branch** → staging environment

### Feature Branch Deployments

Feature branches can be deployed manually:

1. Create merge request
2. Go to pipeline
3. Click "Play" on `deploy:infrastructure` job
4. Stack name: `{{cookiecutter.project_slug}}-feature-<branch-name>`

### Cleanup

**Manual cleanup** (per MR):
- Click "Stop environment" in GitLab UI

**Scheduled cleanup** (weekly):
- Runs automatically via scheduled pipeline
- Removes stacks for deleted branches

**Manual batch cleanup**:
```bash
make cleanup-branches
```

## Monitoring

### View Logs

```bash
# Tail Lambda logs
aws logs tail /aws/lambda/{{cookiecutter.project_slug}}-dev --follow

# Or use AWS Console
# CloudWatch > Log groups > /aws/lambda/{{cookiecutter.project_slug}}-<env>
```

### Add Monitoring

See the "Customizing" section below for examples of adding:
- CloudWatch Alarms
- Dashboards
- X-Ray tracing

## Cost Management

```bash
# View estimated costs before deployment
make cdk-diff

# Check actual costs in AWS Console
# Cost Explorer > Filter by tag or resource
```

**Cost optimization tips:**
- Use Lambda layers (already configured)
- Set appropriate log retention
- Delete unused feature branch stacks
- Use `make cleanup-branches` regularly

## Troubleshooting

### Deployment Fails

```bash
# Check CDK diff
make cdk-diff

# Check CloudFormation events
aws cloudformation describe-stack-events --stack-name {{cookiecutter.project_slug}}-dev
```

### Lambda Errors

```bash
# View logs
aws logs tail /aws/lambda/{{cookiecutter.project_slug}}-dev --follow

# Check DLQ
aws sqs receive-message --queue-url <dlq-url>
```

### Stack Stuck

```bash
# Force destroy
cd infrastructure
cdk destroy --force
```

## Container Deployment (Alternative)

The project uses ZIP deployment by default. To switch to container deployment:

1. Uncomment the Dockerfile
2. Update CDK stack to use `DockerImageCode`
3. See comments in `Dockerfile` for details

Benefits of containers:
- Larger package size (up to 10GB)
- Include system dependencies
- More control over runtime

## Customizing the Infrastructure

### Common Customizations

**Add API Gateway:**
```python
from aws_cdk import aws_apigateway as apigw

api = apigw.RestApi(self, "Api",
    rest_api_name="My API"
)
api.root.add_method("GET", 
    apigw.LambdaIntegration(self.lambda_function)
)
```

**Add DynamoDB Table:**
```python
from aws_cdk import aws_dynamodb as dynamodb

table = dynamodb.Table(self, "Table",
    partition_key=dynamodb.Attribute(
        name="id",
        type=dynamodb.AttributeType.STRING
    ),
    billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
)
table.grant_read_write_data(self.lambda_role)
```

**Add VPC:**
```python
from aws_cdk import aws_ec2 as ec2

vpc = ec2.Vpc(self, "VPC",
    max_azs=2,
    nat_gateways=1
)

# Update Lambda to use VPC
self.lambda_function = lambda_.Function(
    # ... other props
    vpc=vpc,
    vpc_subnets=ec2.SubnetSelection(
        subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
    )
)
```

**Add CloudWatch Alarms:**
```python
from aws_cdk import aws_cloudwatch as cloudwatch

alarm = cloudwatch.Alarm(self, "ErrorAlarm",
    metric=self.lambda_function.metric_errors(),
    threshold=10,
    evaluation_periods=1,
    alarm_description="Lambda errors exceeded threshold"
)
```

### File Structure for Custom Resources

```
infrastructure/
├── app.py                    # CDK app entry point
├── stacks/
│   ├── __init__.py
│   ├── main_stack.py        # Your main stack (customize this)
│   ├── database_stack.py    # Add separate stacks as needed
│   ├── network_stack.py     # VPC, subnets, etc.
│   └── monitoring_stack.py  # Alarms, dashboards
└── constructs/              # Reusable CDK constructs
    ├── __init__.py
    └── custom_construct.py
```

### Best Practices

1. **Separate stacks by lifecycle** - Database, networking, and application stacks
2. **Use constructs for reusability** - Create custom constructs for repeated patterns
3. **Parameterize configurations** - Use environment variables and context
4. **Tag all resources** - For cost tracking and organization
5. **Enable CloudTrail** - For audit logging
6. **Use CDK aspects** - For cross-cutting concerns (tagging, compliance)

### Resources

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [CDK Patterns](https://cdkpatterns.com/)
- [AWS Solutions Constructs](https://aws.amazon.com/solutions/constructs/)
{% endif %}
