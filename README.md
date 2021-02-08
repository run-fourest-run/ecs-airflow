# Astronomer Airflow Demo
Airflow Deployed on Amazon ECS using Teradata/shell deployment scripts.  forked from https://github.com/nicor88/aws-ecs-airflow. Additional changes were made from the original repository in order for me to make the demo work (source changes in terraform,shell,dockerfiles files)


# DAG demonstration

Demo pipeline/workflow represented by DAG definition file will source/fetch data from RapidAPI's yahoo finance endpoints & post to S3 and ideally Redshift from there. There are also some tasks that build the underlying data storage elements (buckets, sql tables, etc.) 





## Requirements

### Local
* Docker

### AWS
* AWS IAM User for the infrastructure deployment, with admin permissions
* [awscli](https://aws.amazon.com/cli/), intall running `pip install awscli`
* [terraform >= 0.13](https://www.terraform.io/downloads.html)
* setup your IAM User credentials inside `~/.aws/credentials`
* setup these env variables in your .zshrc or .bashrc, or in your the terminal session that you are going to use
  <pre>
  export AWS_ACCOUNT=your_account_id
  export AWS_DEFAULT_REGION=us-east-1 # it's the default region that needs to be setup also in infrastructure/config.tf
  </pre>


## Local Development
* Generate a Fernet Key:
  <pre>
  pip install cryptography
  export AIRFLOW_FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
  </pre>
  More about that [here](https://cryptography.io/en/latest/fernet/)

* Start Airflow locally simply running:
  <pre>
  docker-compose up --build
  </pre

If everything runs correctly you can reach Airflow navigating to [localhost:8080](http://localhost:8080).
The current setup is based on [Celery Workers](https://airflow.apache.org/howto/executor/use-celery.html). You can monitor how many workers are currently active using Flower, visiting [localhost:5555](http://localhost:5555)

## Deploy Airflow on AWS ECS
To run Airflow in AWS we will use ECS (Elastic Container Service).

### Deploy Infrastructure using Terraform
Run the following commands:
<pre>
make infra-init
make infra-plan
make infra-apply
</pre>

or alternatively
<pre>
cd infrastructure
terraform get
terraform init -upgrade;
terraform plan
terraform apply
</pre>

By default the infrastructure is deployed in `us-east-1`.

When the infrastructure is provisioned (the RDS metadata DB will take a while) check the if the ECR repository is created then run:
<pre>
bash scripts/push_to_ecr.sh airflow-dev
</pre>
By default the repo name created with terraform is `airflow-dev`
Without this command the ECS services will fail to fetch the `latest` image from ECR

### Deploy new Airflow application
To deploy an update version of Airflow you need to push a new container image to ECR.
You can simply doing that running:
<pre>
./scripts/deploy.sh airflow-dev
</pre>

The deployment script will take care of:
* push a new ECR image to your repository
* re-deploy the new ECS services with the updated image

