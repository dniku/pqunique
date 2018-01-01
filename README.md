This is a very simple Python class for creating priority queues which maintain unique copies of elements.

This is achieved by storing a separate `set` of elements that have been inserted and checking each time whether the new element is in that set or not. An optional `key` parameter allows to specify a function that will be calculated on each element before checking it against the set.

`put()` will return `True` if the element was not present in the queue and `False` otherwise.
