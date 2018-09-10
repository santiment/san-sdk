#!/usr/bin/env ruby

# Example Santiment API wrapper in ruby language

require 'httparty'

API_URL = "https://api.santiment.net/graphql"

class GraphqlClient
  def initialize(url, api_key: nil)
    @url = url
    @api_key = api_key
  end

  def execute(query:, variables: {})
    headers = { 'Content-Type'  => 'application/json' }
    headers['Authorization'] = "Apikey #{@api_key}" if @api_key

    body = {
      query: query,
      variables: variables
    }.to_json

    HTTParty.post(
      @url,
      headers: headers,
      body: body,
      verify: false
    )
  end
end

client = GraphqlClient.new(API_URL)

# Get all projects
projects = client.execute(
  query: %q(
    {
      allProjects {
        slug
      }
    }
  )
).parsed_response

puts projects.inspect

# Get Daily Active Addresses for Santiment
daa = client.execute(
  query: %q(
    {
      dailyActiveAddresses(
        slug: "santiment",
        from: "2018-08-01 00:00:00Z",
        to: "2018-08-05 00:00:00Z") {
          activeAddresses,
          datetime
        }
    }
  )
).parsed_response

puts daa.inspect
