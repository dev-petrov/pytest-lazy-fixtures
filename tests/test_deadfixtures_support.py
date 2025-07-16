from pytest_deadfixtures import EXIT_CODE_SUCCESS  # type: ignore[import-untyped]


def test_lazy_fixtures_collected_simple(pytester):
    pytester.makepyfile(
        """
            import pytest
            from pytest_lazy_fixtures import lf


            @pytest.fixture
            def some_fixture():
                return 1

            @pytest.mark.usefixtures()
            @pytest.mark.parametrize("value", [lf("some_fixture")])
            def test_simple(value):
                assert 1 == value
        """
    )

    result = pytester.runpytest("--dead-fixtures", plugins=("pytest_lazy_fixtures.plugin",))

    assert result.ret == EXIT_CODE_SUCCESS, result.stdout


def test_lazy_fixtures_collected_list(pytester):
    pytester.makepyfile(
        """
            import pytest
            from pytest_lazy_fixtures import lf


            @pytest.fixture
            def some_fixture():
                return 1

            @pytest.mark.parametrize("value", [[lf("some_fixture")]])
            def test_simple(value):
                assert 1 == value
        """
    )

    result = pytester.runpytest("--dead-fixtures", plugins=("pytest_lazy_fixtures.plugin",))

    assert result.ret == EXIT_CODE_SUCCESS, result.stdout


def test_lazy_fixtures_collected_dict_simple(pytester):
    pytester.makepyfile(
        """
            import pytest
            from pytest_lazy_fixtures import lf


            @pytest.fixture
            def some_fixture_key():
                return 1

            @pytest.fixture
            def some_fixture_value():
                return 1

            @pytest.mark.parametrize("value", [{lf("some_fixture_key"): lf("some_fixture_value")}])
            def test_simple(value):
                assert 1 == value
        """
    )

    result = pytester.runpytest("--dead-fixtures", plugins=("pytest_lazy_fixtures.plugin",))

    assert result.ret == EXIT_CODE_SUCCESS, result.stdout


def test_lazy_fixtures_collected_dict_deep(pytester):
    pytester.makepyfile(
        """
            import pytest
            from pytest_lazy_fixtures import lf


            @pytest.fixture
            def some_fixture_key():
                return 1

            @pytest.fixture
            def some_fixture_value():
                return 1

            @pytest.mark.parametrize("value", [{lf("some_fixture_key"): [lf("some_fixture_value")]}])
            def test_simple(value):
                assert 1 == value
        """
    )

    result = pytester.runpytest("--dead-fixtures", plugins=("pytest_lazy_fixtures.plugin",))

    assert result.ret == EXIT_CODE_SUCCESS, result.stdout


def test_lazy_fixture_callable_collected(pytester):
    pytester.makepyfile(
        """
            import pytest
            from pytest_lazy_fixtures import lfc, lf


            @pytest.fixture
            def some_fixture_func():
                return "{} test".format

            @pytest.fixture
            def some_fixture():
                return 1

            @pytest.mark.parametrize("value", [lfc("some_fixture_func", lf("some_fixture"))])
            def test_simple(value):
                assert "1 test" == value
        """
    )

    result = pytester.runpytest("--dead-fixtures", plugins=("pytest_lazy_fixtures.plugin",))

    assert result.ret == EXIT_CODE_SUCCESS, result.stdout


def test_lazy_fixtures_collected_argvalues(pytester):
    pytester.makepyfile(
        """
            import pytest
            from pytest_lazy_fixtures import lf


            @pytest.fixture
            def some_fixture():
                return 1

            @pytest.mark.parametrize("value", argvalues=[lf("some_fixture")])
            def test_simple(value):
                assert 1 == value
        """
    )

    result = pytester.runpytest("--dead-fixtures", plugins=("pytest_lazy_fixtures.plugin",))

    assert result.ret == EXIT_CODE_SUCCESS, result.stdout


