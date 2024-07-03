#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { getEnvironmentConfig, CoreEnvironmentConfig } from "../environment";
import { InfrastructureStack } from "../lib/infrastructure-stack";

const app = new cdk.App();
const envConfig: CoreEnvironmentConfig = getEnvironmentConfig();
const env: cdk.Environment = envConfig.env;

console.log(envConfig);

const infrastructureStack = new InfrastructureStack(app, "RAGPipelineStack", {
  env,
  envConfig,
  stackName: "RAGPipeline",
  description: "RAG Piplines",
  containerPort: 8000,
});
