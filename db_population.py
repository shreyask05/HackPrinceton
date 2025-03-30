import psycopg2
from backend import (
    get_latest_bills,
    get_bill_details,
    extract_text_from_html_url,
    analyze_sentiment_chunks,
    generate_bill_analysis,
    map_to_industry
)
from bs4 import XMLParsedAsHTMLWarning
import warnings

# Suppress XML parser warning
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def establish_connection():
    """Establish connection to PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Bills",
            user="postgres",  # Replace with your actual username
            password="030305",  # Replace with your actual password
            port=5434
        )
        print("Database connection established successfully")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def create_table_if_not_exists(cursor):
    """Create the Bills table if it doesn't exist"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS public.Bills (
        num INTEGER,
        type TEXT,
        title TEXT,
        congress INTEGER,
        summary TEXT,
        sponsors TEXT[],
        justification TEXT,
        effect TEXT,
        confidence_score DOUBLE PRECISION,
        sectors TEXT[]
    )
    """
    try:
        cursor.execute(create_table_query)
        print("Table created or already exists")
        return True
    except Exception as e:
        print(f"Error creating table: {e}")
        return False


def insert_bill_data(conn, cursor, bill_data):
    """Insert bill data into the database with transaction handling."""
    query = """
        INSERT INTO public."Bills" (num, type, title, congress, summary, sponsors, justification, effect, confidence_score, sectors)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        bill_data.get("bill_number", None),
        bill_data.get("bill_type", None),
        bill_data.get("title", "Unknown Title"),
        bill_data.get("congress", None),
        bill_data.get("summary", ""),
        bill_data.get("sponsors", []),
        bill_data.get("justification", ""),
        bill_data.get("effect", ""),
        bill_data.get("confidence_score", None),
        bill_data.get("sectors", [])
    )

    try:
        cursor.execute(query, values)
        conn.commit()
        print(f"Successfully inserted bill {bill_data['bill_type']} {bill_data['bill_number']} into database.")
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error inserting bill {bill_data['bill_type']} {bill_data['bill_number']}: {e}")
        return False


