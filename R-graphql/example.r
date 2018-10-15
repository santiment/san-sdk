library("ghql")
library("jsonlite")
library("httr")

API_URL <- "https://api.santiment.net/graphql"
# change with real Apikey
API_KEY <- Sys.getenv("SANBASE_API_KEY")

cli <- GraphqlClient$new(
  url = API_URL,
  headers = add_headers(Authorization = paste0("Apikey ", API_KEY))
)

qry <- Query$new()

# Get all project identifiers (slugs). They are used in other queries to get data for a specific project.
qry$query('all_projects', '{
    allProjects {
        slug
    }
}')

all_projects <- cli$exec(qry$queries$all_projects)

print(fromJSON(all_projects))

# Get Daily Active Addresses
qry$query('daa', '{
    dailyActiveAddresses(
        slug: "santiment",
        from: "2018-08-01 00:00:00Z",
        to: "2018-08-05 00:00:00Z") {
            activeAddresses,
            datetime
        }
}')

daa <- cli$exec(qry$queries$daa)
print(fromJSON(daa))
