import json
import boto3
import StringIO
import zipfile
from botocore.client import Config
import mimetypes

def lambda_handler(event, context):
    # TODO implement
    try:
        s3 = boto3.resource('s3',config=Config(signature_version='s3v4'))

        portfolio_bucket=s3.Bucket('thisisadamyang.com')
        build_bucket = s3.Bucket('protfoliobuild.thisisadamyang.com')

        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('PortfolioBuild.zip',portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm, ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        sns=boto3.resource('sns')
        topic=sns.Topic('arn:aws:sns:us-east-1:305115124591:DeployDone')
        topic.publish(Subject="Your Portfolio has been deployed successfully!",Message="Your Portfolio, thisisadamyang.com, has been deployed successfully")
    except:
        topic.publish(Subject="Your Portfolio Deployment has failed",Message="Deployment has failed for thisisadamyang.com")
    return {
        "statusCode": 200,
        "body": json.dumps('TTTTTesting!')
    }
