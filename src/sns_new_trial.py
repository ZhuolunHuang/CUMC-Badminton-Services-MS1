import logging
import time
import boto3
import os
from botocore.exceptions import ClientError




class SNS:
    logger = logging.getLogger(__name__)

    sns_client = boto3.client('sns',
                              region_name= os.environ.get("region"),
                              aws_access_key_id= os.environ.get("key_id"),
                              aws_secret_access_key= os.environ.get("aws_secret_access_key")
                              )
    def __int__(self):
        self.current_time = datetime.now()

    def subscribe(sns_client, logger, topic, protocol, endpoint):
        """
    :param topic: The topic to subscribe to.
    :param protocol: The protocol of the endpoint, such as 'sms' or 'email'.
    :param endpoint: The endpoint that receives messages, such as a phone number
                     (in E.164 format) for SMS messages, or an email address for
                     email messages.
    :return: The newly added subscription.
    """
        try:
            subscription = sns_client.subscribe(
                TopicArn=topic, Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
            logger.info("Subscribed %s %s to topic %s.", protocol, endpoint, topic)
        except ClientError:
            logger.exception(
                "Couldn't subscribe %s %s to topic %s.", protocol, endpoint, topic)
            raise
        else:
            return subscription

    def create_topic(sns_client, logger, name):
        """
    Creates a notification topic.

    :param name: The name of the topic to create.
    :return: The newly created topic.
    """

        try:
            topic = sns_client.create_topic(Name=name)
            print(topic)
            logger.info("Created topic %s with ARN %s.", name, topic['TopicArn'])

        except ClientError:
            logger.exception("Couldn't create topic %s.", name)
            raise
        else:
            return topic['TopicArn']

    def list_topics(sns_client, logger):
        """
    Lists topics for the current account.

    :return: An iterator that yields the topics.
    """

        try:
            topics_iter = sns_client.list_topics()
            logger.info("Got topics.")
        except ClientError:
            logger.exception("Couldn't get topics.")
            raise
        else:
            return topics_iter




