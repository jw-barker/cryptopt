# Cryptopt
A simple Linux command-line cryptocurrency portfolio tracking tool.
# Usage
In order to save a portfolio you must provide a portfolio name and the holdings of that portfolio. You can update a portfolio by using the same command.





```
./cryptopt.py save p1 --holdings BTC=1.234,ETH=5.678
```


If you want to view a portfolio you can use the show command.

```
 ./cryptopt.py show p1 --fiat AUD
 ```
 Which will list the current value of the holdings within the portfolio and also the total amount.
