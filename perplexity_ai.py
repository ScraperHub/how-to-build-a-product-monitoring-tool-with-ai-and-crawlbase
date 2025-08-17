import json
import openai
from datetime import datetime, timedelta

def analyze_data(products):
    if len(products) < 2:
        raise ValueError("Not enough data to analyze")

    analysis_data = {
                "total_records": len(products),
                "date_range": {
                    "earliest": products[-1]["timestamp"],
                    "latest": products[0]["timestamp"]
                },
                "price_history": []
            }

    for product in reversed(products):
        analysis_data["price_history"].append({
            "timestamp": product["timestamp"],
            "price": product["price"],
            "currency": product["currency"]
        })

    prices = [p["price"] for p in analysis_data["price_history"]]
    analysis_data["statistics"] = {
        "min_price": min(prices),
        "max_price": max(prices),
        "current_price": prices[-1],
        "price_range": max(prices) - min(prices),
        "price_variance": sum((p - sum(prices)/len(prices))**2 for p in prices) / len(prices)
    }

    prompt = f"""
    Analyze the following product price data and provide insights in JSON format:

    Product Data:
    {json.dumps(analysis_data, indent=2)}

    Please analyze this data and return a JSON response with the following structure:

    {{
        "anomalies": [
            {{
                "type": "price_spike|price_drop|unusual_pattern",
                "description": "Description of the anomaly",
                "severity": "low|medium|high",
                "timestamp": "When it occurred",
                "confidence": 0.85
            }}
        ],
        "trends": [
            {{
                "type": "increasing|decreasing|stable|volatile",
                "description": "Summary of the trend",
                "percentage_change": -5.2,
                "time_period": "last_week|last_month|overall",
                "confidence": 0.90
            }}
        ],
        "patterns": [
            {{
                "type": "seasonal|weekly|daily|random",
                "description": "Description of the pattern",
                "frequency": "daily|weekly|monthly",
                "confidence": 0.75
            }}
        ],
        "recommendations": [
            "Actionable recommendation based on analysis"
        ]
    }}

    Focus on:
    1. Detect unusual price changes (anomalies) - look for sudden spikes or drops
    2. Identify trends - overall price direction and percentage changes
    3. Classify patterns - seasonal, weekly, or other recurring patterns
    4. Provide actionable insights

    Return only valid JSON, no additional text.
    """
    
    try:
        client = openai.OpenAI(api_key="<perplexity.ai API KEY>", base_url="https://api.perplexity.ai")

        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "system",
                    "content": "You are a data analyst specializing in price analysis. Provide accurate, data-driven insights in JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=2000
        )
        
        analysis_result = json.loads(response.choices[0].message.content)

        analysis_result["metadata"] = {
            "analysis_timestamp": datetime.now().isoformat(),
            "data_points_analyzed": analysis_data["total_records"],
            "model_used": "sonar-pro"
        }
        
        return analysis_result
        
    except openai.AuthenticationError:
        return {
            "error": "OpenAI API authentication failed. Please check your API key.",
            "anomalies": [],
            "trends": [],
            "patterns": []
        }
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse OpenAI response. The model may have returned invalid JSON.",
            "anomalies": [],
            "trends": [],
            "patterns": []
        }
    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}",
            "anomalies": [],
            "trends": [],
            "patterns": []
        }
