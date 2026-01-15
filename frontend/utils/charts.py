"""
Fonctions de visualisation réutilisables
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_bar_chart(data, x, y, title, color=None):
    """Crée un graphique en barres horizontal"""
    fig = px.bar(
        data,
        x=x,
        y=y,
        orientation='h',
        title=title,
        color=color,
        color_continuous_scale='Blues' if color else None
    )
    fig.update_layout(height=600, showlegend=False)
    return fig

def create_pie_chart(data, values, names, title):
    """Crée un camembert"""
    fig = px.pie(
        data,
        values=values,
        names=names,
        title=title
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    return fig

def create_map_france(data, locations, color, hover_name, title):
    """Crée une carte de France choroplèthe"""
    fig = px.choropleth(
        data,
        locations=locations,
        locationmode='ISO-3',
        color=color,
        hover_name=hover_name,
        title=title,
        color_continuous_scale='Reds',
        scope='europe'
    )
    
    fig.update_geos(
        fitbounds="locations",
        visible=True,
        showcountries=True,
        showland=True,
        landcolor="lightgray"
    )
    
    fig.update_layout(height=700)
    return fig

def format_number(number):
    """Formate un nombre avec des espaces"""
    return f"{int(number):,}".replace(',', ' ')

def format_currency(amount):
    """Formate un montant en euros"""
    return f"{float(amount):,.2f} €".replace(',', ' ')