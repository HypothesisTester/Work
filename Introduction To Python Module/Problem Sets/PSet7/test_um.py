import um

def test_count_um_only():
    assert um.count("hello, um, world") == 1

def test_ignore_um_in_word():
    assert um.count("yummy") == 0

def test_ignore_case():
    assert um.count("Hello, UM, world") == 1

def test_multiple_ums():
    assert um.count("um um um um") == 4

def test_ums_surrounded_by_non_alphabets():
    assert um.count("um.um,um;um!") == 4
