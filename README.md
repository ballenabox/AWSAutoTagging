# AutoTagging
CloudFormation YAML template for EC2, EBS, S3, RDS auto tagging
<br>

![image](https://github.com/ballenabox/AWSAutoTagging/assets/47315562/d0d3c376-2133-4b1e-b23e-470908ae1e79)

<br>

1. 사용 언어 : Python(with AWS SDK - boto3)
<br><br><br>
2. 배포 방식 : AWS CloudFormation YAML Template
<br><br><br>
3. 구성 요소 : Lambda, EventBridge(CloudWatch Events), CloudWatch Log Group, CloudTrail
<br><br><br>
4. 작동 방식 : 
<br><br>
- 각 리소스(EC2, EBS, RDS, S3) 생성 시 CloudTrail에 찍히는 이벤트가 EventBridge에 감지되면 Lambda를 작동해 Tag를 할당
<br><br>
- CloudTrail 이벤트 로그에서 생성된 리소스의 ID를 추출해 Tagging 진행
<br><br>
1) 대상 이벤트 : RunInstances, CreateVolume, CreateBucket, CreateDBInstance, CreateDBCluster, CreateDBInstanceReadReplica
<br><br>
2) 비고 : 
<br>
- RDS Aurora(MySQL, Postgresql)의 경우를 대비해 리전 클러스터에도 Tag를 할당하기 위해 CreateDBCluster 이벤트도 포함
<br><br>
- Region 단위 배포 필요 : 이벤트를 감지하는 CloudTrail이 Region 단위 서비스
<br><br>
- CloudWatch Log Group 관련 설정은 Template 단계에서 불가 : 기본값 '만기 없음'. 비용 절감을 위해서 별도의 만기 설정 필요
<br><br>
- EC2의 경우 한 번에 여러 리소스가 생성되는 경우를 대비해 반복 처리
<br><br><br>
5. 예상 비용 : 
<br><br>
- Lambda가 작동하는 횟수에 비례해 비용이 발생. 즉, 각 리소스가 생성되는 횟수에 비례해 발생 : Lambda Free Tier 고려 필요
<br><br>
- Lambda Log가 CloudWatch Log Group에 수집/저장되는 비용 발생<br><br>
  
