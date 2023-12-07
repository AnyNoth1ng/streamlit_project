import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# read files
clients = pd.read_csv('/home/egor/HSE/Applied_python/applpython_hw_1/datasets/D_clients.csv')
close_loan = pd.read_csv('/home/egor/HSE/Applied_python/applpython_hw_1/datasets/D_close_loan.csv')
job = pd.read_csv('/home/egor/HSE/Applied_python/applpython_hw_1/datasets/D_job.csv')
last_credit = pd.read_csv('/home/egor/HSE/Applied_python/applpython_hw_1/datasets/D_last_credit.csv')
loan = pd.read_csv('/home/egor/HSE/Applied_python/applpython_hw_1/datasets/D_loan.csv')
pens = pd.read_csv('/home/egor/HSE/Applied_python/applpython_hw_1/datasets/D_pens.csv')
salary = pd.read_csv('/home/egor/HSE/Applied_python/applpython_hw_1/datasets/D_salary.csv')
target = pd.read_csv('/home/egor/HSE/Applied_python/applpython_hw_1/datasets/D_target.csv')
work = pd.read_csv('/home/egor/HSE/Applied_python/applpython_hw_1/datasets/D_work.csv')

# work with duplicates
salary = salary.drop_duplicates(keep='first')

# merge tables loan
merged_loans = pd.merge(loan, close_loan, on='ID_LOAN', how='left')
merged_loans = merged_loans.groupby(['ID_CLIENT']).agg({"ID_LOAN": 'count', 'CLOSED_FL': 'sum'}).reset_index()
merged_loans.columns = ['ID_CLIENT', 'LOAN_NUM_TOTAL', 'LOAN_NUM_CLOSED ']

# merge all tables

merged_all = pd.merge(clients, target, left_on='ID', right_on="ID_CLIENT", how='left').drop(['ID_CLIENT', 'AGREEMENT_RK'], axis=1)\
    .merge(job, left_on="ID", right_on="ID_CLIENT", how='left').drop('ID_CLIENT', axis=1)\
    .merge(salary, left_on="ID", right_on="ID_CLIENT", how='left').drop('ID_CLIENT',axis=1) \
    .merge(last_credit, left_on="ID", right_on="ID_CLIENT", how='left').drop('ID_CLIENT', axis=1) \
    .merge(merged_loans, left_on="ID", right_on="ID_CLIENT", how='left').drop('ID_CLIENT', axis=1)\

merged_all['SOCSTATUS_WORK_FL'] = merged_all['SOCSTATUS_WORK_FL'].map({1: 'работает', 0: 'не работает'})
merged_all['SOCSTATUS_PENS_FL'] = merged_all['SOCSTATUS_PENS_FL'].map({1: 'пенсионер', 0: 'не пенсионер'})
merged_all['GENDER'] = merged_all['GENDER'].map({1: 'мужчина', 0: 'женщина'})
merged_all['FL_PRESENCE_FL'] = merged_all['FL_PRESENCE_FL'].map({1: 'есть', 0: 'нет'})
merged_all['TARGET_new'] = merged_all['TARGET'].map({1: 'был отклик', 0: 'отклика не было'})

# delete old columns in merged_all table
merged_all = merged_all.drop(columns = ['ID','REG_ADDRESS_PROVINCE','POSTAL_ADDRESS_PROVINCE'])

# group type dates
int_float_columns = merged_all.select_dtypes(include=[np.int64, np.float64]).columns
cat_columns = ['GEN_INDUSTRY','FACT_ADDRESS_PROVINCE']
another_col = [i for i in merged_all.select_dtypes(include=[object]).columns if i not in cat_columns]
col_1 = ['WORK_TIME']


merge_columns = list(merged_all.columns)
names = ['Возраст',
            'Пол',
            'Образование',
            'Семейное положение',
            'Кол-во детей',
            'Кол-во иждевенцев',
            'Статус работы',
            'Статус пенсии',
            'Регион фактического пребывания',
            'Наличие квартиры',
            'Кол-во автомобилей',
            'Целевая - отклик_число',
            'Отрасль работы',
            'Должность',
            'Направление деятельности',
            'Время работы на текущем месте',
            'Семейный доход',
            'Личный доход',
            'Сумма последнего кредита',
            'Срок кредита',
            'Первоначальный взнос',
            'Кол-во кредитов',
            'Кол-во закрытых кредитов',
            'Целевая - отклик'
               ]

dict_df = {
    'cls' : merge_columns,
    'nms' : names
}
df_1 = pd.DataFrame(dict_df)


# del_out_col
def vibros_delet(x):
    q1 = x.quantile(0.25)
    q3 = x.quantile(0.75)
    iqr = q3 - q1
    limmax = q3 + 1.5*iqr
    limmin = q1 - 1.5*iqr
    good_col = x[(x >= limmin) & (x <= limmax)]
    return good_col
