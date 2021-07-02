x_years = df['Date']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_years,
                         y=df['Temps annuel de travail (SNCF)'],
                         name='SNCF',
                         marker_color='rgb(55, 83, 109)'
                         )
                  )
    fig.add_trace(go.Bar(x=x_years,
                         y=df['Temps annuel de travail (France)'],
                         name='France',
                         marker_color='rgb(26, 118, 255)'
                         )
                  )

    fig.update_layout(
        title='Temps de Travail',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Heures',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )
    fig.show()