class BookingDeeplinkGenerator:
    @staticmethod
    def bereitstellungDeeplink(reiseziel):
        base_url = "https://www.booking.com/searchresults.html"
        city_query = reiseziel.name.replace(" ", "+")
        country_query = reiseziel.name.replace(" ", "+")
        return f"{base_url}?ss={city_query}+{country_query}"
