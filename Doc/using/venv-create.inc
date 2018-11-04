Creation of :ref:`virtual environments <venv-def>` is done by executing the
command ``venv``::

    python3 -m venv /path/to/new/virtual/environment

Running this command creates the target directory (creating any parent
directories that don't exist already) and places a ``pyvenv.cfg`` file in it
with a ``home`` key pointing to the Python installation from which the command
was run.  It also creates a ``bin`` (or ``Scripts`` on Windows) subdirectory
containing a copy/symlink of the Python binary/binaries (as appropriate for the
platform or arguments used at environment creation time). It also creates an
(initially empty) ``lib/pythonX.Y/site-packages`` subdirectory
(on Windows, this is ``Lib\site-packages``). If an existing
directory is specified, it will be re-used.

.. deprecated:: 3.6
   ``pyvenv`` was the recommended tool for creating virtual environments for
   Python 3.3 and 3.4, and is `deprecated in Python 3.6
   <https://docs.python.org/dev/whatsnew/3.6.html#deprecated-features>`_.

.. versionchanged:: 3.5
   The use of ``venv`` is now recommended for creating virtual environments.

.. highlight:: none

On Windows, invoke the ``venv`` command as follows::

    c:\>c:\Python35\python -m venv c:\path\to\myenv

Alternatively, if you configured the ``PATH`` and ``PATHEXT`` variables for
your :ref:`Python installation <using-on-windows>`::

    c:\>python -m venv c:\path\to\myenv

The command, if run with ``-h``, will show the available options::

    usage: venv [-h] [--system-site-packages] [--symlinks | --copies] [--clear]
                [--upgrade] [--without-pip] [--prompt PROMPT]
                ENV_DIR [ENV_DIR ...]

    하나 이상의 대상 디렉터리에 가상 파이썬 환경을 만듭니다.

    positional arguments:
      ENV_DIR               안에 환경을 만들 디렉터리.

    optional arguments:
      -h, --help            이 도움말 메시지를 보여주고 종료합니다
      --system-site-packages
                            가상 환경이 시스템 site-packages 디렉터리를 액세스하도록 합니다.
      --symlinks            심볼릭 링크가 플랫폼의 기본값이 아닐 때, 복사본 대신 심볼릭 링크를
                            시도하도록 합니다.
      --copies              심볼릭 링크가 플랫폼의 기본값일 때조차, 심볼릭 링크 대신에 복사본을
                            사용하도록 합니다.
      --clear               환경을 만들기 전에, 환경 디렉터리에 내용이 이미 있으면 삭제합니다.
      --upgrade             파이썬이 그 자리에서 업그레이드되었다고 가정하고, 환경 디렉터리를 이
                            버전의 파이썬을 사용하도록 업그레이드합니다.
      --without-pip         가상 환경에 pip을 설치하거나 업그레이드하는 것을 건너뜁니다 (pip은
                            기본적으로 부트스트랩 됩니다)
      --prompt PROMPT       이 환경에 대한 대체 프롬프트 접두어를 제공합니다.

    일단 환경이 만들어지면, 활성화할 수 있습니다. 예를 들어, bin 디렉터리의 activate 스크립트를
    source 합니다.

.. versionchanged:: 3.4
   Installs pip by default, added the ``--without-pip``  and ``--copies``
   options

.. versionchanged:: 3.4
   In earlier versions, if the target directory already existed, an error was
   raised, unless the ``--clear`` or ``--upgrade`` option was provided.

.. note::
   While symlinks are supported on Windows, they are not recommended. Of
   particular note is that double-clicking ``python.exe`` in File Explorer
   will resolve the symlink eagerly and ignore the virtual environment.

The created ``pyvenv.cfg`` file also includes the
``include-system-site-packages`` key, set to ``true`` if ``venv`` is
run with the ``--system-site-packages`` option, ``false`` otherwise.

Unless the ``--without-pip`` option is given, :mod:`ensurepip` will be
invoked to bootstrap ``pip`` into the virtual environment.

Multiple paths can be given to ``venv``, in which case an identical virtual
environment will be created, according to the given options, at each provided
path.

Once a virtual environment has been created, it can be "activated" using a
script in the virtual environment's binary directory. The invocation of the
script is platform-specific (`<venv>` must be replaced by the path of the
directory containing the virtual environment):

+-------------+-----------------+-----------------------------------------+
| Platform    | Shell           | Command to activate virtual environment |
+=============+=================+=========================================+
| Posix       | bash/zsh        | $ source <venv>/bin/activate            |
+-------------+-----------------+-----------------------------------------+
|             | fish            | $ . <venv>/bin/activate.fish            |
+-------------+-----------------+-----------------------------------------+
|             | csh/tcsh        | $ source <venv>/bin/activate.csh        |
+-------------+-----------------+-----------------------------------------+
| Windows     | cmd.exe         | C:\\> <venv>\\Scripts\\activate.bat     |
+-------------+-----------------+-----------------------------------------+
|             | PowerShell      | PS C:\\> <venv>\\Scripts\\Activate.ps1  |
+-------------+-----------------+-----------------------------------------+

You don't specifically *need* to activate an environment; activation just
prepends the virtual environment's binary directory to your path, so that
"python" invokes the virtual environment's Python interpreter and you can run
installed scripts without having to use their full path. However, all scripts
installed in a virtual environment should be runnable without activating it,
and run with the virtual environment's Python automatically.

You can deactivate a virtual environment by typing "deactivate" in your shell.
The exact mechanism is platform-specific: for example, the Bash activation
script defines a "deactivate" function, whereas on Windows there are separate
scripts called ``deactivate.bat`` and ``Deactivate.ps1`` which are installed
when the virtual environment is created.

.. versionadded:: 3.4
   ``fish`` and ``csh`` activation scripts.
