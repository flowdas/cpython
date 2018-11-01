.. highlightlang:: c

.. _iterator:

Iterator Protocol
=================

There are two functions specifically for working with iterators.

.. c:function:: int PyIter_Check(PyObject *o)

   Return true if the object *o* supports the iterator protocol.


.. c:function:: PyObject* PyIter_Next(PyObject *o)

   Return the next value from the iteration *o*.  The object must be an iterator
   (it is up to the caller to check this).  If there are no remaining values,
   returns *NULL* with no exception set.  If an error occurs while retrieving
   the item, returns *NULL* and passes along the exception.

To write a loop which iterates over an iterator, the C code should look
something like this::

   PyObject *iterator = PyObject_GetIter(obj);
   PyObject *item;

   if (iterator == NULL) {
       /* 에러를 전파합니다 */
   }

   while (item = PyIter_Next(iterator)) {
       /* item으로 뭔가 합니다 */
       ...
       /* 끝나면 참조를 반환합니다 */
       Py_DECREF(item);
   }

   Py_DECREF(iterator);

   if (PyErr_Occurred()) {
       /* 에러를 전파합니다 */
   }
   else {
       /* 쓸모있는 일을 계속합니다 */
   }
