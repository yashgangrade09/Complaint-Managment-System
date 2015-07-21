from datetime import timedelta

import t

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

import logging

from gunicorn.config import Config
from gunicorn.instrument.statsd import Statsd


class TestException(Exception): pass

class MockSocket(object):
    "Pretend to be a UDP socket"
    def __init__(self, failp):
        self.failp = failp
        self.msgs = []  # accumulate messages for later inspection

    def send(self, msg):
        if self.failp:
            raise TestException("Should not interrupt the logger")
        self.msgs.append(msg)

    def reset(self):
        self.msgs = []

class MockResponse(object):
    def __init__(self, status):
        self.status = status

def test_statsd_fail():
    "UDP socket fails"
    logger = Statsd(Config())
    logger.sock = MockSocket(True)
    logger.info("No impact on logging")
    logger.debug("No impact on logging")
    logger.critical("No impact on logging")
    logger.error("No impact on logging")
    logger.warning("No impact on logging")
    logger.exception("No impact on logging")

def test_instrument():
    logger = Statsd(Config())
    # Capture logged messages
    sio = StringIO()
    logger.error_log.addHandler(logging.StreamHandler(sio))
    logger.sock = MockSocket(False)

    # Regular message
    logger.info("Blah", extra={"mtype": "gauge", "metric": "gunicorn.test", "value": 666})
    t.eq(logger.sock.msgs[0], "gunicorn.test:666|g")
    t.eq(sio.getvalue(), "Blah\n")
    logger.sock.reset()

    # Only metrics, no logging
    logger.info("", extra={"mtype": "gauge", "metric": "gunicorn.test", "value": 666})
    t.eq(logger.sock.msgs[0], "gunicorn.test:666|g")
    t.eq(sio.getvalue(), "Blah\n")  # log is unchanged
    logger.sock.reset()

    # Debug logging also supports metrics
    logger.debug("", extra={"mtype": "gauge", "metric": "gunicorn.debug", "value": 667})
    t.eq(logger.sock.msgs[0], "gunicorn.debug:667|g")
    t.eq(sio.getvalue(), "Blah\n")  # log is unchanged
    logger.sock.reset()

    logger.critical("Boom")
    t.eq(logger.sock.msgs[0], "gunicorn.log.critical:1|c|@1.0")
    logger.sock.reset()

    logger.access(MockResponse("200 OK"), None, {}, timedelta(seconds=7))
    t.eq(logger.sock.msgs[0], "gunicorn.request.duration:7000.0|ms")
    t.eq(logger.sock.msgs[1], "gunicorn.requests:1|c|@1.0")
    t.eq(logger.sock.msgs[2], "gunicorn.request.status.200:1|c|@1.0")

def test_prefix():
    c = Config()
    c.set("statsd_prefix", "test.")
    logger = Statsd(c)
    logger.sock = MockSocket(False)

    logger.info("Blah", extra={"mtype": "gauge", "metric": "gunicorn.test", "value": 666})
    t.eq(logger.sock.msgs[0], "test.gunicorn.test:666|g")

def test_prefix_no_dot():
    c = Config()
    c.set("statsd_prefix", "test")
    logger = Statsd(c)
    logger.sock = MockSocket(False)

    logger.info("Blah", extra={"mtype": "gauge", "metric": "gunicorn.test", "value": 666})
    t.eq(logger.sock.msgs[0], "test.gunicorn.test:666|g")

def test_prefix_multiple_dots():
    c = Config()
    c.set("statsd_prefix", "test...")
    logger = Statsd(c)
    logger.sock = MockSocket(False)

    logger.info("Blah", extra={"mtype": "gauge", "metric": "gunicorn.test", "value": 666})
    t.eq(logger.sock.msgs[0], "test.gunicorn.test:666|g")

def test_prefix_nested():
    c = Config()
    c.set("statsd_prefix", "test.asdf.")
    logger = Statsd(c)
    logger.sock = MockSocket(False)

    logger.info("Blah", extra={"mtype": "gauge", "metric": "gunicorn.test", "value": 666})
    t.eq(logger.sock.msgs[0], "test.asdf.gunicorn.test:666|g")
