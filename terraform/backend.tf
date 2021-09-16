terraform {
  required_version = ">= 0.13.0"
  backend "s3" {
    key    = "tfstate"
  }
}