def test_lazy_fixtures_collected_argnames_argvalues(pytester):
    pytester.makepyfile(
        """
            import pytest
            from pytest_lazy_fixtures import lf


            @pytest.fixture
            def some_fixture():
                return 1

            @pytest.mark.parametrize(argnames="value", argvalues=[lf("some_fixture")])
            def test_simple(value):
                assert 1 == value
        """
    )

    result = pytester.runpytest("--dead-fixtures", plugins=("pytest_lazy_fixtures.plugin",))

    assert result.ret == EXIT_CODE_SUCCESS, result.stdout


def test_lazy_fixtures_collected_parametrized_fixture_simple(pytester):
    pytester.makepyfile(
        """
            import pytest
            from pytest_lazy_fixtures import lf

            @pytest.fixture
            def some_parametrized_fixture():
                return 1

            @pytest.fixture(params=[lf("some_parametrized_fixture")])
            def some_fixture(request):
                return request.param

            def test_simple(some_fixture):
                assert 1 == value
        """
    )

    result = pytester.runpytest("--dead-fixtures", plugins=("pytest_lazy_fixtures.plugin",))

    assert result.ret == EXIT_CODE_SUCCESS, result.stdout


def test_lazy_fixtures_collected_parametrized_fixture_list(pytester):
    pytester.makepyfile(
        """
            import pytest
            from pytest_lazy_fixtures import lf


            @pytest.fixture
            def some_parametrized_fixture():
                return 1

            @pytest.fixture(params=[[lf("some_parametrized_fixture")]])
            def some_fixture(request):
                return request.param

            def test_simple(some_fixture):
                assert 1 == value
        """
    )

    result = pytester.runpytest("--dead-fixtures", plugins=("pytest_lazy_fixtures.plugin",))

    assert result.ret == EXIT_CODE_SUCCESS, result.stdout


def test_lazy_fixtures_collected_parametrized_fixture_dict_simple(pytester):
    pytester.makepyfile(
        """
            import pytest
            from pytest_lazy_fixtures import lf

            @pytest.fixture
            def some_parametrized_fixture_key():
                return 1

            @pytest.fixture
            def some_parametrized_fixture_value():
                return 1

            @pytest.fixture(params=[{lf("some_parametrized_fixture_key"): lf("some_parametrized_fixture_value")}])
            def some_fixture(request):
                return request.param

            def test_simple(some_fixture):
                assert 1 == value
        """
    )

    result = pytester.runpytest("--dead-fixtures", plugins=("pytest_lazy_fixtures.plugin",))

    assert result.ret == EXIT_CODE_SUCCESS, result.stdout


def test_lazy_fixtures_collected_parametrized_fixture_dict_deep(pytester):
    pytester.makepyfile(
        """
            import pytest
            from pytest_lazy_fixtures import lf


            @pytest.fixture
            def some_parametrized_fixture_key():
                return 1

            @pytest.fixture
            def some_parametrized_fixture_value():
                return 1

            @pytest.fixture(params=[{lf("some_parametrized_fixture_key"): [lf("some_parametrized_fixture_value")]}])
            def some_fixture(request):
                return request.param

            def test_simple(some_fixture):
                assert 1 == value
        """
    )

    result = pytester.runpytest("--dead-fixtures", plugins=("pytest_lazy_fixtures.plugin",))

    assert result.ret == EXIT_CODE_SUCCESS, result.stdout


def test_lazy_fixture_callable_parametrized_fixture_collected(pytester):
    pytester.makepyfile(
        """
            import pytest
            from pytest_lazy_fixtures import lfc, lf


            @pytest.fixture
            def some_parametrized_fixture_func():
                return "{} test".format

            @pytest.fixture
            def some_fixture_value():
                return 1

            @pytest.fixture(params=[lfc("some_fixture_func", lf("some_fixture")])
            def some_fixture(request):
                return request.param

            def test_simple(some_fixture):
                assert "1 test" == value
        """
    )

    result = pytester.runpytest("--dead-fixtures", plugins=("pytest_lazy_fixtures.plugin",))

    assert result.ret == EXIT_CODE_SUCCESS, result.stdout
