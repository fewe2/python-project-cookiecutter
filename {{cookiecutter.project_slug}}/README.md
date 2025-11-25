# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Setup

### With Make (Linux/macOS)
```bash
make install
source .venv/bin/activate
```

### Without Make (Windows/Manual)
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install
```

## Usage

{% if cookiecutter.include_cdk == 'yes' %}### Local Development
```bash
# Run development server
make dev-server
# Or manually:
python -m {{cookiecutter.package_name}}
```

The API will be available at http://localhost:8000
- Root endpoint: http://localhost:8000/
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs

### Docker
```bash
# Build and run with Docker
make docker-build
make docker-run
```
{% else %}```bash
# Run the main module (recommended)
python -m {{cookiecutter.package_name}}

# Or run directly (not recommended - may break relative imports)
python src/{{cookiecutter.package_name}}/main.py
```
{% endif %}

## Development

### With Make (Linux/macOS)
- `make test` - Run tests
- `make lint` - Run linting
- `make format` - Format code
- `make type-check` - Run type checking
- `make shell` - Activate virtual environment

### Without Make (Windows/Manual)
- `pytest` - Run tests
- `ruff check .` - Run linting
- `ruff format .` - Format code
- `mypy src/` - Run type checking
- `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/macOS) - Activate virtual environment{% if cookiecutter.include_cdk == 'yes' %}

## AWS Deployment

### Prerequisites
- AWS CLI configured with appropriate credentials
- AWS CDK CLI installed: `npm install -g aws-cdk`

### Deploy to AWS

```bash
# Bootstrap CDK (run once per account/region)
make cdk-bootstrap

# Deploy infrastructure
make cdk-deploy
```

### CDK Commands
- `make cdk-synth` - Generate CloudFormation templates
- `make cdk-diff` - Show differences before deployment
- `make cdk-deploy` - Deploy all stacks
- `make cdk-destroy` - Destroy all stacks

### Manual CDK Commands (Windows)
```bash
cd infrastructure
python -m pip install -e ".[cdk]"
cdk bootstrap
cdk deploy --all
```

### Deployment Strategy

The template uses a **hybrid deployment strategy**:

- **Main branches** (main/master/develop/staging) → Fixed environments (prod/dev/staging)
- **Feature branches** → Dynamic stacks with `feature-` prefix
- Automatic branch detection and stack naming
- Safe isolation for feature development

### Branch Management
```bash
# Deploy current branch
make cdk-deploy

# Cleanup current branch stack
make cdk-cleanup-branch

# Cleanup orphaned feature branch stacks
make cleanup-branches

# List all stacks
make cdk-list
```

### Architecture

The CDK stack creates:
- **VPC** with public/private subnets
- **ECS Fargate** service with auto-scaling
- **Application Load Balancer** for traffic distribution
- **CloudWatch** logging and monitoring
- **Multi-environment** support with branch-based isolation

### Environment Variables
- `ENVIRONMENT` - Current environment (dev/staging/prod)
- `LOG_LEVEL` - Logging level (DEBUG/INFO/WARNING/ERROR)
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)

## CI/CD Pipeline

The project includes a comprehensive GitLab CI/CD pipeline with:

### Test Stage
- **Unit Tests** - pytest with coverage reporting
- **Code Quality** - ruff linting and formatting
- **Type Checking** - mypy static analysis
- **Security Scanning** - detect-secrets and dependency vulnerability checks

### Build Stage
- **Docker Image** - Multi-stage build and push to ECR
- **Infrastructure** - CDK synthesis and validation

### Deploy Stage
- **Automatic Deployment** - main/develop/staging branches
- **Feature Branch Deployment** - Manual deployment for testing
- **Production Approval** - Manual approval required for production
- **Cleanup** - Automatic cleanup of feature branch resources

### Required GitLab Variables
- `AWS_ACCOUNT_ID` - AWS Account ID
- `AWS_ACCESS_KEY_ID` - AWS Access Key (or use IAM roles)
- `AWS_SECRET_ACCESS_KEY` - AWS Secret Key (or use IAM roles)
- `PYPI_TOKEN` - PyPI token for package publishing (non-CDK projects)

### Branch Strategy
- `main` → Production environment
- `develop` → Development environment
- `staging` → Staging environment
- Feature branches → Isolated feature environments (manual deployment)
{% endif %}

{% if cookiecutter.include_cdk != 'yes' %}## CI/CD Pipeline

The project includes a GitLab CI/CD pipeline with:

### Test Stage
- **Unit Tests** - pytest with coverage reporting
- **Code Quality** - ruff linting and formatting
- **Type Checking** - mypy static analysis
- **Security Scanning** - detect-secrets and dependency vulnerability checks

### Build Stage
- **Package Build** - Python wheel and source distribution
- **Documentation** - MkDocs documentation build

### Deploy Stage
- **PyPI Publishing** - Manual deployment for releases
- **Documentation** - Automatic deployment to GitLab Pages

### Required GitLab Variables
- `PYPI_TOKEN` - PyPI token for package publishing

{% endif %}## License

{{cookiecutter.license}}