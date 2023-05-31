import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    region = os.environ['region']
    default_tag_key = os.environ['Default_Tag_Key']
    default_tag_value = os.environ['Default_Tag_Value']
    rds_comm_tag_value = os.environ['RDS_Comm_Tag_Vaule']
    rds_non_comm_tag_value = os.environ['RDS_Non_Comm_Tag_Vaule']

    detail = event['detail']
    event_name = detail['eventName']
    comm_engine = ['oracle-ee', 'oracle-ee-cdb', 'oracle-se2', 'oracle-se2-cdb', 'custom-oracle-ee', 'custom-oracle-ee-cdb', 'custom-sqlserver-ee', 'custom-sqlserver-se', 'custom-sqlserver-web', 'sqlserver-ee', 'sqlserver-se', 'sqlserver-ex', 'sqlserver-web', 'aurora-mysql', 'aurora-postgresql']
    non_comm_engine = ['mysql', 'postgres', 'mariadb']

    if event_name == 'RunInstances':
        instance_ids = [item['instanceId'] for item in detail['responseElements']['instancesSet']['items']]
        logger.info('Number of instances: ' + str(len(instance_ids)))

        ec2 = boto3.resource('ec2', region_name=region)

        for instance_id in instance_ids:
            logger.info('Tagging resource ' + instance_id)
            instance = ec2.Instance(instance_id)
            instance.create_tags(Tags=[{'Key': default_tag_key, 'Value': default_tag_value}])

            for volume in instance.volumes.all():
                logger.info('Tagging EBS volume ' + volume.id)
                volume.create_tags(Tags=[{'Key': default_tag_key, 'Value': default_tag_value}])
    
    elif event_name == "CreateVolume":
        ec2 = boto3.client('ec2', region_name=region)
        volume_id = detail['responseElements']['volumeId']
        logger.info(f'Tagging EBS volume {volume_id}')
        ec2.create_tags(Resources=[volume_id], Tags=[{'Key': default_tag_key, 'Value': default_tag_value}])
    
    elif event_name == 'CreateBucket':
        s3 = boto3.client('s3', region_name=region)
        bucket_name = detail['requestParameters']['bucketName']
        logger.info('Tagging S3 bucket ' + bucket_name)
        s3.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={'TagSet': [{'Key': default_tag_key, 'Value': default_tag_value}]}
        )
    
    elif event_name == 'CreateDBInstance':
        rds = boto3.client('rds', region_name=region)

        db_instance_arn = detail['responseElements']['dBInstanceArn']
        logger.info(f'Tagging RDS instance {db_instance_arn}')

        engine = detail['responseElements']['engine']
        
        if engine in non_comm_engine:
            rds_tag_value = rds_non_comm_tag_value
        elif engine in comm_engine:
            rds_tag_value = rds_comm_tag_value
        else:
            rds_tag_value = rds_non_comm_tag_value

        rds.add_tags_to_resource(ResourceName=db_instance_arn, Tags=[{'Key': default_tag_key, 'Value': rds_tag_value}])
    
    elif event_name == 'CreateDBCluster':
        rds = boto3.client('rds', region_name=region)

        db_cluster_arn = detail['responseElements']['dBClusterArn']
        logger.info(f'Tagging RDS cluster {db_cluster_arn}')
        
        engine = detail['responseElements']['engine']
        
        if engine in non_comm_engine:
            rds_tag_value = rds_non_comm_tag_value
        elif engine in comm_engine:
            rds_tag_value = rds_comm_tag_value
        else:
            rds_tag_value = rds_non_comm_tag_value
        
        rds.add_tags_to_resource(ResourceName=db_cluster_arn, Tags=[{'Key': default_tag_key, 'Value': rds_tag_value}])

    elif event_name == 'CreateDBInstanceReadReplica':
        rds = boto3.client('rds', region_name=region)

        db_instance_arn = detail['responseElements']['dBInstanceArn']
        logger.info(f'Tagging RDS ReadReplica instance {db_instance_arn}')

        engine = detail['responseElements']['engine']
        
        if engine in non_comm_engine:
            rds_tag_value = rds_non_comm_tag_value
        elif engine in comm_engine:
            rds_tag_value = rds_comm_tag_value
        else:
            rds_tag_value = rds_non_comm_tag_value

        rds.add_tags_to_resource(ResourceName=db_instance_arn, Tags=[{'Key': default_tag_key, 'Value': rds_tag_value}])
    
    else:
        logger.warning('Not supported action')

    logger.info('Remaining time (ms): ' + str(context.get_remaining_time_in_millis()) + '\\n')
    return True
