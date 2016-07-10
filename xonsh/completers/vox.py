import os
import builtins

from xonsh.lazyasd import LazyObject

from xonsh.platform import scandir
from xonsh.vox import Vox

DEFAULT_ENV_HOME = LazyObject(lambda: builtins.__xonsh_expand_path__('~/.virtualenvs'),
                              globals(), 'DEFAULT_ENV_HOME')


def complete_vox(prefix, line, begidx, endidx, ctx):
    """
    Completes xonsh's `vox` virtual environment manager
    """
    if not line.startswith('vox'):
        return
    to_list_when = ['vox activate ', 'vox remove ']
    if any(c in line for c in to_list_when):
        venv_home = builtins.__xonsh_env__.get('VIRTUALENV_HOME', DEFAULT_ENV_HOME)
        env_dirs = list(x.name for x in scandir(venv_home) if x.is_dir())
        return set(env_dirs)

    if (len(line.split()) > 1 and line.endswith(' ')) or len(line.split()) > 2:
        # "vox new " -> no complete (note space)
        return

    all_commands = [c[0].split()[1] for c in Vox.help_commands]
    if prefix in all_commands:
        # "vox new" -> suggest replacing new with other command (note no space)
        return all_commands, len(prefix)
    elif prefix:
        # "vox n" -> suggest "new"
        return [c for c in all_commands if c.startswith(prefix)], len(prefix)
    return set(all_commands)
