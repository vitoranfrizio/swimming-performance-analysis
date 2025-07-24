# -*- coding: utf-8 -*-
"""
Comparação de Avaliações de Natação - 01/01/2025 vs 01/03/2025
@author: Vitor Anfrizio
"""

# %%
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = 'browser'

# %%
# === Dados da 1ª Avaliação ===
data_400m_old = {
    'Distance': [25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400],
    'Time_per_25m': [23.3, 26.8, 28.2, 29.2, 30.4, 30.2, 30.8, 30.7, 30.7, 30.8, 30.8, 31.0, 30.3, 30.9, 29.6, 30.2],
    'Stroke_Count': [25, 26, 27, 27, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28]
}

data_200m_old = {
    'Distance': [25, 50, 75, 100, 125, 150, 175, 200],
    'Time_per_25m': [22.0, 24.0, 26.3, 27.8, 28.6, 29.0, 28.9, 28.2],
    'Stroke_Count': [26, 26, 28, 28, 28, 28, 28, 28]
}

# === Dados da 2ª Avaliação ===
data_400m_new = {
    'Distance': [25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400],
    'Time_per_25m': [15.2,17.9,17.6,17.4,17.4,17.2,18,17.5,17.8,17.3,17.7,17.1,17.9,17.1,17.2,15.2],
    'Stroke_Count': [14, 15, 15, 15, 15, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 17]
}

data_200m_new = {
    'Distance': [25, 50, 75, 100, 125, 150, 175, 200],
    'Time_per_25m': [14.0,16.5,16.1,16.1,16.8,16.7,16.5,16.2],
    'Stroke_Count': [12, 14, 14, 14, 14, 15, 15, 16]
}

# %%
# === Criar DataFrames ===

df_400m_old = pd.DataFrame(data_400m_old)
df_200m_old = pd.DataFrame(data_200m_old)
df_400m_new = pd.DataFrame(data_400m_new)
df_200m_new = pd.DataFrame(data_200m_new)

# %%
# === Calcular Métricas ===

for df in [df_400m_old, df_200m_old, df_400m_new, df_200m_new]:
    df['Velocity'] = 25 / df['Time_per_25m']
    df['SL'] = 25 / df['Stroke_Count']
    df['IE'] = df['Velocity'] * df['SL']
    df['Swolf'] = df['Time_per_25m'] + df['Stroke_Count']

# === Taxa de Braçadas ===
for df in [df_400m_old, df_200m_old, df_400m_new, df_200m_new]:
    df['Stroke_Rate'] = (df['Stroke_Count'] * 60) / df['Time_per_25m']
    df['Rolling_Time_per_25m'] = df['Time_per_25m'].rolling(window=3, min_periods=1).mean()
    df['Rolling_Stroke_Rate'] = df['Stroke_Rate'].rolling(window=3, min_periods=1).mean()

# === Criar Tabelas de Diferença ===
diff_400m = df_400m_new.copy()
diff_200m = df_200m_new.copy()

for col in ['Time_per_25m', 'Stroke_Count', 'Velocity', 'SL', 'IE', 'Swolf', 'Stroke_Rate']:
    diff_400m[col] = df_400m_new[col].round(2).astype(str) + ' (' + (df_400m_new[col] - df_400m_old[col]).round(2).astype(str) + ')'
    diff_200m[col] = df_200m_new[col].round(2).astype(str) + ' (' + (df_200m_new[col] - df_200m_old[col]).round(2).astype(str) + ')'

print("=== TABELA DIFERENÇA 400m ===")
print(diff_400m)

print("\n=== TABELA DIFERENÇA 200m ===")
print(diff_200m)

# %%
# === EXEMPLO DE UM GRÁFICO COMPARATIVO ===


# Velocidade
fig_vel = go.Figure()
fig_vel.add_trace(go.Scatter(x=df_400m_old['Distance'], y=df_400m_old['Velocity'],
                             mode='lines+markers', name='400m (01/01/2025)'))
fig_vel.add_trace(go.Scatter(x=df_400m_new['Distance'], y=df_400m_new['Velocity'],
                             mode='lines+markers', name='400m (01/03/2025)'))
fig_vel.update_layout(title='Comparação Velocidade 400m',
                      xaxis_title='Distância (m)', yaxis_title='Velocidade (m/s)')
fig_vel.show()

# %%
# === SL ===

fig_sl = go.Figure()
fig_sl.add_trace(go.Scatter(
    x=df_400m_old['Distance'], y=df_400m_old['SL'],
    mode='lines+markers', name='400m (01/01/2025)'
))
fig_sl.add_trace(go.Scatter(
    x=df_400m_new['Distance'], y=df_400m_new['SL'],
    mode='lines+markers', name='400m (01/03/2025)'
))
fig_sl.update_layout(
    title='Comparação SL 400m',
    xaxis_title='Distância (m)', yaxis_title='SL (m/braçada)'
)
fig_sl.add_annotation(
    text='ℹ️', x=0, y=1.15, xref='paper', yref='paper',
    showarrow=False, font=dict(size=20),
    hovertext='SL: Comprimento de Braçada. Mede eficiência do alcance.'
)
fig_sl.show()

# %%
# === IE ===

fig_ie = go.Figure()
fig_ie.add_trace(go.Scatter(
    x=df_400m_old['Distance'], y=df_400m_old['IE'],
    mode='lines+markers', name='400m (01/01/2025)'
))
fig_ie.add_trace(go.Scatter(
    x=df_400m_new['Distance'], y=df_400m_new['IE'],
    mode='lines+markers', name='400m (01/03/2025)'
))
fig_ie.update_layout(
    title='Comparação IE 400m',
    xaxis_title='Distância (m)', yaxis_title='IE'
)
fig_ie.add_annotation(
    text='ℹ️', x=0, y=1.15, xref='paper', yref='paper',
    showarrow=False, font=dict(size=20),
    hovertext='IE: Combina Velocidade e SL para medir eficiência técnica.'
)
fig_ie.show()

