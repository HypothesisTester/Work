def f(*args, **kwargs):
    print("Named:", kwargs)


f(galleons=100, sickle=50, knuts=25)