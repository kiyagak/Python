import numpy

data = {
    "gm_url": "https://www.url.com/",
    "results": [
        {
            "marque": "Alfa",
            "sold": True,
            "price_int_eu": 49280
        },
        {
            "marque": "Alfa",
            "sold": True,
            "price_int_eu": 46000
        }
    ]
}

results = data["results"]

prices = [x["price_int_eu"] for x in results]
data["mean"] = sum(prices) / len(prices)

print(data['mean'])