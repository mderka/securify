#!/usr/bin/env python3

"""
Author: Jakob Beckmann

Copyright 2018 ChainSecurity AG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import abc
import pathlib
import subprocess

from . import utils

class Command(metaclass=abc.ABCMeta):
    """Abstract Command implemented by all different kinds of compilations and reporting command."""

    def __init__(self, project_root):
        """Sets the project root."""
        self._project_root = pathlib.Path(project_root)

    def execute(self):
        """Execute the command. This includes compilation and reporting."""
        self.compile_()
        try:
            self.run_securify()
        except subprocess.CalledProcessError:
            utils.print_error("Error running securify")
            sys.exit(1)
        self.report()

    def get_project_root(self):
        """Returns the project root of the project."""
        return self._project_root

    def run_securify(self):
        """Runs the securify command."""
        cmd = ["java", "-Xmx4G", "-jar", "/securify_jar/securify.jar", "-co", self.get_compilation_output(),
               "-o", self.get_securify_target_output()]
        process = subprocess.run(cmd, shell=False, stdout=subprocess.PIPE)
        process.check_returncode()

    def get_compilation_output(self):
        """Returns the hex source resulting from the compilation."""
        return pathlib.Path("/comp.json")

    def get_securify_target_output(self):
        """Returns the target file where the securify output is stored."""
        return pathlib.Path("/securify_res.json")

    @abc.abstractmethod
    def compile_(self):
        """Compile the project."""
        pass

    @abc.abstractmethod
    def report(self):
        """Report findings."""
        pass
