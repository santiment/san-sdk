defmodule SanGraphqlEx do
  require Logger

  @doc ~s"""
  Returns a list of maps with `activeAddresses` and `datetime` keys.
  """
  def daily_active_addresses() do
    case daily_active_addresses_query do
      {:ok, response} ->
        %Neuron.Response{body: %{"data" => %{"dailyActiveAddresses" => active_addresses}}} =
          response

        active_addresses

      error ->
        Logger.error("Cannot fetch daily active addresses. Reason: #{inspect(error)}")
    end
  end

  @doc ~s"""
  Returns a list of all project identifiers. These project identifiers can be used to query
  data for a specific project. The identifier should be provided to the `slug` field
  as seen in the `daily_active_addresses/0` example.
  """
  def project_slugs() do
    case project_slugs_query() do
      {:ok, response} ->
        %Neuron.Response{body: %{"data" => %{"allProjects" => all_projects}}} = response

        all_projects
        |> Enum.map(fn %{"slug" => slug} -> slug end)

      error ->
        Logger.error("Cannot fetch projects' slugs. Reason: #{inspect(error)}")
    end
  end

  # Private functions

  defp project_slugs_query() do
    Neuron.Config.set(url: "https://api.santiment.net/graphql")

    Neuron.query("""
    {
      allProjects{
        slug
      }
    }
    """)
  end

  defp daily_active_addresses_query() do
    Neuron.Config.set(url: "https://api.santiment.net/graphql")

    Neuron.query("""
    {
      dailyActiveAddresses(
        slug: "santiment",
        from: "2017-07-12 00:00:00Z",
        to: "2017-07-15 00:00:00Z") {
          activeAddresses,
          datetime
        }
    }
    """)
  end
end
