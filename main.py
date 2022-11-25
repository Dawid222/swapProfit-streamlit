import streamlit as st
import requests
from requests import Request, Session
import json
from streamlit_lottie import st_lottie

red = "\033[1;31m"

col1, col2, col3 = st.columns([1, 8, 1])

with col2:
    st.title("Calculate your swap profit!")


    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)


    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()


    lottie_coding = load_lottiefile("89118-money.json")  # replace link to local lottie file
    lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_ml0yft0o.json")

    st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",  # medium ; high
        height=400,
        width=400,
        key=None,
    )

amountGNSBT = st.number_input("How many gNSBT you get?:", min_value = 1)

currentBR = requests.get('https://beta.neutrino.at/api/explorer/get_br').text
br = json.loads(currentBR) * 100
br1 = format(br, '.6f')
st.markdown(f'Current BR: {br1}')

currentWavesPrice = requests.get('https://beta.neutrino.at/api/explorer/get_current_price').text
wavesPrice = json.loads(currentWavesPrice)
wavesPrice1 = format(wavesPrice, '.6f')
st.markdown(f'Current WAVES price in sc: {wavesPrice1}')
surfPrice = br / 100
surfPrice1 = format(surfPrice, '.6f')
st.markdown(f'Current SURF price in sc: {surfPrice1}')
a = 0.63
b = 1.105

st.markdown('--------------------------------------------------')

if amountGNSBT > 0:
    result = br / 100 * a * amountGNSBT ** b
    swapAmountUSDN = float(format(result, '.2f'))
    st.markdown(f'Your max swap is {swapAmountUSDN} **USDN**')
else:
    st.markdown(f'Incorrect gNSBT value')
st.markdown('--------------------------------------------------')


if br > 10:
    swapWaves1 = float(swapAmountUSDN / wavesPrice)
    swapWaves22 = format(swapWaves1, '.9f')
    st.markdown(f'Because BR factor is above 0.1, you receive only **WAVES**')
    st.markdown(f'You can swap {swapAmountUSDN} **USDN** into  {swapWaves22} **WAVES**')
else:
    swapSurf = float(0.9 * swapAmountUSDN / (br / 100))
    swapWaves2 = float((0.1 * swapAmountUSDN)/wavesPrice)
    swapWaves23 = format(swapWaves2, '.9f')
    st.markdown('Because BR factor is under 0.1, You receive swap assets in 10% WAVES and 90% in SURF')
    st.markdown(f'{swapWaves23} **WAVES** and {swapSurf} **SURF**')
st.markdown('--------------------------------------------------')

currentWavesPrice = requests.get('https://wavescap.com/api/asset/WAVES.json').text
wavesWxPrice = float((json.loads(currentWavesPrice)['data']['lastPrice_usd-n']))

if br > 10:
    conUsdn1 = float(swapWaves1 * wavesWxPrice)
    conUsdn1_2 = float(format(conUsdn1, '.2f'))
    st.markdown(f'If you want convert all yours swap assets on Waves.Exchange you receive {conUsdn1_2} **USDN**')
else:
    conUsdn2 = float(swapWaves2 * wavesWxPrice) + (swapSurf * surfPrice)
    conUsdn2_2 = float(format(conUsdn2, '.2f'))
    st.markdown(f'If you want convert all yours swap assets on Waves.Exchange you receive {conUsdn2_2} **USDN**')

feeTransaction = float(format(0.01 * wavesWxPrice, '.4f'))
feeProtocol = float(format(0.02 * swapAmountUSDN, '.4f'))

st.markdown(f'You use 0,01 **WAVES** for TWO transaction fee what will be cost you {feeTransaction} **USDN** '
            f'and 2% fee protocol what cost you {feeProtocol} **USDN**')

if br > 10:
    res1 = float(conUsdn1_2 - swapAmountUSDN - feeTransaction - feeProtocol)
    result1 = float(format(res1, '.2f'))
    st.markdown(f'Your potential profit from the swap will be {result1} **USDN**')
else:
    res2 = float(conUsdn2_2 - swapAmountUSDN - feeTransaction - feeProtocol)
    result2 = float(format(res2, '.2f'))
    st.markdown(f'Your potential profit from the swap will be {result2} **USDN**')
st.markdown('--------------------------------------------------')

col4, col5, col6 = st.columns([2, 6, 2])
with col5:
    st.caption("You find more info about the project on https://neutrino.at/")

col7, col8, col9 = st.columns([4, 3, 4])
with col8:
    st.caption("Created by @SzypkiWonsz")