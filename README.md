# OBK

This project demonstrates a small command line interface with a bulletproof
pytest setup.  Tests live under `tests/` and the `pytest.ini` configuration
ensures coverage reporting and seamless imports.

The CLI uses the [`dependency-injector`](https://pypi.org/project/dependency-injector/) library
to wire service classes. See `src/obk/containers.py` for the DI container.

Run the tests with:

```bash
pytest
```

This will execute the full suite with coverage enabled by default.


