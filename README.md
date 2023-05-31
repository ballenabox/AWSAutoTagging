# AutoTagging
CloudFormation YAML template for EC2, EBS, S3, RDS auto tagging
<br>

![image](https://github.com/ballenabox/AWSAutoTagging/assets/47315562/d0d3c376-2133-4b1e-b23e-470908ae1e79)

<br>

사용 언어 : Python<br>
배포 방식 : AWS CloudFormation YAML Template<br>
구성 요소 : Lambda, EventBridge(CloudWatch Events), CloudWatch Log Group, CloudTrail<br>
작동 방식 : 각 리소스(EC2, EBS,RDS, S3) 생성 시 CloudTrail에 찍히는 이벤트가 EventBridge에 감지되면 Lambda를 작동해 Tag를 할당<br>
