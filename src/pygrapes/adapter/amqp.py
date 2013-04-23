#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from amqplib import client_0_8 as amqp


class Amqp(Adapter):
    amqp			= None

    @classmethod
    def name(cls):
        return 'amqp'

    def __init__(self, route, queue='messages', exchange='pigeon', durable=True,\
        exclusive=False, auto_delete=False, prefetch=0, channel_type='direct',\
        host='localhost:5672', user='guest', password='guest', vhost='/', insist=False):
        Adapter.__init__(self)
        self.route = route


        self.queue = queue
        self.exchange = exchange
        self.channel_type = channel_type
        self.durable = durable
        self.exclusive = exclusive
        self.auto_delete = auto_delete
        self.prefetch = prefetch

        self.host = host
        self.user = user
        self.password = password
        self.virtual_host = virtual_host
        self.insist = insist

    def _init(self):
        if self.amqp is not None:
            return
        self.amqp = amqp.Connection(
            host		= self.host,
            userid		= self.user,
            password	= self.password,
            virtual_host= self.virtual_host,
            insist		= self.insist
        )

        self.channel = self.amqp.channel()
        if self.prefetch > 0:
            self.channel.basic_qos(prefetch_count=1)
        self.uuid = str(uuid.uuid4())
        # always declare eschange to be sure that it exists
        self.channel.exchange_declare(
            exchange    = self.exchange,
            type        = self.channel_type,
            durable     = self.durable,
            auto_delete = self.auto_delete
        )


    def consume(self, callback):
        self._init()
        self.channel.queue_declare(
            queue       = self.queue,
            durable     = self.durable,
            exclusive   = self.exclusive,
            auto_delete = self.auto_delete
        )
        self.channel.queue_bind(
            queue       = self.queue,
            exchange    = self.exchange,
            routing_key = self.route
        )
        self.channel.basic_consume(
            queue		= self.queue,
            no_ack		= False,
            callback	= self.on_new_message(callback),
            consumer_tag= self.uuid
        )
        try:
            while True:
                self.channel.wait()
        except KeyboardInterrupt:
            self.channel.close()
            raise

    def on_new_message(self,callback):
        def callback_func(message):
            logger.debug(message.body)
            body = json.loads(message.body)
            if callback(body):
                self.ack(message)
        return callback_func

    def publish(self,message):
        self._init()
        msg = amqp.Message(json.dumps(message))
        if self.durable:
            msg.properties['delivery_mode'] = 2

        self.log.debug("Sending message with route '%s' to exchange '%s'" \
            % (self.route, self.exchange))
        self.log.debug(msg.body)
        self.channel.basic_publish(
            msg,
            exchange	= self.exchange,
            routing_key	= self.route
        )
    
    def send(self, route, message, deferred):
        """
        Sends message to given route. Accepts 'deferred' keyword argument.
        """
        pass

    def attach_listener(self, route, callback):
        """
        Binds callback with message with given route.
        When message with given route was received given callback is called
        with 'deferred' keyword argument that is used to pass back response.
        """
        pass
    
    def detach_listener(self, route):
        """
        Unbinds callback from message with given route.
        """
        pass

    def ack(self, message):
        """
        Sends information that message was processed.
        """
        self._init()
        self.channel.basic_ack(message.delivery_tag)
