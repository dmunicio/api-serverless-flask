output "api_url" {
  value = "${module.lambda_api_gateway.api_url}"
}

output "lambda_zip" {
  value = "${module.lambda_api_gateway.lambda_zip}"
}
