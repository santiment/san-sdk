## Santiment API R example

### Usage

```
SANBASE_API_KEY=put-your-sanbase-apikey Rscript example.r
```

### Getting Apikey

Apikey is optional but without it for some metrics data may be limited to the interval: [3 months ago, 1 day ago].

To obtain an api key you should [log in to sanbase](https://sanbase-low.santiment.net/login) and go to the `account` page - [https://sanbase-low.santiment.net/account](https://sanbase-low.santiment.net/account). There is an `API Keys` section and a `Generate new api key` button.

#### Install `ghql` graphql client https://github.com/ropensci/ghql

```
install.packages("devtools")
library(devtools)
install_github("ropensci/ghql")
```

#### Install `httr`, `jsonlite`

```
install.packages(c("httr", "jsonlite"))
```

#### Example results

```
$data
$data$allProjects
                                  slug
1                               0chain
2                                   0x
3                                0xbtc
4                               0xcert
5                               1world
6                         ab-chain-rtb
7                              abulaba
...
```


```
$data
$data$dailyActiveAddresses
  activeAddresses             datetime
1               4 2018-08-01T00:00:00Z
2               0 2018-08-02T00:00:00Z
3              18 2018-08-03T00:00:00Z
4               3 2018-08-04T00:00:00Z
5               0 2018-08-05T00:00:00Z

```
