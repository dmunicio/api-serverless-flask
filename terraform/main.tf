provider "aws" {
  version = "~> 3.58.0"
}

# Aurora 
module "aurora" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "~> 3.0"

  name                            = "app-db"
  engine                          = "aurora-postgresql"

  engine_mode           = "serverless"
  engine_version        = null
  replica_scale_enabled = false
  replica_count         = 0

  backtrack_window = 10 # ignored in serverless

  #subnets             = data.aws_subnet_ids.all.ids
  #vpc_id              = data.aws_vpc.default.id
  #subnets             = "module.lambda_api_gateway.private_subnet_ids"
  subnets             = module.lambda_api_gateway.private_subnet_ids
  vpc_id              = module.lambda_api_gateway.vpc_id
  monitoring_interval = 60
  skip_final_snapshot = true
  instance_type       = "db.t4g.small" # ignored for serverless
  apply_immediately   = true
  storage_encrypted   = true
  create_random_password = false
  username            = var.db_user
  password            = var.db_pass
  database_name       = "users"
  port                = 5432

  # PostgreSQL
  db_parameter_group_name         = aws_db_parameter_group.aurora_db_postgresql10_parameter_group.id
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.aurora_cluster_postgresql10_parameter_group.id

  scaling_configuration = {
    auto_pause               = true
    min_capacity             = 2
    max_capacity             = 16
    seconds_until_auto_pause = 300
    timeout_action           = "ForceApplyCapacityChange"
  }
}

# PostgreSQL
resource "aws_db_parameter_group" "aurora_db_postgresql10_parameter_group" {
  name        = "test-postgresql10-parameter-group"
  family      = "aurora-postgresql10"
  description = "test-postgresql10-parameter-group"
}

resource "aws_rds_cluster_parameter_group" "aurora_cluster_postgresql10_parameter_group" {
  name        = "test-postgresql10-cluster-parameter-group"
  family      = "aurora-postgresql10"
  description = "test-postgresql10-cluster-parameter-group"
}

resource "aws_security_group" "app_servers" {
  name        = "app-servers"
  description = "For application servers"
  vpc_id      = module.lambda_api_gateway.vpc_id
}

#resource "aws_security_group_rule" "allow_access" {
#  type                     = "ingress"
#  from_port                = 5432
#  to_port                  = 5432
#  protocol                 = "tcp"
#  source_security_group_id = aws_security_group.app_servers.id
#  security_group_id        = "sg-aurora"
#}

# Lambda & API Gateway 
module "lambda_api_gateway" {
  source = "github.com/dmunicio/terraform-aws-lambda-api-gateway"
  # tags
  project    = "${var.project}"
  service    = "${var.service}"
  owner      = "${var.owner}"
  costcenter      = ""

  # vpc
  vpc_cidr             = "${var.vpc_cidr}"
  public_subnets_cidr  = "${var.public_subnets_cidr}"
  private_subnets_cidr = "${var.private_subnets_cidr}"
  nat_cidr             = "${var.nat_cidr}"
  igw_cidr             = "${var.igw_cidr}"
  azs                  = "${var.azs}"

  # lambda
  lambda_zip_path      = "${var.lambda_zip_path}"
  lambda_handler       = "${var.lambda_handler}"
  lambda_runtime       = "${var.lambda_runtime}"
  lambda_function_name = "${var.lambda_function_name}"

  # API gateway
  region     = "${var.region}"

  database_uri = "postgresql+psycopg2://${var.db_user}:${var.db_pass}@${module.aurora.this_rds_cluster_endpoint}:5432/users"
}
