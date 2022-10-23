Python XenForo Api
==================

! PRE-VERSION !

Python Lib für die XenForo api

=======
Sample:
=======

.. code-block:: python

  from LordXen import XenForo

  forum_url = input('URL ? ')
  api_key = input('API_KEY ? ')

  x = XenForo(url=forum_url, api_key=api_key)

  xen_thread_800 = x.get_thread(800)
  s = xen_thread_800.exists()
  if s:
      print("Thread with id 800 exist")
  else:
      print("Thread with id 800 not exist")


  # get node
  xen_node = x.get_node(209)

  # create new thread
  new_xen_thread = xen_node.create_thread('Test', message="LOL", tags='test')

  # edit thread
  s = new_xen_thread.edit(add_tags=['hello', 'world'], remove_tags=['test'])
  if s:
      print(f"Thread with id {new_xen_thread.thread_id} edited!")

  # post to thread
  s = new_xen_thread.create_post('Hallo Test')
  if s:
      print(f"Created post for {new_xen_thread.thread_id}")


Output:
*******

.. code-block::

  Thread with id 800 exist
  Thread with id 17291 edited!
  Created post for 17291


*by LordBex*

