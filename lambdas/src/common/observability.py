"""Observability utilities for the Custom Connector Framework."""

from aws_lambda_powertools import Logger, Tracer

SERVICE = "AmazonQuickSuiteStarterKit"
logger = Logger(service=SERVICE)
tracer = Tracer(service=SERVICE)
