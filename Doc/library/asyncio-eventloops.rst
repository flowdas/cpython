.. currentmodule:: asyncio

Event loops
===========

**Source code:** :source:`Lib/asyncio/events.py`

Event loop functions
--------------------

The following functions are convenient shortcuts to accessing the methods of the
global policy. Note that this provides access to the default policy, unless an
alternative policy was set by calling :func:`set_event_loop_policy` earlier in
the execution of the process.

.. function:: get_event_loop()

   Equivalent to calling ``get_event_loop_policy().get_event_loop()``.

.. function:: set_event_loop(loop)

   Equivalent to calling ``get_event_loop_policy().set_event_loop(loop)``.

.. function:: new_event_loop()

   Equivalent to calling ``get_event_loop_policy().new_event_loop()``.

.. function:: get_running_loop()

   Return the running event loop in the current OS thread.  If there
   is no running event loop a :exc:`RuntimeError` is raised.

   .. versionadded:: 3.7


.. _asyncio-event-loops:

Available event loops
---------------------

asyncio currently provides two implementations of event loops:
:class:`SelectorEventLoop` and :class:`ProactorEventLoop`.

.. class:: SelectorEventLoop

   Event loop based on the :mod:`selectors` module. Subclass of
   :class:`AbstractEventLoop`.

   Use the most efficient selector available on the platform.

   On Windows, only sockets are supported (ex: pipes are not supported):
   see the `MSDN documentation of select
   <https://msdn.microsoft.com/en-us/library/windows/desktop/ms740141%28v=vs.85%29.aspx>`_.

.. class:: ProactorEventLoop

   Proactor event loop for Windows using "I/O Completion Ports" aka IOCP.
   Subclass of :class:`AbstractEventLoop`.

   Availability: Windows.

   .. seealso::

      `MSDN documentation on I/O Completion Ports
      <https://msdn.microsoft.com/en-us/library/windows/desktop/aa365198%28v=vs.85%29.aspx>`_.

   .. admonition:: flowdas

      프로액터(proactor) 는 리액터(reactor)와 대비되는 용어입니다. :mod:`selectors` 모듈이 제공하는
      셀렉터들은 모두 비 블로킹(non-blocking) I/O를 사용합니다. 이들은 동기(synchronous) I/O와 사실상
      같은 구조를 갖지만 요청한 I/O가 블로킹에 들어갈 것 같으면 ``EWOULDBLOCK`` 에러를 일으키도록 하고, 셀렉터는
      이 에러를 일으키지 않고 I/O가 수행될 수 있을 때까지 **한꺼번에** 대기할 수 있도록 합니다. 이런 방식을
      reactive 하다고 합니다. 이에 반해 I/O를 즉시 완료할 수 없어도 요청 자체를 거부하는 것이 아니라, 요청을
      큐에 넣어두고, I/O가 완료되면 완료 신호를 주는 방식이 있습니다. 이때도 셀렉터와 비슷한 종류의 대기 메커니즘이
      제공됩니다. 윈도우의 IOCP 가 이 대기 메커니즘의 하나입니다. 비 블로킹 방식과의 결정적인 차이는, 요청하는
      순간부터 요청이 완료될 때까지 I/O에 수반되는 버퍼가 I/O 하부 시스템에 붙잡혀있게 된다는 것과, 큐에 들어간
      요청을 취소하는 메커니즘이 필요하다는 것입니다. 이 때문에 I/O 루프가 좀 다른 방식으로 구성되어야 합니다.
      구별하기 위해 이런 방식을 proactive 하다고 합니다. 버퍼가 직접 제공되기 때문에 reactive 한 방식보다 메모리
      복사를 줄여 성능을 개선할 수 있는 여지가 있습니다.

Example to use a :class:`ProactorEventLoop` on Windows::

    import asyncio, sys

    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

.. _asyncio-platform-support:

Platform support
----------------

The :mod:`asyncio` module has been designed to be portable, but each platform
still has subtle differences and may not support all :mod:`asyncio` features.

Windows
^^^^^^^

Common limits of Windows event loops:

- :meth:`~AbstractEventLoop.create_unix_connection` and
  :meth:`~AbstractEventLoop.create_unix_server` are not supported: the socket
  family :data:`socket.AF_UNIX` is specific to UNIX
- :meth:`~AbstractEventLoop.add_signal_handler` and
  :meth:`~AbstractEventLoop.remove_signal_handler` are not supported
- :meth:`EventLoopPolicy.set_child_watcher` is not supported.
  :class:`ProactorEventLoop` supports subprocesses. It has only one
  implementation to watch child processes, there is no need to configure it.

:class:`SelectorEventLoop` specific limits:

- :class:`~selectors.SelectSelector` is used which only supports sockets
  and is limited to 512 sockets.
- :meth:`~AbstractEventLoop.add_reader` and :meth:`~AbstractEventLoop.add_writer` only
  accept file descriptors of sockets
- Pipes are not supported
  (ex: :meth:`~AbstractEventLoop.connect_read_pipe`,
  :meth:`~AbstractEventLoop.connect_write_pipe`)
- :ref:`Subprocesses <asyncio-subprocess>` are not supported
  (ex: :meth:`~AbstractEventLoop.subprocess_exec`,
  :meth:`~AbstractEventLoop.subprocess_shell`)

