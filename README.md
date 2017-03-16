# Data Director
Data Director is a custom director for TwoOneThree Athletics. Essentially it takes in JSON, runs it through its innards, and outputs it to the appropriate data sources.

## Architecture
1. Data come in JSON format.
2. Main director module cycles through objects and passes it forwards depending on main object key.
3. This is object is passed to a module as defined by a pre-loaded config file.
4. The module then does its stuff to it.

## Future
Will evaluate NiFi as a potential replacement as scaling becomes an issue.

## License

MIT License - Copyright (c) 2017 Samuel Harding