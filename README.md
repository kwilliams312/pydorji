# pydorji
A simple Dorji818 python module

Based off the reference documents: [http://dorji.com/docs/data/DRA818V.pdf]

## Notes
 * Each time a variable is set dmosetgroup is refreshed
 * prepare for pypi: https://blog.jetbrains.com/pycharm/2017/05/how-to-publish-your-package-on-pypi/

## Todo
 * error checking 

## Example usage:
```python
#!/usr/bin/env python

from pydorji import Dorji

d = Dorji()
d.scan_freq("144.3320")
d['tx'] = "144.4460"
d['rx'] = "144.4460"
```
