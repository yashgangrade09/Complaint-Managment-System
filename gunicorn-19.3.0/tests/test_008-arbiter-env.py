# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.

import t
import os
from gunicorn.app.base import BaseApplication
import gunicorn.arbiter


class PreloadedAppWithEnvSettings(BaseApplication):
    """
    Simple application that makes use of the 'preload' feature to
    start the application before spawning worker processes and sets
    environmental variable configuration settings.
    """

    def init(self, parser, opts, args):
        """No-op"""
        pass

    def load(self):
        """No-op"""
        pass

    def load_config(self):
        """Set the 'preload_app' and 'raw_env' settings in order to verify their
        interaction below.
        """
        self.cfg.set('raw_env', [
            'SOME_PATH=/tmp/something', 'OTHER_PATH=/tmp/something/else'])
        self.cfg.set('preload_app', True)

    def wsgi(self):
        """Assert that the expected environmental variables are set when
        the main entry point of this application is called as part of a
        'preloaded' application.
        """
        verify_env_vars()
        return super(PreloadedAppWithEnvSettings, self).wsgi()


def verify_env_vars():
    t.eq(os.getenv('SOME_PATH'), '/tmp/something')
    t.eq(os.getenv('OTHER_PATH'), '/tmp/something/else')


def test_env_vars_available_during_preload():
    """Ensure that configured environmental variables are set during the
    initial set up of the application (called from the .setup() method of
    the Arbiter) such that they are available during the initial loading
    of the WSGI application.
    """
    # Note that we aren't making any assertions here, they are made in the
    # dummy application object being loaded here instead.
    gunicorn.arbiter.Arbiter(PreloadedAppWithEnvSettings())
