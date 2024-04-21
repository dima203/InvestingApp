import flet


def main(page: flet.Page) -> None:
    page.title = 'Investing App'
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.theme = flet.Theme(
        color_scheme_seed='teal'
    )
    page.scroll = flet.ScrollMode.ADAPTIVE
    page.on_scroll_interval = 0

    start_money_field = flet.TextField(label='Начальная сумма', expand=True)
    added_money = flet.TextField(label='Дополнительный взнос', expand=True)
    percent_field = flet.TextField(label='Процентная ставка')
    tax = flet.TextField(label='Комиссия банка')
    investing_time = flet.TextField(label='Длительность вклада')

    def close_interval(e):
        chart_interval.close_view(e.control.data)

    chart_interval = flet.SearchBar(
        view_elevation=4,
        bar_hint_text="Search colors...",
        view_hint_text="Choose a color from the suggestions...",
        controls=[
            flet.ListTile(title=flet.Text(f'Day'), on_click=close_interval, data='day'),
            flet.ListTile(title=flet.Text(f'Hour'), on_click=close_interval, data='hour'),
            flet.ListTile(title=flet.Text(f'Month'), on_click=close_interval, data='month'),
        ],
    )

    chart = flet.LineChart(
        border=flet.border.all(3, flet.colors.with_opacity(0.7, flet.colors.ON_PRIMARY)),
        left_axis=flet.ChartAxis(
            title=flet.Text('Сумма'),
            title_size=80,
        ),
        bottom_axis=flet.ChartAxis(
            title=flet.Text('Время'),
            title_size=80,
        ),
        expand=True,
        height=500
    )

    def calculate(e):
        money = float(start_money_field.value)
        data = [flet.LineChartDataPoint(0, money)]
        interval = chart_interval.value
        months, days = divmod(int(investing_time.value), 30)

        for month in range(months + 1):
            if month == months and days == 0:
                break
            money += float(added_money.value)
            days_range = days if month == months else 30
            for day in range(days_range):
                for hour in range(24):
                    money += money * float(percent_field.value) / 12 / 30 / 24 * (1 - float(tax.value))
                    if interval == 'hour':
                        data.append(flet.LineChartDataPoint(month * 30 * 24 + day * 24 + hour + 1, money,
                                                            tooltip=f'{money:.4f}'))
                if interval == 'day':
                    data.append(flet.LineChartDataPoint(month * 30 + day + 1, money,
                                                        tooltip=f'{money:.4f}'))
            if interval == 'month':
                data.append(flet.LineChartDataPoint(month + 1, money,
                                                    tooltip=f'{money:.4f}'))

        data = flet.LineChartData(data_points=data)

        horizontal_labels = []
        label_money = float(start_money_field.value)
        while label_money < money:
            horizontal_labels.append(flet.ChartAxisLabel(
                value=label_money,
                label=flet.Text(f'{label_money:.1f}')
            ))
            label_money *= 2

        chart.horizontal_grid_lines = flet.ChartGridLines(
            interval=float(start_money_field.value),
            color=flet.colors.with_opacity(0.2, flet.colors.ON_SURFACE), width=1
        )

        chart.vertical_grid_lines = flet.ChartGridLines(
            interval=30 if interval == 'day' else 1 if interval == 'month' else 30 * 24,
            color=flet.colors.with_opacity(0.2, flet.colors.ON_SURFACE), width=1
        )

        chart.left_axis = flet.ChartAxis(
            title=flet.Text('Сумма'),
            title_size=80,
            labels=horizontal_labels,
            labels_size=40,
        )
        chart.bottom_axis = flet.ChartAxis(
            title=flet.Text('Время'),
            title_size=80,
            labels_interval=30 if interval == 'day' else 1 if interval == 'month' else 30 * 24,
            show_labels=True,
            labels_size=40,
        )
        chart.data_series = [data]
        chart.update()

    page.add(flet.Column(
        [
            flet.Row(
                [
                    flet.Text('Investing App', size=30),
                ],
                alignment=flet.MainAxisAlignment.CENTER
            ),
            flet.Row(
                [
                    flet.Container(start_money_field, expand=True, margin=flet.Margin(0, 0, 5, 0)),
                    flet.Container(added_money, expand=True, margin=flet.Margin(5, 0, 0, 0)),
                ],
                alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                spacing=10,
                adaptive=True
            ),
            percent_field,
            tax,
            investing_time,
            chart_interval,
            flet.Row(
                [
                    flet.FilledButton('Calculate', on_click=calculate),
                ],
                alignment=flet.MainAxisAlignment.CENTER
            ),
            flet.Row(
                [
                    chart,
                ],
                alignment=flet.MainAxisAlignment.CENTER
            )
        ],
        width=700,
        alignment=flet.MainAxisAlignment.CENTER,
    ))


flet.app(target=main, view=flet.FLET_APP)
