import { Environment as CdkEnvironment, StackProps } from "aws-cdk-lib";

/**
 * Environment config.
 * @alpha
 */
export interface CoreEnvironmentConfig extends StackProps {
  /**
   * Name of the environment.
   */
  readonly name: string;
  /**
   * Cdk environment.
   */
  readonly env: CdkEnvironment;
}

/**
 * Core stack props.
 * @alpha
 */
export interface CoreStackProps extends StackProps {
  envConfig: CoreEnvironmentConfig;
}

export const getEnvironmentName = (): string => {
  return process.env.ENV_NAME || "sandbox"; // Will be useful when we have multi-environment
};

export const getDeploymentStackName = (stackName: string): string => {
  const prefix = getDeploymentEnvironmentName();
  return `${prefix}${stackName}`;
};

export const getDeploymentEnvironmentName = (): string => {
  return process.env.DEPLOY_ENV || getEnvironmentName();
};

export function getEnvironmentConfig(): CoreEnvironmentConfig {
  const envName = getEnvironmentName();
  const envConfig: CoreEnvironmentConfig = Environment[envName];

  if (!envConfig) {
    throw new Error(`No environment config found for ${envName}`);
  }

  return envConfig;
}

// We can use this to define configurations per environments.
export const Environment: { [key: string]: CoreEnvironmentConfig } = {
  sandbox: {
    name: "sandbox",
    env: {
      region: "us-east-1",
      account: "654654323576",
    },
  },
};
