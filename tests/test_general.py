import linchemin_services


def test_version():
    version = linchemin_services.__version__
    print(version)
    assert version is not None


if __name__ == '__main__':
    test_version()
