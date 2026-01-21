"""Observability utilities."""

from aws_lambda_powertools import Logger

SERVICE = "AmazonQuickSuiteStarterKitOperaterTools"
logger = Logger(service=SERVICE)
