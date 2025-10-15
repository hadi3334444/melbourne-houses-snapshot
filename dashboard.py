{\rtf1\ansi\ansicpg1252\cocoartf2708
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import pandas as pd\
import matplotlib.pyplot as plt\
import seaborn as sns\
import plotly.express as px\
from dash import Dash, html, dcc\
df = pd.read_csv("melb_data.csv")\
\
# Clean data\
df = df.dropna(subset=["Price", "Rooms", "Distance", "Landsize"])\
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")\
\
# Create summary data\
avg_price_by_suburb = df.groupby("Suburb")["Price"].mean().sort_values(ascending=False).head(10).reset_index()\
price_by_rooms = df.groupby("Rooms")["Price"].mean().reset_index()\
price_over_time = df.groupby(df["Date"].dt.to_period("M"))["Price"].mean().reset_index()\
price_over_time["Date"] = price_over_time["Date"].astype(str)\
\
# Create charts\
fig1 = px.bar(avg_price_by_suburb, x="Price", y="Suburb", orientation="h",\
              title="Top 10 Most Expensive Suburbs in Melbourne",\
              color="Price", color_continuous_scale="viridis")\
\
fig2 = px.line(price_over_time, x="Date", y="Price",\
               title="Average House Price Over Time")\
\
fig3 = px.scatter(df, x="Rooms", y="Price",\
                  size="Landsize", color="Distance",\
                  hover_name="Suburb",\
                  title="Rooms vs Price (Bubble size = Land size)")\
\
\
# Save all figures as images\
fig1.write_image("top10_suburbs.png")\
fig2.write_image("rooms_vs_price.png")\
fig3.write_image("price_over_time.png")\
\
\
# Create dashboard app\
app = Dash(__name__)\
\
app.layout = html.Div([\
    html.H1("\uc0\u55356 \u57313  Melbourne Housing Dashboard", style=\{"textAlign": "center"\}),\
    html.P("Explore housing trends, suburbs, and pricing patterns across Melbourne.",\
           style=\{"textAlign": "center"\}),\
\
    dcc.Graph(figure=fig1),\
    dcc.Graph(figure=fig2),\
    dcc.Graph(figure=fig3)\
])\
\
# Run the app\
if __name__ == "__main__":\
    app.run(debug=True)\
    \
\
}