# %%
# === Swolf ===

fig_swolf = go.Figure()
fig_swolf.add_trace(go.Scatter(
    x=df_400m_old['Distance'], y=df_400m_old['Swolf'],
    mode='lines+markers', name='400m (01/01/2025)'
))
fig_swolf.add_trace(go.Scatter(
    x=df_400m_new['Distance'], y=df_400m_new['Swolf'],
    mode='lines+markers', name='400m (01/03/2025)'
))
fig_swolf.update_layout(
    title='Comparação Swolf 400m',
    xaxis_title='Distância (m)', yaxis_title='Swolf'
)
fig_swolf.add_annotation(
    text='ℹ️', x=0, y=1.15, xref='paper', yref='paper',
    showarrow=False, font=dict(size=20),
    hovertext='Swolf: Tempo + Braçadas. Resume eficiência geral.'
)
fig_swolf.show()

# %%
# === Fadiga 200m ===

fig_fadiga_200m = go.Figure()
fig_fadiga_200m.add_trace(go.Scatter(
    x=df_200m_old['Distance'], y=df_200m_old['Rolling_Time_per_25m'],
    mode='lines+markers', name='Tempo Médio 3 Parciais (01/01/2025)',
    line=dict(color='#1f77b4')
))
fig_fadiga_200m.add_trace(go.Scatter(
    x=df_200m_new['Distance'], y=df_200m_new['Rolling_Time_per_25m'],
    mode='lines+markers', name='Tempo Médio 3 Parciais (01/03/2025)',
    line=dict(color='#1f77b4', dash='dash')
))
fig_fadiga_200m.add_trace(go.Scatter(
    x=df_200m_old['Distance'], y=df_200m_old['Rolling_Stroke_Rate'],
    mode='lines+markers', name='Taxa Média Braçadas (01/01/2025)',
    yaxis='y2', line=dict(color='#ff7f0e')
))
fig_fadiga_200m.add_trace(go.Scatter(
    x=df_200m_new['Distance'], y=df_200m_new['Rolling_Stroke_Rate'],
    mode='lines+markers', name='Taxa Média Braçadas (01/03/2025)',
    yaxis='y2', line=dict(color='#ff7f0e', dash='dash')
))
fig_fadiga_200m.update_layout(
    title='Análise de Fadiga: Médias Móveis - 200m',
    xaxis_title='Distância (m)',
    yaxis=dict(
        title=dict(text='Tempo Médio Parciais (s)', font=dict(color='#1f77b4')),
        tickfont=dict(color='#1f77b4')
    ),
    yaxis2=dict(
        title=dict(text='Taxa Média Braçadas (bpm)', font=dict(color='#ff7f0e')),
        tickfont=dict(color='#ff7f0e'),
        overlaying='y',
        side='right'
    )
)
fig_fadiga_200m.add_annotation(
    text='ℹ️', x=0, y=1.15, xref='paper', yref='paper',
    showarrow=False, font=dict(size=20),
    hovertext='Médias móveis: mostram tendência real de ritmo e cadência.'
)
fig_fadiga_200m.show()

# %%
# === Fadiga 400m ===

fig_fadiga_400m = go.Figure()
fig_fadiga_400m.add_trace(go.Scatter(
    x=df_400m_old['Distance'], y=df_400m_old['Rolling_Time_per_25m'],
    mode='lines+markers', name='Tempo Médio 3 Parciais (01/01/2025)',
    line=dict(color='#1f77b4')
))
fig_fadiga_400m.add_trace(go.Scatter(
    x=df_400m_new['Distance'], y=df_400m_new['Rolling_Time_per_25m'],
    mode='lines+markers', name='Tempo Médio 3 Parciais (01/03/2025)',
    line=dict(color='#1f77b4', dash='dash')
))
fig_fadiga_400m.add_trace(go.Scatter(
    x=df_400m_old['Distance'], y=df_400m_old['Rolling_Stroke_Rate'],
    mode='lines+markers', name='Taxa Média Braçadas (01/01/2025)',
    yaxis='y2', line=dict(color='#ff7f0e')
))
fig_fadiga_400m.add_trace(go.Scatter(
    x=df_400m_new['Distance'], y=df_400m_new['Rolling_Stroke_Rate'],
    mode='lines+markers', name='Taxa Média Braçadas (01/03/2025)',
    yaxis='y2', line=dict(color='#ff7f0e', dash='dash')
))
fig_fadiga_400m.update_layout(
    title='Análise de Fadiga: Médias Móveis - 400m',
    xaxis_title='Distância (m)',
    yaxis=dict(
        title=dict(text='Tempo Médio Parciais (s)', font=dict(color='#1f77b4')),
        tickfont=dict(color='#1f77b4')
    ),
    yaxis2=dict(
        title=dict(text='Taxa Média Braçadas (bpm)', font=dict(color='#ff7f0e')),
        tickfont=dict(color='#ff7f0e'),
        overlaying='y',
        side='right'
    )
)
fig_fadiga_400m.add_annotation(
    text='ℹ️', x=0, y=1.15, xref='paper', yref='paper',
    showarrow=False, font=dict(size=20),
    hovertext='Médias móveis: mostram tendência real de ritmo e cadência.'
)
fig_fadiga_400m.show()

