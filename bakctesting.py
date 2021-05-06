import pyupbit
import numpy as np

# OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-DOGE", count=120)
# 변동성 돌파 기준 범위 계산, (고가-저가)*K값
df['range'] = (df['high'] - df['low']) * 0.1
# rage 컬럼을 한칸씩 밑으로 내림
df['target'] = df['open'] + df['range'].shift(1)

#np.where(조건물, 참일때 값, 거짓일때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)
# 누적 곱 계싼(cumprod) => 누적수익률
df['hpr'] = df['ror'].cumprod()
# draw down 계산(누적 최대값과 현재 hpr 차이/ 누적 최대값 *100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
#MDD 계산
print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx")