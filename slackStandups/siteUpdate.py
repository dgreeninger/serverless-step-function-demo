from pprint import pprint
import boto3
import datetime
now = datetime.datetime.now()


def main(event, context):
    # take the input from event and write to s3
    bucket_name = 'dgreeninger-slack-standups-website'
    pprint(event)
    pprint(context)
    date = str(now.strftime("%Y%m%d"))
    runtime = str(event['result'][0])
    user_count = str(event['result'][1])
    lazy_count = str(event['result'][2])
    standups_not = "standupsNot"+date+".push("+lazy_count+")\n"
    standups = "standups"+date+".push("+user_count+")\n"
    run_time = "time_line"+date+".push("+runtime+")\n"
    s3 = boto3.resource('s3')
    # get the data.js file
    data = s3.Object(bucket_name, 'data.js').get()
    j = data['Body'].read().decode("utf-8")
    pprint(j)
    # add the new stuff and save it
    j = j + run_time + standups_not + standups
    f = open("/tmp/data.js", "w")
    f.write(j)
    f.close()
    s3_client = boto3.client('s3')
    s3_client.upload_file(
            '/tmp/data.js', bucket_name, 'data.js',
            ExtraArgs={'ACL': 'public-read'}
            )
    return True
