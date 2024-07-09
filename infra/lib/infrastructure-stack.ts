import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as ecs from "aws-cdk-lib/aws-ecs";
import { PrivateDnsNamespace } from "aws-cdk-lib/aws-servicediscovery";
import * as log from "aws-cdk-lib/aws-logs";
import * as iam from "aws-cdk-lib/aws-iam";
import * as ecr from "aws-cdk-lib/aws-ecr";
import { CoreStackProps } from "../environment";
import * as elbv2 from "aws-cdk-lib/aws-elasticloadbalancingv2";
import * as apigw from "aws-cdk-lib/aws-apigatewayv2";

interface InfrastructureStackProps extends CoreStackProps {
  containerPort: number;
}

export class InfrastructureStack extends cdk.Stack {
  public readonly httpVpcLink: cdk.CfnResource;
  public readonly httpApiListener: elbv2.ApplicationListener;

  constructor(scope: Construct, id: string, props: InfrastructureStackProps) {
    super(scope, id, props);

    const { containerPort } = props;

    // VPC
    const vpc = new ec2.Vpc(this, "VPC");

    // ECS Cluster
    const ecsCluster = new ecs.Cluster(this, "FGCluster", {
      vpc,
    });

    // CloudMap Namespace
    const dnsNamespace = new PrivateDnsNamespace(this, "DNSNamespace", {
      name: "esgene-api.local",
      vpc,
      description: "Private DNS Namespace for ESGene API",
    });

    // Task Role
    const taskRole = new iam.Role(this, "ecsTaskExecutionRole", {
      assumedBy: new iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
    });
    taskRole.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName(
        "service-role/AmazonECSTaskExecutionRolePolicy"
      )
    );

    // Task Definitions
    const taskDef = new ecs.FargateTaskDefinition(
      this,
      "esgeneTaskDefinition",
      {
        memoryLimitMiB: 512,
        cpu: 256,
        taskRole: taskRole,
      }
    );

    // Log Groups
    const logGroup = new log.LogGroup(this, "esgeneLogGroup", {
      logGroupName: "/ecs/esgene",
      retention: log.RetentionDays.ONE_WEEK,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const logDriver = new ecs.AwsLogDriver({
      logGroup: logGroup,
      streamPrefix: "ESGeneService",
    });

    // ECR Repository
    const ecRRepo = ecr.Repository.fromRepositoryName(
      this,
      "esgeneECRRepo",
      "esgene-rag" // replace with your repository name
    );

    // Task Container
    const container = taskDef.addContainer("esgeneContainer", {
      image: ecs.ContainerImage.fromRegistry(
        "public.ecr.aws/y9j1k7y7/esgene-rag:1.0.0"
      ),
      memoryLimitMiB: 512,
      logging: logDriver,
    });

    container.addPortMappings({
      containerPort,
    });

    // Security Groups
    const securityGroup = new ec2.SecurityGroup(this, "SecurityGroup", {
      allowAllOutbound: true,
      securityGroupName: "sg",
      vpc: vpc,
    });
    securityGroup.connections.allowFromAnyIpv4(ec2.Port.tcp(containerPort));

    // Fargate Service
    const fargateService = new ecs.FargateService(this, "esgeneService", {
      cluster: ecsCluster,
      taskDefinition: taskDef,
      assignPublicIp: false,
      desiredCount: 2,
      securityGroups: [securityGroup],
      cloudMapOptions: {
        name: "esgeneService",
        cloudMapNamespace: dnsNamespace,
      },
    });

    // ALB
    const lb = new elbv2.ApplicationLoadBalancer(this, "ESGeneALB", {
      vpc,
      internetFacing: false,
    });
    this.httpApiListener = lb.addListener("httpapiListener", {
      port: containerPort,
      // Default Target Group
      defaultAction: elbv2.ListenerAction.fixedResponse(200),
    });

    // Target Group
    const targetGroup = this.httpApiListener.addTargets("esgeneTargetGroup", {
      port: containerPort,
      targets: [fargateService],
      healthCheck: {
        path: "/health",
        interval: cdk.Duration.seconds(30),
        timeout: cdk.Duration.seconds(5),
        healthyThresholdCount: 2,
      },
    });

    // VPC Link
    this.httpVpcLink = new cdk.CfnResource(this, "httpVpcLink", {
      type: "AWS::ApiGatewayV2::VpcLink",
      properties: {
        Name: "http-api-vpc-link",
        SecurityGroupIds: [securityGroup.securityGroupId],
        SubnetIds: vpc.privateSubnets.map((subnet) => subnet.subnetId),
      },
    });

    // Consumer VPC
    const consumerVpc = new ec2.Vpc(this, "ConsumerVPC", {
      natGateways: 0,
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: "ingress",
          subnetType: ec2.SubnetType.PUBLIC,
        },
      ],
    });

    // Security Group
    const bastionSecurityGroup = new ec2.SecurityGroup(
      this,
      "BastionSecurityGroup",
      {
        allowAllOutbound: true,
        securityGroupName: "sgbastion",
        vpc: consumerVpc,
      }
    );

    bastionSecurityGroup.connections.allowFromAnyIpv4(ec2.Port.tcp(22));

    // AMI
    const amznLinux = new ec2.AmazonLinuxImage({
      generation: ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
      edition: ec2.AmazonLinuxEdition.STANDARD,
      virtualization: ec2.AmazonLinuxVirt.HVM,
      storage: ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
    });

    // Instance
    const bastionHost = new ec2.Instance(this, "BastionHost", {
      instanceType: new ec2.InstanceType("t3.nano"),
      machineImage: amznLinux,
      vpc: consumerVpc,
      securityGroup: bastionSecurityGroup,
    });

    // HTTP API
    const httpApi = new apigw.HttpApi(this, "HTTPAPI", {
      createDefaultStage: true,
    });

    // API Integration
    const apiIntegration = new apigw.CfnIntegration(
      this,
      "HttpAPIGWIntegration",
      {
        apiId: httpApi.httpApiId,
        connectionType: "VPC_LINK",
        connectionId: this.httpVpcLink.ref,
        integrationType: "HTTP_PROXY",
        integrationMethod: "ANY",
        integrationUri: this.httpApiListener.listenerArn,
        payloadFormatVersion: "1.0",
      }
    );

    // API Route
    new apigw.CfnRoute(this, "HttpAPIRoute", {
      apiId: httpApi.httpApiId,
      routeKey: "ANY /{proxy+}",
      target: `integrations/${apiIntegration.ref}`,
    });

    // EC2 IP Address
    new cdk.CfnOutput(this, "BastionHostPublicIP", {
      value: bastionHost.instancePublicIp,
    });

    // API Service Endpoints
    const httpApiEndpoint = httpApi.apiEndpoint;
    const coreApiEndpoint = `${httpApiEndpoint}`;

    new cdk.CfnOutput(this, "Core API ", {
      value: coreApiEndpoint,
    });
  }
}
