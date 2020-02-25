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
    fancy_date = str(now.strftime("%Y-%m-%d"))
    run_time = "var time_line"+date+"= []\n"
    standups_not = "var standupsNot"+date+"= []\n"
    standups = "var standups"+date+"= []\ndailyGraph('"+date+"')\n"
    s3 = boto3.resource('s3')
    # get the data.js file
    data = s3.Object(bucket_name, 'data.js').get()
    j = data['Body'].read().decode("utf-8")
    pprint(j)
    # add the new stuff and save it
    j = j + run_time + standups_not + standups
    f = open("/tmp/data.js", "a")
    f.write(j)
    f.close()
    s3_client = boto3.client('s3')
    s3_client.upload_file(
            '/tmp/data.js', bucket_name, 'data.js',
            ExtraArgs={'ACL': 'public-read'}
            )
    # Update the index html
    data = s3.Object(bucket_name, 'index.html').get()
    j = data['Body'].read().decode("utf-8")
    pprint(j)
    # add the new stuff and save it
    j = j + '<hr><h1>'+fancy_date+'</h1><hr><div id="'+date+'"><!-- Plotly chart will be drawn inside this DIV --></div><br>'
    f = open("/tmp/index.html", "w")
    f.write(j)
    f.close()
    s3_client = boto3.client('s3')
    s3_client.upload_file(
            '/tmp/index.html', bucket_name, 'index.html',
            ExtraArgs={'ContentType': "text/html", 'ACL': 'public-read'}
            )

    return True