:class:`ProactorEventLoop` specific limits:

- :meth:`~AbstractEventLoop.create_datagram_endpoint` (UDP) is not supported
- :meth:`~AbstractEventLoop.add_reader` and :meth:`~AbstractEventLoop.add_writer` are
  not supported

The resolution of the monotonic clock on Windows is usually around 15.6 msec.
The best resolution is 0.5 msec. The resolution depends on the hardware
(availability of `HPET
<https://en.wikipedia.org/wiki/High_Precision_Event_Timer>`_) and on the Windows
configuration. See :ref:`asyncio delayed calls <asyncio-delayed-calls>`.

.. versionchanged:: 3.5

   :class:`ProactorEventLoop` now supports SSL.


Mac OS X
^^^^^^^^

Character devices like PTY are only well supported since Mavericks (Mac OS
10.9). They are not supported at all on Mac OS 10.5 and older.

On Mac OS 10.6, 10.7 and 10.8, the default event loop is
:class:`SelectorEventLoop` which uses :class:`selectors.KqueueSelector`.
:class:`selectors.KqueueSelector` does not support character devices on these
versions.  The :class:`SelectorEventLoop` can be used with
:class:`~selectors.SelectSelector` or :class:`~selectors.PollSelector` to
support character devices on these versions of Mac OS X. Example::

    import asyncio
    import selectors

    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)


Event loop policies and the default policy
------------------------------------------

Event loop management is abstracted with a *policy* pattern, to provide maximal
flexibility for custom platforms and frameworks. Throughout the execution of a
process, a single global policy object manages the event loops available to the
process based on the calling context. A policy is an object implementing the
:class:`AbstractEventLoopPolicy` interface.

.. admonition:: flowdas

   정책 패턴(policy pattern)은 디자인 패턴의 한 종류 입니다.

For most users of :mod:`asyncio`, policies never have to be dealt with
explicitly, since the default global policy is sufficient (see below).

The module-level functions
:func:`get_event_loop` and :func:`set_event_loop` provide convenient access to
event loops managed by the default policy.


Event loop policy interface
---------------------------

An event loop policy must implement the following interface:

.. class:: AbstractEventLoopPolicy

   Event loop policy.

   .. method:: get_event_loop()

      Get the event loop for the current context.

      Returns an event loop object implementing the :class:`AbstractEventLoop`
      interface. In case called from coroutine, it returns the currently
      running event loop.

      .. admonition:: flowdas

         코루틴에서 호출될 때 그 코루틴을 실행하고 있는 이벤트 루프와 현재 컨텍스트의 이벤트 루프가
         다를 수도 있음을 시사하고 있습니다.

      Raises an exception in case no event loop has been set for the current
      context and the current policy does not specify to create one. It must
      never return ``None``.

      .. admonition:: flowdas

         이벤트 루프를 새로 만들지를 지정하는 인터페이스 같은 것은 없습니다. 이런 정책은 정책 객체의
         코드에서 정의됩니다. 기본 정책의 경우는 메인 스레드에서 호출하는 경우만 루프를 새로 만들도록
         허락합니다. 컨텍스트라는 개념도 추상적인 것으로, 컨텍스트가 무엇을 의미하는지 역시 정책 객체의
         코드에서 결정합니다. 기본 정책의 경우는 컨텍스트가 스레드입니다.

      .. versionchanged:: 3.6

   .. method:: set_event_loop(loop)

      Set the event loop for the current context to *loop*.

   .. method:: new_event_loop()

      Create and return a new event loop object according to this policy's
      rules.

      If there's need to set this loop as the event loop for the current
      context, :meth:`set_event_loop` must be called explicitly.


The default policy defines context as the current thread, and manages an event
loop per thread that interacts with :mod:`asyncio`. An exception to this rule
happens when :meth:`~AbstractEventLoopPolicy.get_event_loop` is called from a
running future/coroutine, in which case it will return the current loop
running that future/coroutine.

If the current thread doesn't already have an event loop associated with it,
the default policy's :meth:`~AbstractEventLoopPolicy.get_event_loop` method
creates one when called from the main thread, but raises :exc:`RuntimeError`
otherwise.


Access to the global loop policy
--------------------------------

.. function:: get_event_loop_policy()

   Get the current event loop policy.

.. function:: set_event_loop_policy(policy)

   Set the current event loop policy. If *policy* is ``None``, the default
   policy is restored.


Customizing the event loop policy
---------------------------------

To implement a new event loop policy, it is recommended you subclass the
concrete default event loop policy :class:`DefaultEventLoopPolicy`
and override the methods for which you want to change behavior, for example::

    class MyEventLoopPolicy(asyncio.DefaultEventLoopPolicy):

        def get_event_loop(self):
            """이벤트 루프를 가져옵니다.

            None 이거나 EventLoop 의 인스턴스일 수 있습니다.
            """
            loop = super().get_event_loop()
            # loop 로 뭔가 합니다 ...
            return loop

    asyncio.set_event_loop_policy(MyEventLoopPolicy())

.. admonition:: flowdas

   따로 설명하고 있지는 않지만 :class:`DefaultEventLoopPolicy` 라는 클래스가 정의되는 것으로
   보아야 합니다.

