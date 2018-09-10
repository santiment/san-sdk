library(httr)
library(jsonlite)

## This example should help to clarify how the URL is built. Left side is the URL and right side is the GraphiQL code 
## that the URL represents
# url = "https://api.santiment.net/graphiql?variables=%7B%7D&query=
#         query%20%7B%0A                                              #query {
#         %20%20dailyActiveAddresses(%0A                              #  dailyActiveAddresses(
#         %20%20%20%20slug:%20%22igtoken%22,%0A                       #    slug: "igtoken",
#         %20%20%20%20from:%20%222018-06-01%2016:00:00Z%22,%0A        #    from: "2018-06-01 16:00:00Z",
#         %20%20%20%20to:%20%222018-06-05%2016:00:00Z%22,%0A          #    to: "2018-06-05 16:00:00Z",
#         %20%20%20%20interval:%20%221d%22)%20%7B%0A                  #    interval: "1d") {
#         %20%20%20%20%20%20activeAddresses,%0A                       #      activeAddresses,
#         %20%20%20%20%20%20datetime%0A                               #      datetime
#         %20%20%20%20%7D%0A                                          #    }
#         %7D%0A"                                                     #}

# Let's build the URL with some variables which makes it easier for us later to automate the process of collecting data.
#Parameters:
base = "https://api.santiment.net/graphql?variables=%7B%7D&query="
fetch = "dailyActiveAddresses"    #dailyActiveAddresses, burnRate, transactionVolume, githubActivity, erc20ExchangeFundsFlow, socialVolume, socialVolumeProjects
slug = "santiment"                #https://api.santiment.net/graphiql?query=%7B%0A%20%20allErc20Projects%20%7B%0A%20%20%09slug%0A%20%20%7D%20%20%0A%7D
start = "2018-01-01"
end = "2018-09-01"
interval = "1d"                   #s, m, h, d, w
fields = c("activeAddresses", "datetime")

URL_nf = paste0(base, "query%20%7B%0A%20%20", fetch, "(%0A%20%20%20%20slug:%20%22", slug, "%22,%0A%20%20%20%20from:%20%22",
                start, "%2000:00:00Z%22,%0A%20%20%20%20to:%20%22", end, "%2016:00:00Z%22,%0A%20%20%20%20interval:%20%22",
                interval, "%22)%20%7B%0A%20%20%20%20%20%20")

URL = URL_nf
for (i in 1:length(fields)) {
  if (i != length(fields)) {
    URL = paste0(URL, "%20%20%20%20%20%20", fields[i], ",%0A")
  } else {
    URL = paste0(URL, "%20%20%20%20%20%20", fields[i], "%0A%20%20%20%20%7D%0A%7D%0A")
  }
}

#Now that we built the URL we need, we can start fetching the data
get_data <- GET(URL)
get_data_text <- content(get_data, "text")  # Convert to "character"
get_data_json <- fromJSON(get_data_text, flatten = TRUE) # Flatten into list
#Should display an array with Date and Amount of Daily Active Addresses for the chosen parameters
View(get_data_json$data$dailyActiveAddresses)