def populate_database():
    """Query 250 bills and add only the ones with text to the database"""
    conn = establish_connection()
    if not conn:
        return

    cursor = conn.cursor()

    # Create table if it doesn't exist
    if not create_table_if_not_exists(cursor):
        cursor.close()
        conn.close()
        return

    bills_with_text = 0
    total_bills = 0

    # List of possible document suffixes to try
    suffixes = [
        "enr.xml", "enr.htm",
        "eh.xml", "eh.htm",
        "ih.xml", "ih.htm",
        "is.xml", "is.htm"
    ]

    # Get a large batch of bills at once
    print("Fetching 250 bills...")
    bills_data = get_latest_bills(5)

    if not bills_data or 'bills' not in bills_data:
        print("No bills data returned from API")
        cursor.close()
        conn.close()
        return

    total_bills = len(bills_data['bills'])
    print(f"Retrieved {total_bills} bills to process")

    for bill in bills_data['bills']:
        title = bill.get("title", "Unknown Title")
        congress = bill.get('congress')
        bill_type = bill.get('type')
        bill_number = bill.get('number')

        if not all([congress, bill_type, bill_number]):
            print(f"Missing essential bill data, skipping")
            continue

        print(f"Processing bill: {bill_type} {bill_number}")

        # Try each suffix until we find one that works
        bill_text = None
        used_suffix = None

        for suffix in suffixes:
            text_url = f"https://www.congress.gov/{congress}/bills/{bill_type.lower()}{bill_number}/BILLS-{congress}{bill_type.lower()}{bill_number}{suffix}"
            try:
                temp_text = extract_text_from_html_url(text_url)
                if temp_text:
                    bill_text = temp_text
                    used_suffix = suffix
                    print(f"✅ Text found for {bill_type} {bill_number} using suffix: {suffix}")
                    break
            except Exception as e:
                print(f"Error checking suffix {suffix} for {bill_type} {bill_number}: {e}")
                continue

        # Skip bills without text in any format
        if not bill_text:
            print(f"No text available for {bill_type} {bill_number} in any format, skipping")
            continue

        bills_with_text += 1

        try:
            # Get detailed bill data
            bill_details = get_bill_details(congress, bill_type, bill_number)

            # Analyze sentiment and generate insights
            bill_text = bill_text[:20]  # Truncate if needed
            sentiment_label, sentiment_scores = analyze_sentiment_chunks(bill_text[:8000])

            # Get confidence score for FinBERT
            label_map = {"negative": 0, "neutral": 1, "positive": 2}
            reverse_label_map = {0: "negative", 1: "neutral", 2: "positive"}
            sentiment_index = label_map.get(sentiment_label, 1)
            fin_score = float(sentiment_scores[sentiment_index])

            # Generate bill analysis using Gemini
            analysis = generate_bill_analysis(congress=congress, bill_number=bill_number, bill_text=bill_text[:8000])

            # Extract data from analysis
            lines = analysis.strip().split("\n")
            summary = next((line.split("3.", 1)[1].strip() for line in lines if line.startswith("3.")), "")
            justification = next((line.split("4.", 1)[1].strip() for line in lines if line.startswith("4.")), "")

            # Extract Gemini sentiment and confidence
            gemini_sentiment = None
            gemini_score = None

            for line in lines:
                if line.lower().startswith("1."):
                    gemini_sentiment = line.split(".")[1].strip().lower()
                elif line.lower().startswith("2."):
                    percent_text = line.split(".")[1].strip().replace("%", "")
                    try:
                        gemini_score = float(percent_text) / 100
                    except ValueError:
                        gemini_score = None

            # If Gemini analysis is successful, calculate hybrid sentiment
            if gemini_sentiment is not None and gemini_score is not None:
                # Convert sentiments to index
                fin_label_idx = label_map.get(sentiment_label, 1)
                gemini_label_idx = label_map.get(gemini_sentiment, 1)

                # Calculate weighted hybrid sentiment (30% FinBERT, 70% Gemini)
                hybrid_position = 0.3 * fin_label_idx + 0.7 * gemini_label_idx

                # Use narrower thresholds for neutral classification
                if hybrid_position < 0.85:  # Was effectively 0.5
                    hybrid_index = 0  # Negative
                elif hybrid_position > 1.15:  # Was effectively 1.5
                    hybrid_index = 2  # Positive
                else:
                    hybrid_index = 1  # Neutral

                hybrid_sentiment = reverse_label_map[hybrid_index]

                # Set final sentiment and confidence
                final_sentiment = hybrid_sentiment
                confidence_score = 0.3 * fin_score + 0.7 * gemini_score
            else:
                # Fallback to FinBERT if Gemini doesn't work
                final_sentiment = sentiment_label
                confidence_score = fin_score

            # Create effect field based on final sentiment
            effect_map = {
                "positive": "This bill is likely to have a positive impact on financial markets.",
                "neutral": "This bill is likely to have a neutral impact on financial markets.",
                "negative": "This bill is likely to have a negative impact on financial markets."
            }
            effect = effect_map.get(final_sentiment, "Impact on financial markets is uncertain.")

            # Map affected industry sectors
            subjects = bill_details.get("subjects", [])
            sectors = map_to_industry(subjects, title=title)
            if not sectors:
                sectors = ["General"]

            # Prepare data for insertion
            prepared_data = {
                "bill_number": bill_number,
                "bill_type": bill_type,
                "title": title,
                "congress": congress,
                "summary": summary,
                "sponsors": [s.get("fullName", "Unknown") for s in bill_details.get("sponsors", [])],
                "justification": justification,
                "effect": effect,
                "confidence_score": confidence_score,
                "sectors": sectors
            }

            # Insert into database
            insert_bill_data(conn, cursor, prepared_data)

        except Exception as e:
            print(f"Error processing bill {bill_type} {bill_number}: {e}")

    print(f"Completed database population.")
    print(f"Found {bills_with_text} bills with text out of {total_bills} total bills.")

    cursor.close()
    conn.close()
    print("Database connection closed")

if __name__ == "__main__":
    populate_database()