# dist_bar
def funcplot_x(df):
    if df.nunique() > 20:
        bin= 15
    else:
        bin = df.nunique()+1
    n = df.name
    col_name = df_1[df_1.cls == n].nms.values
    nums = list(df)
    graphics = go.Figure()
    graphics.add_trace(go.Histogram(
        x = nums,
        nbinsx = bin,
        name = 'count',
        marker_color ='darkviolet',
        texttemplate = '%{y}',
        textfont_size = 20,
        textfont_color = 'burlywood'
    ))

    graphics.update_layout(title = f'{col_name[0]}',
                           xaxis_title=f'{col_name[0]}',
                           yaxis_title='Количество клиентов'
    )
    return graphics

# dist_bar_y
def funcplot_y(df):
    if df.nunique() > 20:
        bin = 15
    else:
        bin = df.nunique()+1
    n = df.name
    col_name = df_1[df_1.cls == n].nms.values
    nums = list(df)
    graphics = go.Figure()
    graphics.add_trace(go.Histogram(
        y = nums,
        nbinsx = bin,
        name = 'count',
        marker_color ='#00ff00',
        texttemplate = '%{y}',
        textfont_size = 20,
        textfont_color = 'palegreen'
    ))
    graphics.update_layout(title = f'{col_name[0]}',
                           xaxis_title=f'{col_name[0]}',
                           yaxis_title='Количество клиентов',
                           width = 500,
                           height = 1000
    )
    return graphics

# box_plot
def plotly_box(df):
    n = df.name
    x_1 = df.values
    graphics = go.Figure()
    graphics.add_trace(go.Box(x = x_1, name = n))
    return graphics

# stat_data#
def percintls(df):
    min_ = round(min(df), 1)
    min_25 = round(np.percentile(df,25),1)
    med = round(df.median(),1)
    med_75 = round(np.percentile(df,75),1)
    mean = round(df.mean(),1)
    max_ = round(max(df),1)

    df_pers ={
        'Minimum': [min_],
        '25%' : [min_25],
        '50%' : [med],
        '75%' : [med_75],
        'mean' : [mean],
        'Maximum' : [max_]
    }
    df_finish = pd.DataFrame.from_dict(df_pers)
    return df_finish

# corr_bar
def correl_card(df):
    cor = df.corr()
    graphic = go.Figure()
    graphic.add_trace(
        go.Heatmap(
            x = cor.columns,
            y = cor.index,
            z = np.array(cor),
            colorscale = 'Greens',
            text = cor.values,
            texttemplate = '%{text:.2f}',
        )
    )
    return graphic
# hist_target
def histogr_col(col):
    df = merged_all
    col_name = df_1[df_1.cls == col].nms.values
    graphic = px.histogram(df, x=col, color="SOCSTATUS_WORK_FL").update_xaxes(categoryorder='total descending')
    graphic.update_layout(title= f'Зависимость {col_name[0]} от целевой переменной',
                          xaxis_title = f'{col_name[0]}',
                          yaxis_title = 'total clientov')
    return graphic

colors = ['#ff0000', '#00ff00', '#0000ff','#ffff00', '#000000']

#pie_chart
def circle_diag(df):
    n = df.name
    col_name = df_1[df_1.cls == n].nms.values
    df = df.value_counts()
    graphic = go.Figure()
    graphic.add_trace(go.Pie(labels=df.index, values=df.values, marker_colors = colors))
    graphic.update_layout(title = col_name[0])
    graphic.update_traces(hole=.4, textposition = 'outside', textinfo = 'percent')

    return graphic

# st.title("HW1")
st.write("EDA")

tabs = ['Графики распределения', 'Матрица корреляций', 'График зависимости целевой переменной']

selected_tab = st.selectbox('Выберите вкладку', tabs)
if selected_tab == tabs[0]:
    option = st.selectbox('Графики распределения каждого признака', list(merged_all.columns))
    if option in int_float_columns:
        if option in col_1:
            st.info(f"В графике по {option} не были учтены выбросы,так как в задании про это не говорилось")
            st.plotly_chart(funcplot_x(vibros_delet(merged_all[option])), use_container_width = True)
        else:
            st.plotly_chart(funcplot_x(merged_all[option]),use_container_width = True)
        st.plotly_chart(plotly_box(merged_all[option]), use_container_width = True)
        st.dataframe(percintls(merged_all[option]))
    elif option in cat_columns:
        st.plotly_chart(funcplot_y(merged_all[option]), use_container_width= True)
    else:
        st.plotly_chart(circle_diag(merged_all[option]), use_container_width=True)
elif selected_tab == tabs[1]:
    st.info("Матрица корреляции ссделана только для числовых признаков")
    st.plotly_chart(correl_card(merged_all[int_float_columns]), use_container_width=True)

elif selected_tab == tabs[2]:
    option2 = st.selectbox('Графики распределения каждого признака', list(merged_all.columns))
    st.plotly_chart(histogr_col(option2), use_container_width=True)


