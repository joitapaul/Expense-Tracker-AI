def predict_category(title):

    title = title.lower()

    categories = {

        "Food": ["swiggy", "zomato", "restaurant", "pizza", "burger", "food", "cafe", "apnamart"],

        "Transport": ["uber", "ola", "metro", "bus", "train", "taxi", "auto"],

        "Shopping": ["amazon", "flipkart", "myntra", "shopping", "clothes","apna mart"],

        "Bills": ["electricity", "bill", "recharge", "wifi", "water", "gas", "phone bill"],

        "Entertainment": ["movie", "netflix", "hotstar", "cinema"],

        "Healthcare": ["doctor", "medicine", "hospital", "pharmacy", "treatment"],

        "Education": ["course", "books", "udemy", "coursera", "exam fee", "tuition"],

        "Rent": ["rent", "house rent", "room rent"],

        "Groceries": ["milk", "vegetables", "grocery", "supermarket", "bigbasket"],

        "Travel": ["flight", "hotel", "trip", "travel", "airbnb"],

        "Subscriptions": ["spotify", "prime", "subscription", "youtube premium"]

    }

    for category, keywords in categories.items():
        for word in keywords:
            if word in title:
                return category

    return "Other"