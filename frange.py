def frange(x, y, jump=1.0):
    '''
    Range for floats.
    
    Parameters:
      x: range starting value, will be included.
      y: range ending value, will be excluded
      jump: the step value. Only positive steps are supported.
    
    Return:
      a generator that yields floats
    
    Usage:
    >>> list(frange(0, 1, 0.2))
    [0.0, 0.2, 0.4, 0.6000000000000001, 0.8]
    >>> list(frange(1, 0, 0.2))
    [1.0]
    >>> list(frange(0.0, 0.05, 0.1))
    [0.0]
    >>> list(frange(0.0, 0.15, 0.1))
    [0.0, 0.1]
    
    '''
    i = 0.0
    x = float(x)  # Prevent yielding integers.
    y = float(y)  # Comparison converts y to float every time otherwise.
    x0 = x
    epsilon = jump / 2.0
    yield x  # yield always first value
    while x + epsilon < y:
        i += 1.0
        x = x0 + i * jump
        yield x