#!/usr/bin/env python3

"""
Authors: Tobias Kaiser, Jakob Beckmann

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

import os
import sys
from pathlib import Path
import json

from solc import install_solc
from solc.main import _parse_compiler_output
from solc.wrapper import solc_wrapper
from solc.exceptions import SolcError
import solc.install

from . import command
from . import utils

class SolcCommand(command.Command):
    """A command that uses the `solc` compiler."""
    def __init__(self, project_root):
        super().__init__(project_root)

    def compile_(self):
        """Compile the project and dump the output to an intermediate file."""
        sources = self._get_sol_files()
        if not sources:
            raise utils.NoSolidityProject(self.get_project_root())
        comp_output = self._compile_solfiles(sources)
        with open(self.get_compilation_output(), 'w') as fs:
            json.dump(comp_output, fs)

    def report(self):
        """Reports the output from securify."""
        with open(self.get_securify_target_output(), mode='r') as file:
            for line in file.readlines():
                print(line, end="")

    def _get_sol_files(self):
        """Returns the solidity files contained in the project root."""
        return [os.path.join(p, f) for p, _, fs in os.walk(self.get_project_root()) for f in fs if
                f.endswith('.sol') and
                'node_modules' not in p and
                '/test/' not in p[len(str(self.get_project_root())):] and
                not p.endswith('/test')]

    def _get_binary(self, version):
        """Returns the binary for some version of solc."""
        binary = os.path.join(Path.home(), f'.py-solc/solc-v{version}/bin/solc')
        if not os.path.exists(binary):
            install_solc(f'v{version}', platform='linux')
        return binary

    def _compile_solfiles(self, files, solc_version=None, output_values=utils.OUTPUT_VALUES):
        """Compiles the files using the solc compiler."""
        remappings = []
        node_modules_dir = utils.find_node_modules_dir(self.get_project_root())

        if node_modules_dir is not None:
            zeppelin_path = os.path.abspath(os.path.join(
                node_modules_dir, 'zeppelin-solidity'))
            open_zeppelin_path = os.path.abspath(
                os.path.join(node_modules_dir, 'openzeppelin-solidity'))
            if os.path.isdir(zeppelin_path):
                remappings.append(f'zeppelin-solidity={zeppelin_path}')
            if os.path.isdir(open_zeppelin_path):
                remappings.append(f'openzeppelin-solidity={open_zeppelin_path}')

        if solc_version is None:
            solc_version = min(map(utils.parse_sol_version, files),
                               key=lambda x: utils.version_to_tuple(x))

        binary = self._get_binary(solc_version)

        combined_json = ','.join(output_values)
        compiler_kwargs = {'import_remappings': remappings,
                           'allow_paths': self.get_project_root(),
                           'source_files': files,
                           'solc_binary': binary,
                           'combined_json': combined_json}

        try:
            stdoutdata, _, _, _ = solc_wrapper(**compiler_kwargs)
            return _parse_compiler_output(stdoutdata)
        except SolcError as e:
            raise utils.SolidityCompilationException(e, files)
