#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { getEnvironmentConfig, CoreEnvironmentConfig } from "../environment";
import { InfrastructureStack } from "../lib/infrastructure-stack";

const app = new cdk.App();
const envConfig: CoreEnvironmentConfig = getEnvironmentConfig();
const env: cdk.Environment = envConfig.env;

console.log(envConfig);

const infrastructureStack = new InfrastructureStack(app, "FileIngestorStack", {
  env,
  envConfig,
  stackName: "NucleusAPI",
  description:
    "Sets up the basic infrastructure for Nucleus AI agent as API Services.",
  containerPort: 8000,
});
