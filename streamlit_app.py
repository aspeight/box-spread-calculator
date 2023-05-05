import streamlit as st
import pandas as pd
import datetime

if not st.session_state:
    st.session_state['trade_date'] = datetime.date.today()
    st.session_state['expiration_date'] = st.session_state['trade_date'] + datetime.timedelta(days=90)
    st.session_state['box_width'] = 1000
    st.session_state['extra_days'] = 2
    st.session_state['days_per_year'] = 360
    st.session_state['yield_pct'] = 6.0

if 'counter' not in st.session_state:
    st.session_state.counter = 0

def yield_from(
    trade_date,
    expiration_date,
    box_width,
    extra_days,
    box_price,
    days_per_year,
):
    num_days = (pd.to_datetime(expiration_date) - pd.to_datetime(trade_date)).days + extra_days
    tau = num_days / days_per_year
    return 100 * (box_width / box_price - 1) / tau


def price_from(
    trade_date,
    expiration_date,
    box_width,
    extra_days,
    yield_pct,
    days_per_year,
):
    num_days = (pd.to_datetime(expiration_date) - pd.to_datetime(trade_date)).days + extra_days
    tau = num_days / days_per_year
    return box_width / (1 + 0.01*yield_pct * tau)
    
def compute_box_price():
    st.session_state.counter += 1
    return round(price_from(
        trade_date=st.session_state['trade_date'],
        expiration_date=st.session_state['expiration_date'],
        box_width=st.session_state['box_width'],
        extra_days=st.session_state['extra_days'],
        yield_pct=st.session_state['yield_pct'],
        days_per_year=st.session_state['days_per_year'],     
    ), 4)

def handle_price_update():
    st.session_state['yield_pct'] = yield_from(
        trade_date=st.session_state['trade_date'],
        expiration_date=st.session_state['expiration_date'],
        box_width=st.session_state['box_width'],
        extra_days=st.session_state['extra_days'],
        box_price=st.session_state['box_price'],
        days_per_year=st.session_state['days_per_year'],     
    )


st.title('Box Spread Calculator')

st.markdown(
    'Computes prices/yields of a box spread: \n'
    '  - B is the width of the strikes \n'
    '  - P is the price of the box spread \n'
    '  - R is the yield of the box spread \n'
    '  - T is the fraction of year between trade and expiration dates \n'
    '    - T may include a few extra days to allow funds to settle \n'
    '\n'
    '`B = (1 + R * T) * P`\n'
)



st.date_input('Trade Date: ', key='trade_date')
st.date_input('Expiration Date: ', key='expiration_date')
st.number_input('Box Strike Width: ', key='box_width', min_value=0, max_value=999_999)
st.number_input('Extra Settle Days: ', key='extra_days', min_value=-5, max_value=10)
st.selectbox('Days per year: ', [360, 365], key='days_per_year')
st.number_input('Yield (pct): ', key='yield_pct', step=0.01,)
st.number_input('Box Price: ', value=compute_box_price(), disabled=True, format='%.3f')

#st.date_input('Trade Date: ', key='trade_date')
#st.date_input('Expiration Date: ', key='expiration_date', value=st.session_state['trade_date'] + datetime.timedelta(days=90))
#st.number_input('Box Strike Width: ', key='box_width', value=1000, min_value=0, max_value=999_999)
#st.number_input('Extra Settle Days: ', key='extra_days', value=3, min_value=-5, max_value=10)
#st.selectbox('Days per year: ', [360, 365], index=0, key='days_per_year')
#st.number_input('Yield (pct): ', key='yield_pct', value=5., step=0.01,)
#st.number_input('Box Price: ', key='box_price', value=compute_box_price(), disabled=True, format='%.3f')

#st.button('Solve for yield given price', on_click=handle_price_update())



st.json(st.session_state)
    


